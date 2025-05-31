# backend/dependencies.py
from fastapi import HTTPException, status, Depends
import aio_pika
import logging

from main import app # <-- Important: Import your FastAPI app instance

logger = logging.getLogger(__name__)

async def get_rabbitmq_connection_dependency() -> aio_pika.RobustConnection:
    """
    FastAPI dependency to retrieve the RabbitMQ connection from app.state.
    """
    # Check if the connection exists and is not closed
    if not hasattr(app.state, 'rabbitmq_connection') or app.state.rabbitmq_connection.is_closed:
        logger.error("RabbitMQ connection is not available or closed in dependency.")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="RabbitMQ service is unavailable."
        )
    return app.state.rabbitmq_connection