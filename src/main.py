import logging
import time
import signal
import sys

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

def run():
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

def terminate(signal, frame):
    print("Terminating...")
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)
    run()