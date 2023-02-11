#!/usr/bin/env python3

import io
import logging
import shutil
import tarfile
import tempfile

from config import SyncConfig
from patch import run_patches
from pihole import Instance

def sync(cfg: SyncConfig):
    logging.info("Exporting source instance backup")
    primary = Instance(cfg.source)
    primary.login()
    backup = primary.export()
    logging.info("Backup size: %d bytes", len(backup))

    tmp_folder = tempfile.mkdtemp(prefix="pihole-sync")
    logging.info("Extracting to temporary folder: %s", tmp_folder)
    with io.BytesIO(backup) as backup_bytes:
        with tarfile.open(fileobj=backup_bytes) as tar:
            tar.extractall(tmp_folder)

    logging.info("Applying patches")
    applied_patches = run_patches(tmp_folder, cfg.patches)
    for patch_id in applied_patches:
        logging.info("Applied patch: %s", patch_id)

    logging.info("Recompressing backup")
    with io.BytesIO() as patched_bytes:
        with tarfile.open(fileobj=patched_bytes, mode="w:gz") as tar:
            tar.add(tmp_folder, arcname="")
        patched_backup = patched_bytes.getvalue()
    logging.info("Patched backup size: %d bytes", len(patched_backup))

    logging.info("Removing temporary folder: %s", tmp_folder)
    shutil.rmtree(tmp_folder)

    logging.info("Uploading to target instances")
    for target_cfg in cfg.targets:
        target = Instance(target_cfg)
        target.login()

        logging.info("[%s] Cleaning up target", target_cfg.endpoint)
        target.cleanup()

        logging.info("[%s] Restoring backup", target_cfg.endpoint)
        logs = target.restore(patched_backup)
        for log in logs:
            logging.info("[%s]   %s", target_cfg.endpoint, log)
        
        logging.info("[%s] Restarting DNS resolver", target_cfg.endpoint)
        target.restart()

    logging.info("Synchronization completed")