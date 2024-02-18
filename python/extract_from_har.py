import json


def rem_starting_digits(string):
    while string[0].isdigit():
        string = string[1:]
    return string


def bring_into_good_shape(har_file):
    with open(har_file) as f:
        hardata = json.load(f)

    entries = hardata["log"]["entries"]
    my_entry = [x for x in entries if "_webSocketMessages" in x.keys()][0]
    ws_msgs = my_entry["_webSocketMessages"]

    for msg in ws_msgs:
        try:
            d = json.loads(rem_starting_digits(msg["data"]))
            if len(d) > 0:
                msg["data"] = d
        except:
            pass

    return ws_msgs


def extract_game_updates(ws_msgs):
    return [
        x["data"][1]
        for x in ws_msgs
        if isinstance(x["data"], list) and x["data"][0] == "gameUpdate"
    ]


def extract_none_game_updates(ws_msgs):
    return [
        x["data"][1:]
        for x in ws_msgs
        if isinstance(x["data"], list) and x["data"][0] != "gameUpdate"
    ]


def get_sent_messages(ws_msgs):
    return [x["data"] for x in ws_msgs if x["type"] == "send"]


if __name__ == "__main__":
    ws_msgs = bring_into_good_shape("data/harharhar/localhost_final.har")
    game_updates = extract_game_updates(ws_msgs)
    none_game_updates = extract_none_game_updates(ws_msgs)
    sent_messages = get_sent_messages(ws_msgs)

    for dat, fname in [
        (ws_msgs, "data/examples/ws_msgs.json"),
        (game_updates, "data/examples/game_updates.json"),
        (sent_messages, "data/examples/sent_messages.json"),
        (none_game_updates, "data/examples/none_game_updates.json"),
    ]:
        with open(fname, "w") as f:
            json.dump(dat, f, indent=2)
