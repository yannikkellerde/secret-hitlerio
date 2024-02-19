from event_status import EventStatus
from init_sio import initialize_sio, actually_connect
from sio_events import register_events
from stupid_player import StupidPlayer
from event_builder import EventBuilder
import sys
import fire
from background_carry import carry_in_the_back


def run_it_all(username, creator=False):
    sio, cookie = initialize_sio(username=username)
    builder = EventBuilder(client=sio)
    builder.player = StupidPlayer(None, None, username)
    register_events(
        sio,
        EventStatus(),
        cookie=cookie,
        event_builder=builder,
        am_game_creator=creator,
    )
    carry_in_the_back(builder, sio)


if __name__ == "__main__":
    fire.Fire(run_it_all)
