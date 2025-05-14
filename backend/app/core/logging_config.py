import logging
from logging.config import dictConfig
from pydantic import BaseModel
from typing import ClassVar, Dict, Any
from app.core.config import settings

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    LOGGER_NAME: str = "udea_logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(name)s | %(module)s:%(lineno)d | %(message)s"
    LOG_LEVEL: str = settings.LOG_LEVEL.upper()

    version: ClassVar[int] = 1
    disable_existing_loggers: ClassVar[bool] = False
    formatters: ClassVar[Dict[str, Dict[str, Any]]] = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: ClassVar[Dict[str, Dict[str, Any]]] = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: ClassVar[Dict[str, Dict[str, Any]]] = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
        "uvicorn.error": {"handlers": ["default"], "level": LOG_LEVEL, "propagate": False},
        "uvicorn.access": {"handlers": ["default"], "level": LOG_LEVEL, "propagate": False},
        "sqlalchemy.engine": {"handlers": ["default"], "level": "WARNING", "propagate": False},
    }

def setup_logging() -> logging.Logger:
    log_config_instance = LogConfig()
    
    config_dict = {
        "version": LogConfig.version,
        "disable_existing_loggers": LogConfig.disable_existing_loggers,
        "formatters": LogConfig.formatters,
        "handlers": LogConfig.handlers,
        "loggers": {
            log_config_instance.LOGGER_NAME: {"handlers": ["default"], "level": log_config_instance.LOG_LEVEL},
            "uvicorn.error": {"handlers": ["default"], "level": log_config_instance.LOG_LEVEL, "propagate": False},
            "uvicorn.access": {"handlers": ["default"], "level": log_config_instance.LOG_LEVEL, "propagate": False},
            "sqlalchemy.engine": {"handlers": ["default"], "level": "WARNING", "propagate": False},
        }
    }
    config_dict["formatters"]["default"]["fmt"] = log_config_instance.LOG_FORMAT

    dictConfig(config_dict)
    current_logger = logging.getLogger(log_config_instance.LOGGER_NAME)
    current_logger.info(f"Logger 	'{log_config_instance.LOGGER_NAME}	' configured with level {log_config_instance.LOG_LEVEL}")
    return current_logger

# Initialize logger instance for use in other modules
logger = setup_logging() # This makes the logger instance available for import

