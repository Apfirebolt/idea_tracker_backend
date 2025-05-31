import aio_pika
import json
import logging

logger = logging.getLogger(__name__)

RABBITMQ_URL = "amqp://guest:guest@localhost/" # Replace with your RabbitMQ URL
EXCHANGE_NAME = "notifications_exchange"
EXCHANGE_TYPE = "topic"

async def connect_rabbitmq():
    """Establishes a connection to RabbitMQ."""
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        logger.info("Successfully connected to RabbitMQ.")
        return connection
    except Exception as e:
        logger.critical(f"Failed to connect to RabbitMQ: {e}", exc_info=True)
        raise

async def get_rabbitmq_channel():
    """Provides an existing channel or creates a new one."""
    if not hasattr(get_rabbitmq_channel, "_connection") or get_rabbitmq_channel._connection.is_closed:
        get_rabbitmq_channel._connection = await connect_rabbitmq()
    return await get_rabbitmq_channel._connection.channel()


async def publish_notification_message(
    routing_key: str, message_payload: dict
):
    """Publishes a message to the RabbitMQ notification exchange."""
    channel = None
    try:
        channel = await get_rabbitmq_channel()
        exchange = await channel.declare_exchange(
            EXCHANGE_NAME, EXCHANGE_TYPE, durable=True
        )

        await exchange.publish(
            aio_pika.Message(
                body=json.dumps(message_payload).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT, # Make message persistent
            ),
            routing_key=routing_key,
        )
        logger.info(f"Published message to RabbitMQ. Routing Key: {routing_key}, Payload: {message_payload}")
    except Exception as e:
        logger.error(f"Failed to publish message to RabbitMQ: {e}", exc_info=True)
        # Depending on your error handling strategy, you might re-raise or store for retry
    finally:
        if channel:
            # Do not close the channel here if you want to reuse the connection/channel.
            # The robust connection handles channel lifecycle.
            pass