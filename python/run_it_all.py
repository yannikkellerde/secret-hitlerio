from event_status import EventStatus
from init_sio import initialize_sio, actually_connect
from sio_events import register_events
from event_builder import EventBuilder

if __name__ == "__main__":
    sio, cookie = initialize_sio()
    builder = EventBuilder(client=sio)
    register_events(sio, EventStatus(), cookie=cookie, event_builder=builder)
    # actually_connect(sio, cookie)
