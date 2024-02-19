from abc import ABC, abstractmethod
from sh_game import Event
from state_model import GameUpdate
from socketio import Client
from constants import claim_map
from game_list_model import GameList
from log_util import log


class Player(ABC):
    def __init__(self, pid, game_id, username, is_smart=True):
        self.role = None
        self.pid = pid
        self.game_id = game_id
        self.username = username
        self.is_smart = is_smart

    def update_with_game_list(self, game_list: GameList):
        for i, name in enumerate(game_list.userNames):
            if name == self.username:
                self.pid = i
                break
        self.game_id = game_list.uid

    @abstractmethod
    def inform_event(self, event: dict[str, str | Event]):
        pass

    @abstractmethod
    def request_action(self, phase: Event, gameUpdate: GameUpdate):
        pass

    def action_to_server(self, sio: Client, event: Event, **kwargs):
        log(f"Action {event} with {kwargs} from {self.username}")
        match event:
            case Event.PEEK_MESSAGE:
                sio.emit(
                    "selectedPolicies",
                    {"uid": self.game_id},
                )
            case Event.PERSONAL_VOTE:
                assert "vote" in kwargs
                sio.emit(
                    "selectedVoting",
                    {"vote": kwargs["vote"], "uid": self.game_id},
                )
            case Event.PLAY_CARD:
                assert "selection" in kwargs
                sio.emit(
                    "selectedChancellorPolicy",
                    {"selection": kwargs["selection"], "uid": self.game_id},
                )
            case Event.DISCARD:
                assert "selection" in kwargs
                sio.emit(
                    "selectedPresidentPolicy",
                    {"selection": kwargs["selection"], "uid": self.game_id},
                )
            case _ if event in claim_map:
                assert "claimState" in kwargs
                sio.emit(
                    "addNewClaim",
                    {
                        "userName": self.username,
                        "claimState": kwargs["claimState"],
                        "claim": claim_map[event],
                        "uid": self.game_id,
                    },
                )
            case Event.NOMINATION:
                assert "chancellorIndex" in kwargs
                sio.emit(
                    "presidentSelectedChancellor",
                    {
                        "chancellorIndex": kwargs["chancellorIndex"],
                        "uid": self.game_id,
                    },
                )
            case Event.EXECUTE_ACTION:
                assert "playerIndex" in kwargs
                sio.emit(
                    "selectedPlayerToExecute",
                    {"playerIndex": kwargs["playerIndex"], "uid": self.game_id},
                )
            case Event.CHANCELLOR_VETO:
                assert "vote" in kwargs
                sio.emit(
                    "selectedChancellorVoteOnVeto",
                    {"vote": kwargs["vote"], "uid": self.game_id},
                )
            case Event.PRESIDENT_VETO:
                assert "vote" in kwargs
                sio.emit(
                    "selectedPresidentVoteOnVeto",
                    {"vote": kwargs["vote"], "uid": self.game_id},
                )
            case Event.MESSAGE:
                assert "chat" in kwargs
                sio.emit(
                    "addNewGameChat", {"chat": kwargs["chat"], "uid": self.game_id}
                )
