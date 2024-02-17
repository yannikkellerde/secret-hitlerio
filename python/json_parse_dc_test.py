from state_model import GameUpdate
from dacite import from_dict
from compute_diff import dataclass_diff
from update_dataclass import update_dataclass
from copy import deepcopy
import json

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
]


with open("data/examples/collected_actions.json", "r") as f:
    data = json.load(f)
    old_game_update = None
    for d in data:
        gameUpdate = from_dict(data_class=GameUpdate, data=d[0])
        if old_game_update is not None:
            old_gu = deepcopy(old_game_update)
            update_dataclass(old_gu, gameUpdate)
            gameUpdate = old_gu

        if old_game_update is not None:
            diffs = dataclass_diff(old_game_update, gameUpdate, ignores=ignores)
            print(diffs)
        old_game_update = gameUpdate
