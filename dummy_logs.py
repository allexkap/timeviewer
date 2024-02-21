import random
from collections import Counter
from datetime import datetime, timedelta


class DummyLogs:
    precision = timedelta(days=1)

    def __init__(self, seed=None):
        self.random = random.Random(seed)

    def __getitem__(self, ts: datetime):
        return Counter({'': self.random.randint(0, 255)})
