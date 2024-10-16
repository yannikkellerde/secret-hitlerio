from sh_game import Event
from state_model import GameUpdate, chat, chatData
from update_dataclass import update_dataclass
from compute_diff import dataclass_diff
from copy import deepcopy
import json
from player_api import Player
from dacite import from_dict, Config
from stupid_player import StupidPlayer
from constants import inv_claim_map
from datetime import datetime
from socketio import Client
import re
from typing import Optional
from log_util import log

ignores = [
    "leftGame",
    "userName",
    "isTracksFlipped",
    "audioCue",
    "timeStarted",
    "cardDisplayed",
    "isLoader",
    "isFlipped",
    "undrawnPolicyCount",
    "customGameSettings",
]


def diff_split(diff_info):
    nums = [int(x) for x in re.findall(r"\[(\d)+\]", diff_info)]
    return re.sub(r"\[\d+\]", "", diff_info), nums


class EventBuilder:
    def __init__(self, client: Client = None):
        self.events: list[dict[str, str | Event]] = []
        self.gameUpdate: GameUpdate = None
        self.player: Player = None
        self.chat_timestamp: datetime = None
        self.next_timestamp: datetime = None
        self.client: Optional[Client] = client

    def new_event(self, event: dict[str, str | Event]):
        self.player.inform_event(event)
        self.events.append(event)

    def perform_action(self, event: Event):
        act = self.player.request_action(event, self.gameUpdate)
        if self.client is not None and act is not None:
            self.player.action_to_server(self.client, **act)

    def new_game_update(self, game_update: GameUpdate):
        if self.gameUpdate is None:
            self.gameUpdate = game_update
        else:
            old_game_state = deepcopy(self.gameUpdate)
            update_dataclass(self.gameUpdate, game_update)
            diff = dataclass_diff(old_game_state, self.gameUpdate, ignores)
            some_diff = [x for x in diff if not x[0].startswith("chats")]
            # if some_diff:
            #    log(some_diff)
            for d in diff:
                if "phase" in str(d):
                    log(d)
                self.inform_diff(d)
            if self.next_timestamp is not None:
                self.chat_timestamp = self.next_timestamp
                self.next_timestamp = None

    def inform_diff(self, diff):
        d_first, nums = diff_split(diff[0])
        if d_first.endswith("discard"):
            log(diff)
        match d_first:
            case "gameState.isCompleted":
                if diff[2]:
                    self.new_event(
                        {
                            "event": (
                                Event.FASCIST_WIN
                                if diff[2] == "fascist"
                                else Event.LIBERAL_WIN
                            )
                        }
                    )
            case "publicPlayersState.isDead":
                if diff[2]:
                    self.new_event(
                        {
                            "event": Event.EXECUTE_ACTION,
                            "killed": nums[0],
                            "killer": self.gameUpdate.gameState.presidentIndex,
                        }
                    )
            case "chats":
                if isinstance(diff[2], chat) and diff[2].timestamp is not None:
                    chat_time = datetime.strptime(
                        diff[2].timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    if self.chat_timestamp is None or chat_time > self.chat_timestamp:
                        self.next_timestamp = chat_time
                        if diff[2].isClaim:
                            self.new_event(
                                {
                                    "event": inv_claim_map[diff[2].claim],
                                    "hand": diff[2].claimState,
                                }
                            )
                            if (
                                diff[2].userName != self.player.username
                                or self.player.is_smart
                            ):
                                self.perform_action(Event.MESSAGE)
                        if isinstance(diff[2].chat, str):
                            self.new_event(
                                {
                                    "event": Event.MESSAGE,
                                    "player": self.gameUpdate.id_from_username(
                                        diff[2].userName
                                    ),
                                    "text": diff[2].chat,
                                }
                            )
                            if (
                                diff[2].userName != self.player.username
                                or self.player.is_smart
                            ):
                                self.perform_action(Event.MESSAGE)
                        elif isinstance(diff[2].chat, list):
                            for cd in diff[2].chat:
                                if isinstance(cd, chatData):
                                    if cd.text == " has voted to veto this election.":
                                        self.new_event(
                                            {
                                                "event": (
                                                    Event.CHANCELLOR_VETO
                                                    if self.gameUpdate.gameState.phase
                                                    == "chancellorVoteOnVeto"
                                                    else Event.PRESIDENT_VETO
                                                ),
                                                "veto": True,
                                            }
                                        )
                                        if (
                                            diff[2].userName != self.player.username
                                            or self.player.is_smart
                                        ):
                                            self.perform_action(Event.MESSAGE)
                                    elif (
                                        cd.text
                                        == " has voted not to veto this election."
                                    ):
                                        self.new_event(
                                            {
                                                "event": (
                                                    Event.CHANCELLOR_VETO
                                                    if self.gameUpdate.gameState.phase
                                                    == "chancellorVoteOnVeto"
                                                    else Event.PRESIDENT_VETO
                                                ),
                                                "veto": False,
                                            }
                                        )
                                        if (
                                            diff[2].userName != self.player.username
                                            or self.player.is_smart
                                        ):
                                            self.perform_action(Event.MESSAGE)
            case "playersState.policyNotification":
                if nums[0] == self.player.pid and diff[1] and not diff[2]:
                    self.new_event(
                        {
                            "event": Event.PEEK_PERSONAL,
                            "hand": self.gameUpdate.get_card_flinger_hand(),
                        }
                    )
            case "general.status":
                if diff[2] == "President to peek at policies.":
                    self.new_event({"event": Event.PEEK_MESSAGE})
                    self.perform_action(Event.PEEK_MESSAGE)
            case "gameState.isStarted":
                if not diff[1] and diff[2]:
                    self.new_event({"event": Event.START})
            case "trackState.electionTrackerCount":
                if diff[2] > diff[1]:
                    self.new_event({"event": Event.ELECTION_FAIL, "num": diff[2]})
                    if diff[2] == 3:
                        self.new_event({"event": Event.CHAOS_POLICY})
            case "playersState.nameStatus" if nums[0] == self.player.pid:
                self.new_event({"event": Event.PERSONAL_ROLE_CALL, "role": diff[2]})
                self.perform_action(Event.MESSAGE)
            case "trackState.liberalPolicyCount":
                self.new_event(
                    {"event": Event.ENACTED, "policy_type": "liberal", "num": diff[2]}
                )
                self.perform_action(Event.MESSAGE)
            case "trackState.fascistPolicyCount":
                self.new_event(
                    {"event": Event.ENACTED, "policy_type": "fascist", "num": diff[2]}
                )
                self.perform_action(Event.MESSAGE)
            case "gameState.pendingChancellorIndex":
                self.new_event(
                    {
                        "event": Event.NOMINATION,
                        "pres": self.gameUpdate.gameState.presidentIndex,
                        "chanc": self.gameUpdate.gameState.pendingChancellorIndex,
                    }
                )
                self.perform_action(Event.MESSAGE)
            case "gameState.phase":
                if diff[1] == "voting":
                    votes = [
                        x.cardStatus.cardBack.cardName
                        for x in self.gameUpdate.publicPlayersState
                    ]
                    self.new_event({"event": Event.VOTES, "votes": votes})
                match diff[2]:
                    case "execution":
                        self.new_event({"event": Event.EXECUTE_MESSAGE})
                        self.perform_action(Event.MESSAGE)
                    case "selectingChancellor":
                        self.perform_action(Event.MESSAGE)
                    case "voting":
                        self.perform_action(Event.PERSONAL_VOTE)
                    case "presidentSelectingPolicy":
                        if (
                            self.gameUpdate.publicPlayersState[
                                self.player.pid
                            ].governmentStatus
                            == "isPresident"
                        ):
                            self.new_event(
                                {
                                    "event": Event.DRAW,
                                    "hand": self.gameUpdate.get_card_flinger_hand(),
                                }
                            )
                            self.perform_action(Event.DISCARD)
                        else:
                            self.perform_action(Event.MESSAGE)
                    case "chancellorSelectingPolicy":
                        if (
                            self.gameUpdate.publicPlayersState[
                                self.player.pid
                            ].governmentStatus
                            == "isChancellor"
                        ):
                            self.new_event(
                                {
                                    "event": Event.GET_CARD,
                                    "hand": self.gameUpdate.get_card_flinger_hand(),
                                }
                            )
                            self.perform_action(Event.PLAY_CARD)
                        else:
                            self.perform_action(Event.MESSAGE)


def simulate_from_file(fpath):
    with open(fpath, "r") as f:
        data = json.load(f)
    builder = EventBuilder()
    builder.player = StupidPlayer(2, "helo", "Uther")
    for el in data:
        game_update = from_dict(
            data_class=GameUpdate, data=el, config=Config(strict=True)
        )
        builder.new_game_update(game_update)
    log(json.dumps(builder.events, indent=4))


if __name__ == "__main__":
    simulate_from_file("data/examples/game_updates.json")
