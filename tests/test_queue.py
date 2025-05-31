import json
from unittest.mock import patch
from popup_pos.backend.services.queue import send_payment_event_to_queue

@patch("pika.BlockingConnection")
def test_send_payment_event_to_queue(mock_connection):
    mock_channel = mock_connection.return_value.channel.return_value

    send_payment_event_to_queue("matti.meikalainen@example.com", 100)

    mock_channel.basic_publish.assert_called_once()
    args, kwargs = mock_channel.basic_publish.call_args
    body = json.loads(kwargs["body"])
    assert body["email"] == "matti.meikalainen@example.com"
    assert body["unikko_points"] == 100