"""Application logging setup."""

from __future__ import annotations

import logging
import sys
import time
from datetime import datetime, timezone

from utils.paths import log_dir


class HourlyUTCFileHandler(logging.FileHandler):
    """Append each record to its UTC hour without overwriting earlier records."""

    def __init__(self, directory):
        self.directory = directory
        first = self.path_for(datetime.now(timezone.utc).timestamp())
        super().__init__(first, encoding="utf-8", delay=True)

    def path_for(self, created):
        stamp = datetime.fromtimestamp(created, timezone.utc).strftime("%Y%m%d%H")
        return self.directory / (stamp + "-media-manager-runtime.log")

    def emit(self, record):
        expected = str(self.path_for(record.created).resolve())
        if expected != self.baseFilename:
            if self.stream:
                self.stream.close()
                self.stream = None
            self.baseFilename = expected
        super().emit(record)


def setup_logging(level: int = logging.INFO) -> None:
    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )

    fmt.converter = time.gmtime

    root = logging.getLogger()
    root.setLevel(level)
    for handler in root.handlers:
        handler.close()
    root.handlers.clear()

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    root.addHandler(console)

    file_handler = HourlyUTCFileHandler(log_dir())
    file_handler.setFormatter(fmt)
    root.addHandler(file_handler)
