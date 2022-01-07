def format_duration(duration: int) -> str:
    add_zero_if_needed = lambda value: value if value >= 10 else "0" + str(value)

    if duration >= 60:
        min = int(duration / 60)
        sec = duration % 60

        if min >= 60:
            hours = int(min / 60)
            min = min % 60
            return "{}:{}:{}".format(add_zero_if_needed(hours), add_zero_if_needed(min), add_zero_if_needed(sec))
        else:
            return "{}:{}".format(add_zero_if_needed(min), add_zero_if_needed(sec))
    else:
        return "00:{}".format(add_zero_if_needed(duration))