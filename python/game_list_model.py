from dataclasses import dataclass
from typing import Optional


@dataclass
class GameList:
    name: Optional[str]
    flag: Optional[str]
    userNames: Optional[list[str]]
    customCardback: Optional[list[str | None]]
    customCardbackUid: Optional[list[str | None]]
    gameStatus: Optional[str]
    seatedCount: Optional[int]
    gameCreatorName: Optional[str]
    minPlayersCount: Optional[int]
    maxPlayersCount: Optional[int]
    excludePlayerCount: Optional[list[int]]
    experiencedMode: Optional[bool]
    playerChats: Optional[str]
    enactedLiberalPolicyCount: Optional[int]
    enactedFascistPolicyCount: Optional[int]
    electionCount: Optional[int]
    uid: Optional[str]
    isCustomGame: Optional[bool]
