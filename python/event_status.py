from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EventStatus:
    game: Optional[str] = None
    fully_joined: bool = False
    tou_ready: bool = False
    join_initialized: bool = False
    collected_actions: list = field(default_factory=list)
    player_chat: list = field(default_factory=list)
