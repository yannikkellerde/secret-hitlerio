import requests
import socketio
import time

game = None
done = False


def main():
    sio = socketio.Client()
    stuff = {"username": "ccc", "password": "snipsnap"}
    s = requests.Session()
    x = s.post("http://localhost:8080/account/signin", json=stuff)
    cookie = s.cookies._cookies["localhost.local"]["/"]["connect.sid"]

    @sio.event
    def connect(data=None):
        print("I'm connected!", data)
        sio.emit("confirmTOU")

    @sio.event
    def generalChats(data=None):
        print("generalChats", data)

    @sio.event
    def gameList(data):
        global game
        print("gameList", data)
        if len(data) >= 0 and game is None:
            game = data[0]["uid"]
            sio.emit("updateSeatedUser", {"uid": data[0]["uid"]})
            print("emit done")

    @sio.event
    def warningPopup(data=None):
        print("warningPopup", data)

    @sio.event
    def touChange(data=None):
        print("touChange", data)

    @sio.event
    def removeAllPopups(data=None):
        print("removeAllPopups", data)

    @sio.event
    def disconnect(data=None):
        print("disconnected", data)

    @sio.event
    def updateSeatForUser(data=None):
        global done
        print("managed to join game", data)
        if not done:
            sio.emit("getGameInfo", game)
            done = True
            sio.emit("updateUserStatus", ("", game))

    @sio.event
    def version(data=None):
        print("version", data)

    @sio.event
    def gameUpdate(*data):
        print("game_update", data)

    @sio.event
    def joinGameRedirect(data):
        print("redirect", data)

    @sio.event
    def fetchUser():
        print("fetchUser")

    @sio.event
    def playerChatUpdate(data):
        print("playerChatUpdate", data)

    sio.connect(
        "ws://localhost:8080", headers={"Cookie": f"{cookie.name}={cookie.value}"}
    )
    print(input())


main()
