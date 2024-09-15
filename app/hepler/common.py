import json
from typing import Any
import datetime


def utc_now() -> datetime.datetime:
    """Return current datetime in UTC timezone now."""
    return datetime.datetime.now(datetime.timezone.utc)


def json_dumps(v: Any, *, default: json.JSONEncoder) -> str:
    """Transforms python-data to JSON-like string.

    Args:
        v (Any): Value that should be dumped into the JSON.
        default (json.JSONEncoder): JSON encoder instance to customize transformation behavior.

    Returns:
        (str): JSON-like string.
    """
    return json.dumps(v, cls=default)


def json_loads(v: str, *, cls: json.JSONDecoder) -> Any:
    """Transform JSON-like string to python-data.

    Args:
        v (str): JSON-like string.
        cls (json.JSONDecoder): JSON decoder instance to customize transformation behavior.

    Returns:
        (Any): Python-data.
    """
    return json.loads(v, cls=cls)


def get_timestamp(v: datetime.datetime) -> float:
    """Extract timestamp from datetime object and round for 3 decimal digits."""
    return round(v.timestamp(), 3)
