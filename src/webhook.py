import logging
import requests

from config import SyncConfig

class Webhook:
    def __init__(self, cfg: SyncConfig):
        if cfg.webhook != None:
            self._cfg = cfg.webhook

    def start(self):
        if self._cfg.start != None and len(self._cfg.start) > 0:
            self._get(self._cfg.start)

    def success(self):
        if self._cfg.success != None and len(self._cfg.success) > 0:
            self._get(self._cfg.success)

    def failure(self):
        if self._cfg.failure != None and len(self._cfg.failure) > 0:
            self._get(self._cfg.failure)

    def _get(self, url):
        try:
            resp = requests.get(url)
            logging.info("[Webhook] GET %s returned %d", url, resp.status_code)
        except Exception as e:
            logging.error("[Webhook] GET %s failed: %s", e)
