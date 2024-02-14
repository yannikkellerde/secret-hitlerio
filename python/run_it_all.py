from event_status import EventStatus
from init_sio import initialize_sio, actually_connect
from sio_events import register_events

if __name__ == "__main__":
    sio, cookie = initialize_sio()
    register_events(sio, EventStatus(), cookie)
    # actually_connect(sio, cookie)
