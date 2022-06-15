from dataclasses import dataclass
from os import environ, path
from typing import Dict
from urllib.parse import urlparse

from yaml import SafeLoader, safe_load

_CONFIG_DEFAULT_PATH = "config.yaml"
_CONFIG_ENV_TAG = "!env"


@dataclass(frozen=True)
class Endpoint:
    protocol: str
    host: str
    port: int


class Config:
    def __init__(self, kwargs: dict):
        self.endpoints: Dict[str, Endpoint] = dict()
        endpoint_param = kwargs["endpoints"]
        for endpoint_name, endpoint_url in endpoint_param.items():
            parse_result = urlparse(endpoint_url)
            endpoint = Endpoint(
                parse_result.scheme,
                parse_result.hostname,
                parse_result.port if parse_result.port else 80,
            )
            self.endpoints[endpoint_name] = endpoint


def load_config(config_path: str = _CONFIG_DEFAULT_PATH):
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
    environ.setdefault("MODEL_CPU_OPTIMIZED_URL", "http://host1.docker.internal:8001")
    config = load_config()
