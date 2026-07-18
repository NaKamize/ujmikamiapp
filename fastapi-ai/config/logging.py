import logging
import sys

from config.settings import settings

_CONFIGURED = False


def configure_logging() -> None:
    """Idempotent structured logging setup. Safe to call from main.py, ingest.py, and tests."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    )

    root = logging.getLogger()
    root.setLevel(settings.log_level.upper())
    root.handlers = [handler]

    # Quiet noisy third-party loggers unless we're actually debugging them.
    for noisy_logger in ("httpx", "httpcore", "chromadb"):
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)

    _CONFIGURED = True
