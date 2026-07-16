# Функция configure_logging()
import logging
import os
import sys
from datetime import datetime

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["timestamp"] = datetime.utcnow().isoformat()
        log_record["level"] = record.levelname
        log_record["service"] = os.getenv("SERVICE_NAME", "unknown")
        if hasattr(record, "request_id"):
            log_record["request_id"] = record.request_id


class ServiceFilter(logging.Filter):
    """Добавляет service в каждый лог-рекорд"""

    def filter(self, record):
        record.service = os.getenv("SERVICE_NAME", "unknown")
        return True


def configure_logging(service_name: str = None, human_readable: bool = False):
    """Настройка логирования для сервиса"""
    if service_name:
        os.environ["SERVICE_NAME"] = service_name

    handler = logging.StreamHandler(sys.stdout)

    if human_readable or os.getenv("LOG_FORMAT") == "human":
        # 👇 ЧЕЛОВЕЧЕСКИЙ ФОРМАТ
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(service)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        # 👇 JSON-ФОРМАТ
        formatter = CustomJsonFormatter(fmt="%(timestamp)s %(level)s %(service)s %(message)s")

    handler.setFormatter(formatter)
    handler.addFilter(ServiceFilter())  # ← ДОБАВЛЯЕМ ФИЛЬТР!

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    return root_logger
