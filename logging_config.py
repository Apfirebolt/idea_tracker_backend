# my_fastapi_app/logging_config.py
import sys

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": True,
        },
        "file": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "file_app": {
            "formatter": "file",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "app.log",
            "maxBytes": 10485760, # 10 MB
            "backupCount": 5,
            "level": "INFO",
        },
    },
    "loggers": {
        "my_fastapi_app": { # Top-level logger for your application
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "my_fastapi_app.routers": { # Logger for router modules
            "handlers": ["console", "file_app"],
            "level": "DEBUG", # Maybe more verbose for debugging specific routes
            "propagate": False,
        },
        "my_fastapi_app.services": { # Logger for service modules
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING", # Root logger as a fallback for unconfigured loggers
    },
}