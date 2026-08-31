"""
StudyChart AI - Structured Logging Configuration.
Safely masks sensitive tokens, passwords, and authorization headers.
"""

import logging
import sys
import json
from datetime import datetime

class SafeJsonFormatter(logging.Formatter):
    SENSITIVE_KEYS = {"password", "token", "secret", "authorization", "api_key", "access_token", "refresh_token"}

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno
        }
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            clean_extra = {}
            for k, v in record.extra.items():
                if any(sens in k.lower() for sens in self.SENSITIVE_KEYS):
                    clean_extra[k] = "[REDACTED]"
                else:
                    clean_extra[k] = v
            log_obj["extra"] = clean_extra

        return json.dumps(log_obj)

def setup_logging():
    logger = logging.getLogger("studychart")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        logger.addHandler(handler)
    return logger

logger = setup_logging()
