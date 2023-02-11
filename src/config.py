from dataclasses import asdict, dataclass
from pydantic import BaseModel

class InstanceConfig(BaseModel):
    endpoint: str
    password: str

class SyncConfig(BaseModel):
    interval: int
    source: InstanceConfig
    targets: list[InstanceConfig]
    patches: list[str]


def load_config(filename: str) -> SyncConfig:
    with open(filename) as f:
        config = SyncConfig.parse_raw(f.read())
    return config
