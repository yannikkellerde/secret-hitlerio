from sh_game import Event
from player_api import Player
from state_model import GameUpdate
import random


class StupidPlayer(Player):
    def __init__(self, pid, game_id, username):
        self.collected_events = []
        super().__init__(pid, game_id, username, is_smart=False)

    def inform_event(self, event: dict[str, str | Event]):
        self.collected_events.append(event)

    def request_action(self, phase: Event, gameUpdate: GameUpdate):
        match phase:
            case Event.PERSONAL_VOTE:
                return {
                    "event": Event.DISCARD,
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
                options = [Event.MESSAGE, Event.NOOP]
                if (
                    gameUpdate.publicPlayersState[self.pid].governmentStatus
                    == "isPresident"
                ):
                    match gameUpdate.gameState.phase:
                        case "execution":
                            options.append(Event.EXECUTE_ACTION)
                        case "presidentVoteOnVeto":
                            options.append(Event.PRESIDENT_VETO)
                if gameUpdate.playersState[self.pid].governmentStatus == "isChancellor":
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
                    phase == Event.NOMINATION
                    and gameUpdate.publicPlayersState[self.pid].governmentStatus
                    == "isPendingPresident"
                    and gameUpdate.gameState.phase == "selectingChancellor"
                ):
                    options.append(Event.NOMINATION)

                event = random.choice(options)
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
