# logger_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

# Create a logs directory if it doesn't exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, "app_errors.log")


# Configure the logger
def setup_logging():
    logger = logging.getLogger("idea_app")
    logger.setLevel(logging.INFO)  # Only log ERROR level and above

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024 * 5,  # 5 MB
        backupCount=5,  # Keep up to 5 old log files
        encoding="utf-8",
    )

    # Define the log format to include object ID, error message, timestamp, level, etc.
    class OptionalObjectIdFormatter(logging.Formatter):
        def format(self, record):
            object_id = getattr(record, "object_id", None)
            if object_id is not None:
                record.object_id_str = f"(Object ID: {object_id})"
            else:
                record.object_id_str = ""
            return super().format(record)

    formatter = OptionalObjectIdFormatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d %(object_id_str)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(file_handler)

    # Optionally, also log to console for development
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
