from sh_game import Event
from player_api import Player
from state_model import GameUpdate


class StupidPlayer(Player):
    def inform_event(self, event: dict[str, str | Event]):
        return super().inform_event(event)

    def request_action(self, phase: Event, gameUpdate: GameUpdate):
        return super().request_action(phase, gameUpdate)
