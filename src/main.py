import logging
import time

from config import load_config
from sync import sync

ONE_MINUTE = 60

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

while True:
    cfg = load_config("config.json")

    logging.info("Starting synchronization")
    sync(cfg)

    logging.info("Sleeping for %d minutes", cfg.interval)
    time.sleep(ONE_MINUTE * cfg.interval)
