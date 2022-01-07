def format_duration(duration: int) -> str:
    add_zero_if_needed = lambda value: value if value >= 10 else "0" + str(value)
    if duration >= 60:
        min = int(duration / 60)
        sec = duration % 60
        return "{}:{}".format(add_zero_if_needed(min), add_zero_if_needed(sec))
    else:
        return add_zero_if_needed(duration)