__all__ = (
    "get_logger",
    "LOGGING_CONFIG",
    "setup_logging",
    "SUCCESS",
    "TRACE",
)

import copy
import logging
import logging.config
import typing
import datetime
import functools

from app.core.config import settings
from app.hepler.common import CommonHelper

LOG_FORMAT_AWS = "%(name)s | %(filename)s:%(lineno)s | %(funcName)s | %(levelname)s | %(message)s | (%(asctime)s)"
# Example: app.core.logger | logger.py:123 | get_logger | ERROR | This is an error message | (2021-01-01T00:00:00.000000Z)
# Use this format for AWS CloudWatch Logs
LOG_FORMAT_EXTENDED = (
    "{levelname} | {name} | {filename}:{lineno} | {funcName} | {message} | ({asctime})"
)
# Example: ERROR | app.core.logger | logger.py:123 | get_logger | This is an error message | (2021-01-01T00:00:00.000000Z)
# Use this format for extended logging
LOG_FORMAT = "{levelname} | {message} | ({asctime})"
# Example: ERROR | This is an error message | (2021-01-01T00:00:00.000000Z)
# Use this format for simple logging
LOG_DATE_TIME_FORMAT_ISO_8601 = "%Y-%m-%dT%H:%M:%S.%fZ"
# Example: 2021-01-01T00:00:00.000000Z
LOG_DATE_TIME_FORMAT_WITHOUT_MICROSECONDS = "%Y-%m-%dT%H:%M:%SZ"
# Example: 2021-01-01T00:00:00Z
SUCCESS = 25
TRACE = 5
LOG_DEFAULT_HANDLER_CLASS = "logging.StreamHandler"
logging.addLevelName(SUCCESS, "SUCCESS")
logging.addLevelName(TRACE, "TRACE")


def _get_main_handler(*, is_third_party: bool = True) -> list[str]:
    """Returns main handler depends on Settings."""
    result = ["default_handler"]
    return result


def _get_default_log_format() -> str:
    """Returns log format depends on Settings."""
    return LOG_FORMAT_EXTENDED if settings.LOG_FORMAT_EXTENDED else LOG_FORMAT


def _get_default_formatter() -> dict[str, typing.Any]:
    return {
        "format": _get_default_log_format(),
        "style": "{",
        "datefmt": LOG_DATE_TIME_FORMAT_WITHOUT_MICROSECONDS,
        "validate": True,
    }


LOGGING_CONFIG: dict[str, typing.Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default_formatter": _get_default_formatter(),
        "access_formatter": _get_default_formatter(),
    },
    "handlers": {
        "default_handler": {
            "class": LOG_DEFAULT_HANDLER_CLASS,
            "formatter": "default_formatter",
            "level": TRACE,
        },
    },
    "root": {
        "handlers": _get_main_handler(is_third_party=False),
        "level": settings.LOG_LEVEL,
    },
    "loggers": {
        "asyncio": {
            "level": "WARNING",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "gunicorn": {
            "level": "INFO",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "uvicorn": {
            "level": "INFO",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "casbin": {
            "level": "WARNING",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "watchfiles": {
            "level": "WARNING",
            "handlers": _get_main_handler(),
            "propagate": False,
        },
        "app.debug": {
            "level": "DEBUG",
            "handlers": _get_main_handler(is_third_party=False),
            "propagate": False,
        },
    },
}


class ExtendedLogger(logging.Logger):
    """Custom logger class, with new log methods."""

    def trace(self, msg: str, *args, **kwargs) -> None:
        """Add extra `trace` log method."""
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs, stacklevel=2)

    def success(self, msg: str, *args, **kwargs) -> None:
        """Add extra `success` log method."""
        if self.isEnabledFor(SUCCESS):
            self._log(SUCCESS, msg, args, **kwargs, stacklevel=2)


logging.setLoggerClass(klass=ExtendedLogger)


def setup_logging() -> None:
    """Setup logging from dict configuration object. Setup AWS boto3 logging."""
    logging.config.dictConfig(config=LOGGING_CONFIG)
    # boto3.set_stream_logger(level=Settings.AWS_LOG_LEVEL, format_string=LOG_FORMAT_AWS)


def get_logger(name: str | None = "app.") -> ExtendedLogger:
    """Get logger instance by name.

    Args:
        name (str): Name of logger.

    Returns:
        logging.Logger: Instance of logging.Logger.

    Examples:
        >>>from loggers import get_logger

        >>>logger = get_logger(name=__name__)
        >>>logger.debug(msg="Debug message")
    """
    return logging.getLogger(name=f"app.{name}")


logger = get_logger(name="root")
