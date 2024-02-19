from sh_game import Event
from socketio import Client
from player_api import Player
from state_model import GameUpdate
import random
import time
from log_util import log


class StupidPlayer(Player):
    def __init__(self, pid, game_id, username):
        self.collected_events = []
        self.last_action_time = None
        self.last_action_hash = None
        self.last_action_type = None
        self.low_prio_actions = [
            Event.MESSAGE,
            Event.PEEK_CLAIM,
            Event.PRESIDENT_CLAIM,
            Event.CHANCELLOR_CLAIM,
        ]
        self.slow_time = 2
        super().__init__(pid, game_id, username, is_smart=False)

    def action_to_server(self, sio: Client, event: Event, **kwargs):
        if (
            self.last_action_type is not None
            and event in self.low_prio_actions
            and self.last_action_type not in self.low_prio_actions
        ):
            log(
                f"Low prio action {event} was ignored in favor of {self.last_action_type}"
            )
            return
        action_hash = hash((event, tuple(sorted(kwargs.items()))))
        self.last_action_hash = action_hash
        self.last_action_type = event
        my_time = time.time()
        if self.last_action_time is not None:
            if my_time - self.last_action_time < self.slow_time:
                time.sleep(self.last_action_time + self.slow_time - my_time)
        if self.last_action_hash != action_hash:
            log(f"Action {event} was overridden")
            return
        self.last_action_time = time.time()
        self.last_action_type = None
        return super().action_to_server(sio, event, **kwargs)

    def inform_event(self, event: dict[str, str | Event]):
        log(f"Player {self.username} received event {event}")
        self.collected_events.append(event)

    def request_action(self, phase: Event, gameUpdate: GameUpdate):
        match phase:
            case Event.PERSONAL_VOTE:
                return {
                    "event": Event.PERSONAL_VOTE,
                    "vote": random.choice((True, False)),
                }
            case Event.DISCARD:
                # options = gameUpdate.get_card_flinger_hand()
                return {
                    "event": Event.DISCARD,
                    "selection": random.randint(0, 2),
                }
            case Event.PLAY_CARD:
                return {
                    "event": Event.PLAY_CARD,
                    "selection": random.choice([0, 3]),
                }
            case Event.MESSAGE:  # Phase 2 and 6
                options = []
                if (
                    gameUpdate.publicPlayersState[self.pid].governmentStatus
                    == "isPresident"
                ):
                    match gameUpdate.gameState.phase:
                        case "execution":
                            options.append(Event.EXECUTE_ACTION)
                        case "presidentVoteOnVeto":
                            options.append(Event.PRESIDENT_VETO)
                    if gameUpdate.general.status == "President to peek at policies.":
                        options.append(Event.PEEK_MESSAGE)
                if (
                    gameUpdate.publicPlayersState[self.pid].governmentStatus
                    == "isChancellor"
                ):
                    if gameUpdate.gameState.phase == "chancellorVoteOnVeto":
                        options.append(Event.CHANCELLOR_VETO)

                match gameUpdate.playersState[self.pid].claim:
                    case "wasChancellor":
                        options.append(Event.CHANCELLOR_CLAIM)
                    case "wasPresident":
                        options.append(Event.PRESIDENT_CLAIM)
                    case "didPolicyPeek":
                        options.append(Event.PEEK_CLAIM)
                if (
                    gameUpdate.publicPlayersState[self.pid].governmentStatus
                    == "isPendingPresident"
                    and gameUpdate.gameState.phase == "selectingChancellor"
                ):
                    options.append(Event.NOMINATION)

                if len(options) == 0:
                    options = [Event.NOOP, Event.MESSAGE]

                event = random.choice(options)
                log(self.username, options)
                match event:
                    case Event.NOOP:
                        return None
                    case Event.MESSAGE:
                        return {
                            "event": Event.MESSAGE,
                            "chat": f"I, {self.username}, {self.pid} am a stupid player",
                        }
                    case Event.NOMINATION:
                        valid_nominees = gameUpdate.gameState.clickActionInfo[1]
                        return {
                            "event": Event.NOMINATION,
                            "chancellorIndex": random.choice(valid_nominees),
                        }
                    case Event.EXECUTE_ACTION:
                        valid_targets = gameUpdate.gameState.clickActionInfo[1]
                        return {
                            "event": Event.EXECUTE_ACTION,
                            "playerIndex": random.choice(valid_targets),
                        }
                    case Event.CHANCELLOR_VETO | Event.PRESIDENT_VETO:
                        return {
                            "event": event,
                            "vote": random.choice([True, False]),
                        }
                    case (
                        Event.PRESIDENT_CLAIM
                        | Event.CHANCELLOR_CLAIM
                        | Event.PEEK_CLAIM
                    ):
                        return {
                            "event": event,
                            "claimState": "".join(
                                [
                                    random.choice("rb")
                                    for _ in range(
                                        2 if event == Event.CHANCELLOR_CLAIM else 3
                                    )
                                ]
                            ),
                        }
            case _:
                return {"event": phase}
