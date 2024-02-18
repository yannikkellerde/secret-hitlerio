from dataclasses import dataclass, field
from typing import Optional, List, Dict, Type


@dataclass
class gameState:
    isStarted: Optional[bool]
    isCompleted: Optional[str]
    timeCompleted: Optional[int]
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
    discardedPolicyCount: Optional[int]
    clickActionInfo: Optional[List[str | List[int]]]


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
    claim: Optional[str]
    policies: Optional[List[str]]


@dataclass
class chat:
    chat: Optional[str | List[chatData]]
    type: Optional[str]
    gameChat: Optional[bool]
    isClaim: Optional[bool]
    isBroadcast: Optional[bool]
    timestamp: Optional[str]
    claim: Optional[str]
    claimState: Optional[str]
    userName: Optional[str]
    uid: Optional[str]
    isRemainingPolicies: Optional[bool]


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
    rebalance9p2f: Optional[bool]
    rerebalance9p: Optional[bool]
    tourneyInfo: Optional[tournyInfo]
    practiceGame: Optional[bool]
    eloMinimum: Optional[int]
    flappyMode: Optional[bool]
    unlistedGame: Optional[bool]
    flag: Optional[str]
    privateAnonymousRemakes: Optional[bool]
    chatReplTime: Optional[List[int]]
    timeAbandoned: Optional[int]
    flappyOnlyMode: Optional[bool]
    isRecorded: Optional[bool]


@dataclass
class cardBack:
    icon: Optional[int]
    roleName: Optional[str]
    team: Optional[str]
    cardName: Optional[str]


@dataclass
class cardStatus:
    cardDisplayed: Optional[bool]
    isFlipped: Optional[bool]
    cardFront: Optional[str]
    cardBack: Optional[cardBack | str]


@dataclass
class enactedCard:
    cardBack: Optional[cardBack | str]
    isFlipped: Optional[bool]
    position: Optional[str]


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
    isPrivate: Optional[bool]
    tournyWins: Optional[List[str]]
    notificationStatus: Optional[str]
    nameStatus: Optional[str]


@dataclass
class trackState:
    liberalPolicyCount: Optional[int]
    electionTrackerCount: Optional[int]
    fascistPolicyCount: Optional[int]
    enactedPolicies: Optional[List[enactedCard]]


@dataclass
class seatedPlayer:
    connected: Optional[bool]
    userName: Optional[str]


@dataclass
class OneRemakeData:
    userName: Optional[str]
    isRemaking: Optional[bool]
    remakeTime: Optional[int]
    timesVoted: Optional[int]


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
    cardStatus: Optional[cardStatus]
    claim: Optional[str]


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
    action: Optional[str]
    discard: Optional[bool]


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
class privInfo:
    reports: Optional[dict]
    unSeatedGameChats: Optional[list]
    commandChats: Optional[dict]
    replayGameChats: Optional[list]
    lock: Optional[dict]
    votesPeeked: Optional[bool]
    remakeVotesPeeked: Optional[bool]
    invIndex: Optional[int]
    hiddenInfoChat: Optional[list]
    hiddenInfoSubscriptions: Optional[list]
    hiddenInfoShouldNotify: Optional[bool]
    gameCreatorName: Optional[str]
    gameCreatorBlacklist: Optional[list]


@dataclass
class RoleState:
    lib: Optional[int]
    fas: Optional[int]


@dataclass
class customGameSettings:
    enabled: Optional[bool]
    hitlerZone: Optional[int]
    vetoZone: Optional[int]
    trackState: Optional[RoleState]
    deckState: Optional[RoleState]
    fascistCount: Optional[int]
    hitKnowsFas: Optional[bool]
    powers: Optional[List[str | None]]


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
    private: Optional[privInfo]
    remakeData: Optional[remakeData]
    summary: Optional[dict]
    summarySaved: Optional[bool]

    def get_card_flinger_hand(self):
        return [
            x.cardStatus.cardBack[:-1] for x in self.cardFlingerState if x is not None
        ]

    def id_from_username(self, username):
        for i, player in enumerate(self.publicPlayersState):
            if player.userName == username:
                return i
