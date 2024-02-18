import socketio
from event_status import EventStatus
from event_builder import EventBuilder
from dacite import from_dict
from state_model import GameUpdate
import json
import os


def register_events(
    sio: socketio.Client, status: EventStatus, event_builder: EventBuilder, cookie
):
    @sio.event
    def connect():
        sio.emit("confirmTOU")
        print("I'm connected!")

    @sio.event
    def disconnect():
        print("got disconnected :(")

    @sio.event
    def gameList(data):
        print("gameList", data)
        if len(data) > 0 and status.game is None:
            status.game = data[0]["uid"]
            if status.tou_ready and not status.join_initialized:
                status.join_initialized = True
                sio.emit("updateSeatedUser", {"uid": status.game})
            elif not status.tou_ready:
                sio.emit("confirmTOU")

    @sio.event
    def touChangeConfirmed(data):
        print("touChangeConfirmed", data)
        status.tou_ready = True
        if status.game and not status.join_initialized:
            status.join_initialized = True
            sio.emit("updateSeatedUser", {"uid": status.game})

    @sio.event
    def updateSeatForUser(data=None):
        if not status.fully_joined:
            sio.emit("getGameInfo", status.game)
            sio.emit("updateUserStatus", ("", status.game))
            status.fully_joined = True
            print("Successfully joined game", status.game)

    @sio.event
    def gameUpdate(*data):
        game_update = from_dict(data[0], GameUpdate)
        event_builder.new_game_update(game_update)

    @sio.event
    def playerChatUpdate(data):
        status.player_chat.append(data)

    sio.connect(
        "ws://localhost:8080", headers={"Cookie": f"{cookie.name}={cookie.value}"}
    )
