import logging
import time

from config import load_config
from sync import sync
from webhook import Webhook

ONE_MINUTE = 60

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.StreamHandler()]
)

while True:
    cfg = load_config("config.json")

    webhook = Webhook(cfg)
    logging.info("Starting synchronization")
    try:
        webhook.start()
        sync(cfg)
        webhook.success()
    except Exception as e:
        logging.error(e)
        webhook.failure()

    logging.info("Sleeping for %d minutes", cfg.interval)
    time.sleep(ONE_MINUTE * cfg.interval)
