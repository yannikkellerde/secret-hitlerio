from sh_game import Event
import socketio
import requests

collected_actions = []
player_chat = []


def collect_actions(sio: socketio.Client):
    @sio.event
    def gameUpdate(*data):
        collected_actions.append(data)

    @sio.event
    def playerChatUpdate(data):
        player_chat.append(data)
