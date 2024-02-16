from dataclasses import dataclass, field
from typing import Optional, List, Dict, Type


@dataclass
class gameState:
    isStarted: Optional[bool]
    isCompleted: Optional[bool]
    isVetoEnabled: Optional[bool]
    isTracksFlipped: Optional[bool]
    isGameFrozen: Optional[bool]
    pendingChancellorIndex: Optional[int]
    timedModeEnabled: Optional[bool]
    phase: Optional[str]
    previousElectedGovernment: Optional[List[int]]
    presidentIndex: Optional[int]
    undrawnPolicyCount: Optional[int]
    specialElectionFormerPresidentIndex: Optional[int]
    audioCue: Optional[str]


@dataclass
class flappyState:
    liberalScore: Optional[int]
    fascistScore: Optional[int]
    pylonDensity: int = field(default=1)
    flapDistance: int = field(default=1)


@dataclass
class chatData:
    text: Optional[str]
    type: Optional[str]


@dataclass
class chat:
    chat: Optional[List[chatData]]
    type: Optional[str]
    gameChat: Optional[bool]
    isClaim: Optional[bool]
    isBroadcast: Optional[bool]
    timestamp: Optional[str]


chats = List[chat]


@dataclass
class tournyInfo:
    round: Optional[int]
    showOtherTournyTable: Optional[bool]
    queuedPlayers: Optional[list]
    isCancelled: Optional[bool]
    isRound1TableThatFinished2nd: Optional[bool]


@dataclass
class general:
    lastModPing: Optional[int]
    isVerifiedOnly: Optional[bool]
    blindMode: Optional[bool]
    name: Optional[str]
    isRemade: Optional[bool]
    gameCreatorBlacklist: Optional[list]
    replacementNames: Optional[list]
    minPlayersCount: Optional[int]
    maxPlayersCount: Optional[int]
    excludedPlayerCount: Optional[list]
    status: Optional[str]
    whitelistedPlayers: Optional[list]
    uid: Optional[str]
    timedMode: Optional[int]
    rainbowgame: Optional[bool]
    private: Optional[bool]
    gameCreatorName: Optional[str]
    timeStarted: Optional[int]
    timeCreated: Optional[str]
    experiencedMode: Optional[bool]
    casualGame: Optional[bool]
    playerChats: Optional[str]
    disableGamechat: Optional[bool]
    disableObserverLobby: Optional[bool]
    disableObserver: Optional[bool]
    playerCount: Optional[int]
    type: Optional[int]
    livingPlayerCount: Optional[int]
    electionCount: Optional[int]
    privateOnly: Optional[bool]
    isTourny: Optional[bool]
    rebalance6p: Optional[bool]
    rebalance7p: Optional[bool]
    rebalance9p: Optional[bool]
    rerebalance9p: Optional[bool]
    tourneyInfo: Optional[tournyInfo]


@dataclass
class cardBack:
    icon: Optional[int]
    roleName: Optional[str]
    team: Optional[str]


@dataclass
class cardStatus:
    cardDisplayed: Optional[bool]
    isFlipped: Optional[bool]
    cardFront: Optional[str]
    cardBack: Optional[cardBack | str]


@dataclass
class OnePublicPlayersState:
    pingTime: Optional[int]
    governmentStatus: Optional[str]
    isDead: Optional[bool]
    isConfetti: Optional[bool]
    connected: Optional[bool]
    isLoader: Optional[bool]
    leftGame: Optional[bool]
    userName: Optional[str]
    previousGovernmentStatus: Optional[str]
    cardStatus: Optional[cardStatus]


@dataclass
class trackState:
    liberalPolicyCount: Optional[int]
    electionTrackerCount: Optional[int]
    fascistPolicyCount: Optional[int]
    enactedPolicies: Optional[List[str]]


@dataclass
class seatedPlayer:
    connected: Optional[bool]
    userName: Optional[str]


@dataclass
class OneRemakeData:
    userName: Optional[str]
    isRemaking: Optional[bool]
    remakeTime: Optional[int]


@dataclass
class OneunSeatedGameChats:
    chat: Optional[str]
    timestamp: Optional[str]


unSeatedGameChats = List[OneunSeatedGameChats]


@dataclass
class OnePlayersState:
    cardBack: Optional[cardBack]
    notificationStatus: Optional[str]
    nameStatus: Optional[str]
    hasVoted: Optional[bool]
    policyNotification: Optional[bool]


playersState = List[OnePlayersState]


@dataclass
class role:
    icon: Optional[int]
    cardName: Optional[str]
    team: Optional[str]


@dataclass
class voteStatus:
    hasVoted: Optional[bool]
    didVoteYes: Optional[bool]


@dataclass
class OneCardFlingerState:
    position: Optional[str]
    notificationStatus: Optional[str]
    cardStatus: Optional[cardStatus]


cardFlingerState = List[OneCardFlingerState]


@dataclass
class PrivateSeatedPlayer:
    userName: Optional[str]
    connected: Optional[bool]
    policyNotification: Optional[bool]
    wonGame: Optional[bool]
    role: Optional[role]
    gameChats: Optional[chats]
    governmentStatus: Optional[str]
    voteStatus: Optional[voteStatus]
    cardFlingerState: Optional[cardFlingerState]
    reportedGame: Optional[bool]
    wasInvestigated: Optional[bool]
    playersState: Optional[playersState]


privateSeatedPlayers = List[PrivateSeatedPlayer]


@dataclass
class private:
    timerId: Optional[int]
    reports: Optional[dict]
    _chancellorPlayerName: Optional[str]
    timeout: Optional[dict]
    policies: Optional[list]
    currentElectionPolicies: Optional[list]
    privatePassword: Optional[str]
    unSeatedGameChats: Optional[unSeatedGameChats]
    votesPeeked: Optional[list]
    remakeVotesPeeked: Optional[list]
    gameFrozen: Optional[bool]
    seatedPlayers: Optional[privateSeatedPlayers]


@dataclass
class customGameSettings:
    enabled: Optional[bool]


remakeData = List[OneRemakeData]
seatedPlayers = List[seatedPlayer]
publicPlayersState = List[OnePublicPlayersState]


@dataclass
class GameUpdate:
    gameState: Optional[gameState]
    chats: Optional[chats]
    general: Optional[general]
    customGameSettings: Optional[customGameSettings]
    publicPlayersState: Optional[publicPlayersState]
    playersState: Optional[playersState]
    cardFlingerState: Optional[cardFlingerState]
    trackState: Optional[trackState]
    guesses: Optional[dict]
    electionCount: Optional[int]
