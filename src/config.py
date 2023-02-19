from dataclasses import asdict, dataclass
from pydantic import BaseModel
from typing import Optional

class InstanceConfig(BaseModel):
    endpoint: str
    password: str

class WebhookConfig(BaseModel):
    start: Optional[str]
    success: Optional[str]
    failure: Optional[str]

class SyncConfig(BaseModel):
    interval: int
    source: InstanceConfig
    targets: list[InstanceConfig]
    patches: list[str]
    webhook: Optional[WebhookConfig]


def load_config(filename: str) -> SyncConfig:
    with open(filename) as f:
        config = SyncConfig.parse_raw(f.read())
    return config
