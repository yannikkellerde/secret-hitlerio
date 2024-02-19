from dataclasses import dataclass, field


@dataclass
class CreationData:
    blindMode: bool = False
    disableGamechat: bool = False
    disableObserver: bool = False
    disableObserverLobby: bool = False
    eloSliderValue: bool = None
    excludedPlayerCount: list[int] = field(default_factory=lambda: [6, 7, 8, 9, 10])
    experiencedMode: bool = True
    flag: str = "none"
    flappyMode: bool = False
    flappyOnlyMode: bool = False
    gameName: str = "eyo"
    gameType: str = "ranked"
    isTourny: bool = False
    isVerifiedOnly: bool = False
    maxPlayersCount: str = 5
    minPlayersCount: str = 5
    playerChats: str = "enabled"
    privateAnonymousRemakes: bool = False
    privatePassword: bool = False
    rainbowgame: bool = False
    rebalance6p: bool = True
    rebalance7p: bool = False
    rebalance9p2f: bool = True
    timeMode: bool = False
    unlisedGame: bool = False


@dataclass
class GameSettings:
    blacklist: list = field(default_factory=list)
    gameFilters: dict = field(default_factory=dict)
    gameNotes: dict = field(default_factory=dict)
    isPrivate: bool = False
    playerNotes: list = field(default_factory=list)
    soundStatus: str = "pack2"
    tournyWins: list = field(default_factory=list)


@dataclass
class UserData:
    userName: str
    gameSettings: GameSettings = field(default_factory=GameSettings)
    hasNotDismissedSignupModal: bool = False
    isTournamentMod: bool = False
    staffRole: str = ""
    verified: bool = False
