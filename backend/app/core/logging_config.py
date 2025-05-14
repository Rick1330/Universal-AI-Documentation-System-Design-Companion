import logging
from logging.config import dictConfig
from pydantic import BaseModel
from ..core.config import settings # To get LOG_LEVEL

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    LOGGER_NAME: str = "udea_logger"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(name)s | %(module)s:%(lineno)d | %(message)s"
    LOG_LEVEL: str = settings.LOG_LEVEL.upper() # Get from settings, ensure it's upper case

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
        "uvicorn.error": {"handlers": ["default"], "level": LOG_LEVEL, "propagate": False},
        "uvicorn.access": {"handlers": ["default"], "level": LOG_LEVEL, "propagate": False},
        "sqlalchemy.engine": {"handlers": ["default"], "level": "WARNING", "propagate": False}, # Quieter SQLAlchemy
    }

def setup_logging():
    config = LogConfig()
    dictConfig(config.dict())
    logger = logging.getLogger(config.LOGGER_NAME)
    logger.info(f"Logger 	ható{config.LOGGER_NAME}" configured with level {config.LOG_LEVEL}")
    return logger

# Initialize logger instance for use in other modules
# logger = setup_logging() # Call setup_logging when this module is imported or in main.py

