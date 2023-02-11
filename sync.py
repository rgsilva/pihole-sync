#!/usr/bin/env python3

import io
import tarfile
import tempfile

from config import load_config
from patch import run_patches
from pihole import Instance

cfg = load_config("config.json")

print("* Exporting source instance backup")
primary = Instance(cfg.source)
primary.login()
backup = primary.export()
print("  Backup size:", len(backup), "bytes")

tmp_folder = tempfile.mkdtemp(prefix="pihole-sync")
print()
print("* Extracting to temporary folder:", tmp_folder)
with io.BytesIO(backup) as backup_bytes:
  with tarfile.open(fileobj=backup_bytes) as tar:
    tar.extractall(tmp_folder)

print()
print("* Applying patches")
applied_patches = run_patches(tmp_folder, cfg.patches)
for patch_id in applied_patches:
  print("  Applied:", patch_id)

print()
print("* Recompressing backup")
with io.BytesIO() as patched_bytes:
  with tarfile.open(fileobj=patched_bytes, mode="w:gz") as tar:
    tar.add(tmp_folder, arcname="")
  patched_backup = patched_bytes.getvalue()
print("  Backup size:", len(patched_backup), "bytes")

print()
print("* Uploading to target instances")
for target_cfg in cfg.targets:
  target = Instance(target_cfg)
  target.login()

  print("  Cleaning up target", target_cfg.endpoint)
  target.cleanup()

  print("  Restoring target", target_cfg.endpoint)
  logs = target.restore(patched_backup)
  for log in logs:
    print("   ", log)
  
  print("  Restarting target", target_cfg.endpoint)
  target.restart()
