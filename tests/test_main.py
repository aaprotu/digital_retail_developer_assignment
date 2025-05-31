from fastapi.testclient import TestClient
from popup_pos.backend.main import app
from unittest.mock import patch

client = TestClient(app)

@patch("popup_pos.backend.main.send_payment_request")
@patch("popup_pos.backend.main.send_payment_event_to_queue")
@patch("popup_pos.backend.main.calculate_unikko_points", return_value=10)
def test_process_payment(mock_points, mock_queue, mock_adyen):
    mock_adyen.return_value = {
        "SaleToPOIResponse": {
            "PaymentResponse": {
                "PaymentResult": {
                    "AmountsResp": {
                        "AuthorizedAmount": 100,
                        "Currency": "EUR"
                    }
                }
            }
        }
    }

    response = client.post("/pay", json={
        "email": "test@example.com",
        "amount": 100,
        "currency": "EUR"
    })

    assert response.status_code == 200
    assert response.json()["earned_unikko_points"] == 10
    mock_queue.assert_called_once()