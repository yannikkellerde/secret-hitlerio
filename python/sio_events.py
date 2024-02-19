import socketio
from event_status import EventStatus
from event_builder import EventBuilder
from dacite import from_dict
from state_model import GameUpdate
from game_list_model import GameList
from dataclasses import asdict
from event_models import CreationData, UserData
from log_util import log
import json
import os


def register_events(
    sio: socketio.Client,
    status: EventStatus,
    event_builder: EventBuilder,
    cookie,
    am_game_creator=False,
):
    @sio.event
    def connect():
        sio.emit("sendUser", asdict(UserData(userName=event_builder.player.username)))
        sio.emit("getUserGameSettings")
        sio.emit("confirmTOU")
        log("I'm connected!")

    @sio.event
    def disconnect():
        log("got disconnected :(")

    @sio.event
    def fetchUser():
        sio.emit("sendUser", asdict(UserData(userName=event_builder.player.username)))

    @sio.event
    def gameList(data):
        log("gameList", data)
        if len(data) > 0:
            gls = [from_dict(data=game, data_class=GameList) for game in data]
            if status.game is None:
                if status.tou_ready and not status.join_initialized:
                    status.game = gls[0].uid
                    status.join_initialized = True
                    sio.emit("updateSeatedUser", {"uid": status.game})
                elif not status.tou_ready:
                    sio.emit("confirmTOU")
            for gl in gls:
                if gl.uid == status.game:
                    event_builder.player.update_with_game_list(gl)
        elif am_game_creator:
            if status.am_in_user_list:
                if status.tou_ready and not status.creation_request_sent:
                    status.creation_request_sent = True
                    sio.emit("addNewGame", asdict(CreationData()))
                else:
                    sio.emit("confirmTOU")
            else:
                sio.emit("getUserGameSettings")

    @sio.event
    def userList(data):
        if not status.am_in_user_list:
            for user in data["list"]:
                log(user)
                if user["userName"] == event_builder.player.username:
                    status.am_in_user_list = True
                    if not status.creation_request_sent:
                        sio.emit("getGameList")
                    break
            else:
                sio.emit("getUserGameSettings")

    @sio.event
    def touChangeConfirmed(data):
        log("touChangeConfirmed", data)
        status.tou_ready = True
        sio.emit("getGameList")

    @sio.event
    def updateSeatForUser(data=None):
        if not status.fully_joined:
            sio.emit("getGameInfo", status.game)
            sio.emit("updateUserStatus", ("", status.game))
            status.fully_joined = True
            log("Successfully joined game", status.game)

    @sio.event
    def gameUpdate(*data):
        game_update = from_dict(data=data[0], data_class=GameUpdate)
        event_builder.new_game_update(game_update)

    @sio.event
    def playerChatUpdate(data):
        status.player_chat.append(data)

    sio.connect(
        "ws://localhost:8080", headers={"Cookie": f"{cookie.name}={cookie.value}"}
    )
