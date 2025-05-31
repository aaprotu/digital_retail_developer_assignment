import time
import pika
import json
from popup_pos.backend.services.commerce_layer import CommerceLayerClient

def callback(ch, method, properties, body):
    """
    Callback function for RabbitMQ consumer. This function is triggered when a message
    is received from the "payment" queue. It processes the loyalty points update for a customer.

    Args:
        ch: pika.channel.Channel
            The channel through which the message was received.
        method: pika.spec.Basic.Deliver
            Delivery metadata such as delivery tag.
        properties: pika.spec.BasicProperties
            Message properties.
        body: bytes
            The message payload (JSON-encoded).
    """
    data = json.loads(body)

    email = data["email"]
    points = data["unikko_points"]

    try:
        client = CommerceLayerClient()
        client.sync_unikko_points(email, points)
        # Acknowledge message only after successful processing
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        raise e

def start_consumer(max_retries=10, delay=5):
    """
    Initializes a RabbitMQ connection and starts consuming messages
    from the 'payment' queue using the defined callback.
    """
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            print("✅ Connected to RabbitMQ")
            break
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready (attempt {attempt + 1}/{max_retries})... retrying in {delay}s")
            time.sleep(delay)
    else:
        raise Exception("Failed to connect to RabbitMQ after several retries")
    
    channel = connection.channel()

    # Declare a durable queue (in case the broker restarts)
    channel.queue_declare(queue="payment", durable=True)
    
    # Start consuming messages with the callback function
    channel.basic_consume(queue="payment", on_message_callback=callback)
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()