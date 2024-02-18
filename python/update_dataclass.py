from dataclasses import is_dataclass, fields


def update_dataclass(dc1, dc2):
    for field in fields(dc1):
        val1 = getattr(dc1, field.name)
        val2 = getattr(dc2, field.name)
        if val2 is None:
            continue
        if is_dataclass(val1):
            if is_dataclass(val2):
                update_dataclass(val1, val2)
            else:
                setattr(dc1, field.name, val2)
        elif isinstance(val1, list):
            if len(val1) > 0 and is_dataclass(val1[0]):
                for i, (e1, e2) in enumerate(zip(val1, val2)):
                    if is_dataclass(e1) and is_dataclass(e2) and field.name != "chats":
                        update_dataclass(e1, e2)
                    else:
                        val1[i] = e2

                if len(val2) > len(val1):
                    for e2 in val2[len(val1) :]:
                        val1.append(e2)
                elif len(val1) > len(val2):
                    setattr(dc1, field.name, val1[: len(val2)])
            elif val2 is not None:
                setattr(dc1, field.name, val2)

        elif val2 is not None:
            setattr(dc1, field.name, val2)
