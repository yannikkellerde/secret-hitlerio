from dataclasses import dataclass, field
from state_model import GameUpdate


@dataclass
class BoardInfo:
    chancellor: int = field(default=None)
    president: int = field(default=None)
    term_blocked: list[int] = field(default_factory=list)
    num_players: int = field(default=None)
    dead_players: list[int] = field(default_factory=list)

    @classmethod
    def from_game_update(cls, game_update: GameUpdate):
        return cls(
            chancellor=game_update.gameState.pendingChancellorIndex,
            president=game_update.gameState.presidentIndex,
            num_players=game_update.general.playerCount,
            dead_players=[
                i for i, ps in enumerate(game_update.publicPlayersState) if ps.isDead
            ],
        )
