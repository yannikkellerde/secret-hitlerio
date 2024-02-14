import requests
import socketio
from dataclasses import dataclass
from typing import Optional


def initialize_sio(username="ccc", password="snipsnap"):
    sio = socketio.Client()
    stuff = {"username": username, "password": password}
    s = requests.Session()
    s.post("http://localhost:8080/account/signin", json=stuff)
    cookie = s.cookies._cookies["localhost.local"]["/"]["connect.sid"]

    return sio, cookie


def actually_connect(sio, cookie):
    sio.connect(
        "ws://localhost:8080", headers={"Cookie": f"{cookie.name}={cookie.value}"}
    )
