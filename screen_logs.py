import json
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import yaml  # remove


class ScreenLogs:
    precision = timedelta(hours=1)
    timestamp_format = r'%y%m%d%H'

    def __init__(self, db_path, raw_path, bak_path):
        self.db_path = Path(db_path)
        self.raw_path = Path(raw_path)
        self.bak_path = Path(bak_path)
        self.logs = self._load()
        self.update()

    def _load(self):
        if not self.db_path.exists():
            return dict()
        with open(self.db_path) as file:
            return {k: Counter(v) for k, v in json.load(file).items()}

    def _dump(self):
        with open(self.db_path, 'w') as file:
            return json.dump(self.logs, file)

    def update(self):
        logs = dict()
        parsed_entries = []
        now = int(datetime.now().strftime(ScreenLogs.timestamp_format))
        for entry in sorted(self.raw_path.glob('*')):
            if not re.match(r'\d{8}$', entry.name):
                continue
            if int(entry.stem) >= now:
                continue
            with open(entry) as file:
                logs[entry.stem] = Counter(yaml.load(file.read(), yaml.Loader))
            parsed_entries.append(entry)
        self.logs.update(logs)
        self._dump()
        for entry in parsed_entries:
            entry.rename(self.bak_path / entry.name)

    def __getitem__(self, ts: datetime):
        return self.logs.get(ts.strftime(ScreenLogs.timestamp_format), Counter())
