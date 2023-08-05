import logging
from concurrent.futures.thread import ThreadPoolExecutor
from json import dumps
from logging import Handler, LogRecord
from urllib.parse import urljoin

try:
    import loguru
    HAS_LOGURU = True
except ImportError:
    HAS_LOGURU = False

import requests

__all__ = ["QWhaleLogsHandler", "init"]

SERVICE_URL = "https://logs.qwhale.ml/"


class QWhaleLogsHandler(Handler):
    def __init__(self, token: str, batch_site: int = 100, timeout: float = 7.5, **kwargs):
        self.token = token
        self.logs = []
        self.batch = None
        self.batch_size = batch_site
        self.timeout = timeout
        self.executor = ThreadPoolExecutor(max_workers=5)
        super().__init__()

    def __upload(self):
        payload = {"token": self.token}
        try:
            requests.put(
                urljoin(SERVICE_URL, "/api/logs"),
                params=payload,
                data=dumps({"logs": self.batch}),
                timeout=self.timeout,
            )
        except (ConnectionError, ValueError):
            pass

    def emit(self, record: LogRecord) -> None:
        print(record)
        self.logs.append(record.__dict__)
        if len(self.logs) >= self.batch_size:
            self.batch = self.logs.copy()
            self.logs.clear()
            self.executor.submit(self.__upload)

    def flush(self) -> None:
        self.batch = self.logs.copy()
        self.logs.clear()
        self.__upload()

    def close(self) -> None:
        self.flush()
        super().close()
        self.executor.shutdown()


def init(token: str, batch_size: int = 100, **kwargs):
    handler = QWhaleLogsHandler(token, batch_size=batch_size, **kwargs)
    if HAS_LOGURU:
        loguru.logger.add(handler)
    logging.root.addHandler(handler)
    for name, logger in logging.Logger.manager.loggerDict.items():
        print(name)
        if isinstance(logger, logging.Logger):
            logger.addHandler(handler)
