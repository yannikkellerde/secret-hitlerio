from sh_game import Event
from state_model import GameUpdate
from update_dataclass import update_dataclass
from compute_diff import dataclass_diff
from copy import deepcopy
import json
from player_api import Player
from dacite import from_dict, Config
from stupid_player import StupidPlayer

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
]


class EventBuilder:
    def __init__(self):
        self.id = None
        self.role = None
        self.know_roles = False
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
            print(diff)
            for d in diff:
                self.inform_diff(d)

    def inform_diff(self, diff):
        match diff[0]:
            case "gameState.isStarted":
                if not diff[1] and diff[2]:
                    self.new_event({"event": Event.START})
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


def simulate_from_file(fpath):
    with open(fpath, "r") as f:
        data = json.load(f)
    builder = EventBuilder()
    builder.player = StupidPlayer(1, "helo", "Uther")
    for el in data[:30]:
        game_update = from_dict(
            data_class=GameUpdate, data=el, config=Config(strict=True)
        )
        builder.new_game_update(game_update)


if __name__ == "__main__":
    simulate_from_file("data/examples/game_updates.json")
