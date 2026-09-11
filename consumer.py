# consumer.py
import pika
import time
import json
import sys
import datetime

# --- Configuration ---
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
EXCHANGE_NAME = 'message_exchange' # Name of your exchange
QUEUE_NAME = 'message_queue'     # Name of the queue you bound in the GUI

BINDING_KEY = 'log.user.*' # Example: Change this to 'log.#' if your queue binding is 'log.#' in GUI

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

def setup_consumer(channel):
    """Declares exchange, queue, and binds them (idempotent)."""
    # Declare the exchange (ensure it exists and its type matches producer)
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='topic', # Must match producer's exchange type
        durable=True
    )
    print(f"[*] Exchange '{EXCHANGE_NAME}' declared.")

    # Declare the queue (ensure it exists). If you created it manually, this is idempotent.
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    print(f"[*] Queue '{QUEUE_NAME}' declared.")

    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=QUEUE_NAME,
        routing_key=BINDING_KEY
    )
    print(f"[*] Queue '{QUEUE_NAME}' bound to exchange '{EXCHANGE_NAME}' with binding key '{BINDING_KEY}'.")

def message_callback(ch, method, properties, body):

    received_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        message_data = json.loads(body.decode('utf-8'))
        print(f"[{received_time}] [x] Received from '{method.routing_key}': {message_data}")

        # --- Simulate Processing ---
        # In a real application, you would do your actual work here,
        # e.g., save to DB, send notification, trigger another service.
        processing_time = 0.5 # seconds
        time.sleep(processing_time)
        print(f"[{received_time}] [x] Message processed in {processing_time}s. Acknowledging...")

        # --- ACKNOWLEDGE THE MESSAGE ---
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"[{received_time}] [x] Message with delivery_tag {method.delivery_tag} acknowledged.")

    except json.JSONDecodeError:
        print(f"[{received_time}] [!] Error decoding JSON: {body.decode('utf-8')}")
        # If message is malformed, you might nack it to a dead-letter queue or discard it
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Don't requeue malformed messages
    except Exception as e:
        print(f"[{received_time}] [!] Error processing message: {e}")
        # If processing fails (e.g., DB error), you might nack and requeue,
        # or send to a dead-letter queue.
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) # Requeue for another attempt

def main():
    connection, channel = connect_rabbitmq()
    setup_consumer(channel)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=message_callback,
        auto_ack=False # <--- VERY IMPORTANT: Manual acknowledgment
    )

    print(f"[*] Waiting for messages on queue '{QUEUE_NAME}'. To exit press CTRL+C")
    try:
        while True:
            connection.process_data_events(time_limit=5.0) # Process events for 5 seconds
            print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [*] Consumer idle for 5 seconds, checking again...")

    except KeyboardInterrupt:
        print("\n[*] Exiting consumer.")
    finally:
        if connection:
            connection.close()
            print("[*] RabbitMQ connection closed.")

if __name__ == "__main__":
    main()