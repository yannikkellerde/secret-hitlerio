from sh_game import Event
from state_model import GameUpdate, chat
from update_dataclass import update_dataclass
from compute_diff import dataclass_diff
from copy import deepcopy
import json
from player_api import Player
from dacite import from_dict, Config
from stupid_player import StupidPlayer
from constants import inv_claim_map

ignores = [
    "status",
    "leftGame",
    "userName",
    "isTracksFlipped",
    "audioCue",
    "timestamp",
    "timeStarted",
    "cardDisplayed",
    "isLoader",
    "isFlipped",
    "undrawnPolicyCount",
    "customGameSettings",
    "notificationStatus",
]


class EventBuilder:
    def __init__(self):
        self.events: list[dict[str, str | Event]] = []
        self.gameUpdate: GameUpdate = None
        self.player: Player = None

    def new_event(self, event: dict[str, str | Event]):
        self.player.inform_event(event)
        self.events.append(event)

    def new_game_update(self, game_update: GameUpdate):
        if self.gameUpdate is None:
            self.gameUpdate = game_update
        else:
            old_game_state = deepcopy(self.gameUpdate)
            update_dataclass(self.gameUpdate, game_update)
            diff = dataclass_diff(old_game_state, self.gameUpdate, ignores)
            for d in diff:
                print(d)
                self.inform_diff(d)

    def inform_diff(self, diff):
        if diff[0].startswith("chats"):  # This whole thing does not work right
            if diff[1] is None and isinstance(diff[2], chat):
                if diff[2].isClaim:
                    self.new_event(
                        {
                            "event": inv_claim_map[diff[2].claim],
                            "hand": diff[2].claimState,
                        }
                    )
                if isinstance(diff[2].chat, str):
                    self.new_event(
                        {"event": Event.MESSAGE, "player": diff[2].userName}
                    )  # Replace with pid?
        match diff[0]:
            case "gameState.isStarted":
                if not diff[1] and diff[2]:
                    self.new_event({"event": Event.START})
            case "trackState.electionTrackerCount":
                if diff[2] > diff[1]:
                    self.new_event({"event": Event.ELECTION_FAIL, "num": diff[2]})
            case _ if diff[0] == f"playerState[{self.player.pid}].nameStatus":
                self.new_event({"event": Event.PERSONAL_ROLE_CALL, "role": diff[2]})
            case "trackState.liberalPolicyCount":
                self.new_event(
                    {"event": Event.ENACTED, "policy_type": "liberal", "num": diff[2]}
                )
            case "trackState.fascistPolicyCount":
                self.new_event(
                    {"event": Event.ENACTED, "policy_type": "fascist", "num": diff[2]}
                )
            case "gameState.pendingChancellorIndex":
                self.new_event(
                    {
                        "event": Event.NOMINATION,
                        "pres": self.gameUpdate.gameState.presidentIndex,
                        "chanc": self.gameUpdate.gameState.pendingChancellorIndex,
                    }
                )
            case "gameState.phase":
                match diff[2]:
                    case "selectingChancellor":
                        self.player.request_action(Event.NOMINATION, self.gameUpdate)
                    case "voting":
                        self.player.request_action(Event.PERSONAL_VOTE, self.gameUpdate)
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
                                    "hand": [
                                        x.cardStatus.cardBack[:-1]
                                        for x in self.gameUpdate.cardFlingerState
                                        if x is not None
                                    ],
                                }
                            )
                            self.player.request_action(Event.DISCARD, self.gameUpdate)
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
                                    "hand": [
                                        x.cardStatus.cardBack[:-1]
                                        for x in self.gameUpdate.cardFlingerState
                                        if x is not None
                                    ],
                                }
                            )
                            self.player.request_action(Event.PLAY_CARD, self.gameUpdate)


def simulate_from_file(fpath):
    with open(fpath, "r") as f:
        data = json.load(f)
    builder = EventBuilder()
    builder.player = StupidPlayer(1, "helo", "Uther")
    for el in data[:130]:
        game_update = from_dict(
            data_class=GameUpdate, data=el, config=Config(strict=True)
        )
        builder.new_game_update(game_update)


if __name__ == "__main__":
    simulate_from_file("data/examples/game_updates.json")
