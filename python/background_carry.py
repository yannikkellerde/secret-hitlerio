from event_builder import EventBuilder
from sh_game import Event
from socketio import Client
import time
from log_util import log
import logging


def carry_in_the_back(builder: EventBuilder, sio: Client, sleeptime=10):
    while 1:
        time.sleep(sleeptime)
        if builder.gameUpdate is not None and (
            builder.player.last_action_time is None
            or time.time() - builder.player.last_action_time > sleeptime / 2
        ):
            match builder.gameUpdate.gameState.phase:
                case "voting" if len(builder.gameUpdate.cardFlingerState) == 2:
                    for flinger in builder.gameUpdate.cardFlingerState:
                        if flinger.notificationStatus == "selected":
                            break
                    else:
                        log(
                            "Background carry stepping in with PERSONAL_VOTE action",
                            level=logging.WARNING,
                        )
                        builder.perform_action(Event.PERSONAL_VOTE)
                case "presidentSelectingPolicy":
                    if (
                        builder.gameUpdate.publicPlayersState[
                            builder.player.pid
                        ].governmentStatus
                        == "isPresident"
                    ):
                        log(
                            "Background carry stepping in with DISCARD action",
                            level=logging.WARNING,
                        )
                        builder.perform_action(Event.DISCARD)
                case "chancellorSelectingPolicy":
                    if (
                        builder.gameUpdate.publicPlayersState[
                            builder.player.pid
                        ].governmentStatus
                        == "isChancellor"
                    ):
                        log(
                            "Background carry stepping in with PlayCard action",
                            level=logging.WARNING,
                        )
                        builder.perform_action(Event.PLAY_CARD)
                case _:
                    log(
                        "Background carry stepping in with message action",
                        level=logging.WARNING,
                    )
                    sio.emit("getGameInfo", builder.gameUpdate.general.uid)
                    builder.perform_action(Event.MESSAGE)
