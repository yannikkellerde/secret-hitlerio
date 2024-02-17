from dataclasses import is_dataclass, fields


def dataclass_diff(dc1, dc2, ignores):
    diffs = []
    for field in fields(dc1):
        if field.name in ignores:
            continue
        val1 = getattr(dc1, field.name)
        val2 = getattr(dc2, field.name)
        if (val1 is None and val2 is not None) or (val1 is not None and val2 is None):
            diffs.append([field.name, val1, val2])
        elif is_dataclass(val1):
            if is_dataclass(val2):
                sub_diffs = dataclass_diff(
                    getattr(dc1, field.name), getattr(dc2, field.name), ignores
                )
                diffs.extend([[f"{field.name}.{x[0]}"] + x[1:] for x in sub_diffs])
            else:
                diffs.append([field.name, val1, val2])
        elif isinstance(val1, list):
            if isinstance(val2, list):
                for i, (e1, e2) in enumerate(zip(val1, val2)):
                    if is_dataclass(e1) and is_dataclass(e2):
                        sub_diffs = dataclass_diff(e1, e2, ignores)
                        diffs.extend(
                            [[f"{field.name}[{i}].{x[0]}"] + x[1:] for x in sub_diffs]
                        )
                    else:
                        if e1 != e2:
                            diffs.append([f"{field.name}[{i}]", e1, e2])

                if len(val1) > len(val2):
                    for i in range(len(val2), len(val1)):
                        diffs.append([f"{field.name}[{i}]", val1[i], None])
                elif len(val2) > len(val1):
                    for i in range(len(val1), len(val2)):
                        diffs.append([f"{field.name}[{i}]", None, val2[i]])
            else:
                diffs.append([field.name, val1, val2])
        else:
            if val1 != val2:
                diffs.append([field.name, val1, val2])

    return diffs
