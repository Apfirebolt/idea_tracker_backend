# Idea Tracker Backend API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Postgres](https://img.shields.io/badge/Postgres-316192?style=for-the-badge&logo=postgresql&logoColor=white)

## Tech Stack

- FastAPI
- PostGres
- Swagger
- Docker

## Introduction

Idea tracker app API which would be used to generate ideas, create tasks associated with those ideas. Additional features like segregation of ideas based on category would also be possible.

## Updates

- Any updates in the project would be added in future

## Screenshots

Any screenshots of the APIs go here

## Deployment using Docker containers

```sh
$ docker-compose up -d --build
$ docker-compose exec web alembic upgrade head
```

## Alembic

```
alembic revision --autogenerate -m "Initial tables"
```

```
alembic upgrade head
```

```
pip install 'pydantic[email]'
```

### Steps to clean database

```
rm alembic/versions*.py
```

This would remove all the migration files inside the Alembic folder. Then, you can delete the tables in the database and start fresh.

```
 alembic revision --autogenerate -m "initial migrations added"
```

### Setting up Logger

This file contains the config related setup for the logger. We can configure log level deciding what kind of messages we want to log.

```Python
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
    logger.setLevel(logging.INFO) # Only log ERROR level and above

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024 * 5,  # 5 MB
        backupCount=5,  # Keep up to 5 old log files
        encoding="utf-8"
    )

    # Define the log format to include object ID, error message, timestamp, level, etc.
    # We'll use %(extra)s to inject the object_id
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - (Object ID: %(object_id)s) - %(message)s"
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
```

Importing the logger in the main file

```Python
from logging_config import setup_logging  # Import your logging setup function
import logging

# 1. Call setup_logging() once at the application's entry point
setup_logging()

# 2. Get the *configured* logger instance by its name
logger = logging.getLogger("idea_app")

app = FastAPI(title="Fast API Ticket Master App",
    docs_url="/docs",
    version="0.0.1")
```


