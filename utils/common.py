def clamp(min_value, max_value, value):
    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


def time_trans_m(second: int):
    return "{:>d}:{:02d}".format(second // 60, second % 60)
