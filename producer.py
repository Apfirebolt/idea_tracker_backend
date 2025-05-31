import pika
import time
import json
import sys

# --- Configuration ---
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
EXCHANGE_NAME = 'message_exchange'
EXCHANGE_TYPE = 'topic' # We'll use a topic exchange for flexible routing

def connect_rabbitmq():
    """Establishes a connection to RabbitMQ."""
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()
        print(f"[*] Connected to RabbitMQ at {RABBITMQ_HOST}:{RABBITMQ_PORT}")
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error connecting to RabbitMQ: {e}")
        sys.exit(1)

def declare_exchange(channel):
    """Declares the exchange."""
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type=EXCHANGE_TYPE,
        durable=True # Make the exchange durable so it survives RabbitMQ restarts
    )
    print(f"[*] Exchange '{EXCHANGE_NAME}' ({EXCHANGE_TYPE}) declared.")

def publish_message(channel, routing_key, message_body):
    """Publishes a message to the exchange."""
    properties = pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent # Make message persistent so it survives RabbitMQ restarts
    )
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=json.dumps(message_body), # Send message as JSON string
        properties=properties
    )
    print(f" [x] Sent message to '{routing_key}': {message_body}")

def main():
    connection, channel = connect_rabbitmq()
    declare_exchange(channel)

    try:
        message1 = {
            "event": "user_signup",
            "data": {
                "user_id": 123,
                "username": "john_doe"
            }
        }
        message2 = {
            "event": "user_login",
            "data": {
                "user_id": 123,
                "timestamp": time.time()
            }
        }
        message3 = {
            "event": "user_logout",
            "data": {
                "user_id": 123,
                "timestamp": time.time()
            }
        }

        # Publish these messages with different routing keys, routing keys must begin with 'log.'
        publish_message(channel, 'log.user.signup', message1)
        publish_message(channel, 'log.user.login', message2)
        publish_message(channel, 'log.user.logout', message3)
        print("[*] Messages published successfully. Press Ctrl+C to exit.")

    except KeyboardInterrupt:
        print("\n[*] Exiting producer.")
    finally:
        if connection:
            connection.close()
            print("[*] RabbitMQ connection closed.")

if __name__ == "__main__":
    main()