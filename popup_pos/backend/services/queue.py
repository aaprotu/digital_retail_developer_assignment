import pika
import json

def send_payment_event_to_queue(email: str, points: int):
    """
    Publishes a customer loyalty update event to the RabbitMQ queue.

    This function connects to RabbitMQ, declares a durable queue named 'payment',
    and sends a JSON-formatted message containing the customer's email and earned
    Unikko points. The message is marked as persistent to ensure it survives broker restarts.

    Args:
        email (str): The customer's email address.
        points (int): The amount of earned Unikko points.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="payment", durable=True)

    message = {
        "event": "customer_update",
        "email": email,
        "unikko_points": points
    }

    channel.basic_publish(
        exchange='',
        routing_key='payment',
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()
