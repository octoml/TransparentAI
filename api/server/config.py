import logging
from dataclasses import dataclass
from os import environ
from typing import Dict
from urllib.parse import urlparse

from yaml import SafeLoader, safe_load

_CONFIG_DEFAULT_PATH = "config.yaml"
_CONFIG_ENV_TAG = "!env"

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TargetConfig:
    model: str
    protocol: str
    host: str
    port: int


class Config:
    def __init__(self, kwargs: dict):
        self.targets: Dict[str, TargetConfig] = dict()
        targets_param = kwargs["targets"]
        for target_name, target_config in targets_param.items():
            endpoint = target_config["endpoint"]
            parse_result = urlparse(endpoint)
            logger.info(f"Loaded {target_name}, {endpoint}")
            model_config = TargetConfig(
                target_config["model"],
                parse_result.scheme,
                parse_result.hostname,
                parse_result.port if parse_result.port else 80,
            )
            self.targets[target_name] = model_config


def load_config(config_path: str = _CONFIG_DEFAULT_PATH) -> Config:
    with open(config_path, "r") as config_file:
        SafeLoader.add_constructor(_CONFIG_ENV_TAG, _load_env_property)
        config_kwargs = safe_load(config_file)
        return Config(config_kwargs)


def _load_env_property(loader, node):
    values = loader.construct_scalar(node)
    tags = values.split(" ")
    env_var = tags[0]
    value = environ.get(env_var)
    if value is None:
        default_value = tags[1] if len(tags) > 1 else ""
        value = environ.get(env_var.upper(), default_value)
    return value


if __name__ == "__main__":
    environ.setdefault(
        "TARGET_ENDPOINT_CPU_OPTIMIZED", "http://host1.docker.internal:8001"
    )
    config = load_config()
    print(config)
