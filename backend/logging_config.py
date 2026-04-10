"""
ReliefLink AI — Structured JSON Logging Configuration

Replaces the default stdlib basicConfig with JSON-formatted log output
that can be ingested by Datadog, ELK/Loki, or any log aggregator.
Set LOG_FORMAT=text in .env to revert to plain-text for local dev.
"""
import logging
import os
from pythonjsonlogger import jsonlogger


def configure_logging() -> None:
    """
    Configure application-wide logging.
    - JSON format in production (LOG_FORMAT=json, the default)
    - Human-readable format when LOG_FORMAT=text (local dev convenience)
    """
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)
    log_format = os.getenv("LOG_FORMAT", "json").lower()

    handler = logging.StreamHandler()

    if log_format == "json":
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
            rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    handler.setFormatter(formatter)

    # Configure root logger — affects all child loggers (backend.*)
    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()
    root.addHandler(handler)

    # Silence noisy third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("faiss").setLevel(logging.WARNING)
