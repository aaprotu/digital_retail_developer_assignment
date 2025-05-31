import pytest
import respx
from httpx import Response
from popup_pos.backend.services.adyen import send_payment_request

@respx.mock
@pytest.mark.asyncio
async def test_send_payment_request():
    adyen_response = {
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

    respx.post("http://adyen:3000/sync").mock(return_value=Response(200, json=adyen_response))
    result = await send_payment_request(100, "EUR")
    assert result["SaleToPOIResponse"]["PaymentResponse"]["PaymentResult"]["AmountsResp"]["AuthorizedAmount"] == 100