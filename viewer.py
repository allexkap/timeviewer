from collections import Counter
from datetime import datetime, timedelta
from itertools import chain

import numpy as np


def timerange(start, stop, step):
    while start < stop:
        yield start
        start += step


def get_log_handler(titles=None):
    if titles is None:
        return lambda c: c.total()
    return lambda c: sum((c[title] for title in titles), Counter())


def gen_day_view(logs, log_handler, start, stop, hour_shift=8):
    assert not timedelta(days=1) % logs.precision

    start = datetime.combine(start, datetime.min.time())
    stop = datetime.combine(stop, datetime.min.time())

    start_offset = start.weekday()
    start -= timedelta(days=start_offset)
    stop_offset = -stop.weekday() % 7
    stop += timedelta(days=stop_offset)
    shift = timedelta(hours=hour_shift)

    res = np.fromiter(
        chain.from_iterable(
            (
                (
                    sum(
                        log_handler(logs[ts + shift])
                        for ts in timerange(
                            day, day + timedelta(days=1), logs.precision
                        )
                    )
                    for day in timerange(
                        week, week + timedelta(days=7), timedelta(days=1)
                    )
                )
                for week in timerange(
                    start,
                    stop,
                    timedelta(days=7),
                )
            )
        ),
        dtype=int,
    )
    res = res.reshape(-1, 7).T

    res[:start_offset, 0] = -1
    res[res.shape[0] - stop_offset :, -1] = -1

    return res
