import httpx
import os
import uuid
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

# Endpoint for the mock Adyen payment terminal API
ADYEN_TERMINAL_URL = os.getenv("ADYEN_TERMINAL_URL")

async def send_payment_request(amount: float, currency: str):
    """
    Sends a payment request to the mock Adyen terminal API.

    This function constructs a SaleToPOIRequest payload with a unique transaction ID and timestamp,
    then sends it to the mock Adyen terminal for processing. It awaits the response and returns it
    as a parsed JSON object.

    Args:
        amount (float): The requested payment amount.
        currency (str): The currency code (e.g., "EUR").

    Returns:
        dict: The parsed JSON response from the Adyen terminal.

    Raises:
        httpx.HTTPStatusError: If the request fails or the response status is not 2xx.
    """
    # Generate a unique transaction ID and timestamp
    transaction_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # Construct the payment request payload
    payload = {
        "SaleToPOIRequest": {
            "MessageHeader": {
                "ProtocolVersion": "3.0",
                "MessageClass": "Service",
                "MessageCategory": "Payment",
                "MessageType": "Request",
                "ServiceID": "1234567890AB",
                "SaleID": "MMKKO-POS-POP-UP",
                "POIID": "V400m-123456789"
            },
            "PaymentRequest": {
                "SaleData": {
                    "SaleToAcquirerData": "tenderOption=ReceiptHandler",
                    "SaleTransactionID": {
                        "TransactionID": transaction_id,
                        "TimeStamp": timestamp
                    }
                },
                "PaymentTransaction": {
                    "AmountsReq": {
                        "Currency": currency,
                        "RequestedAmount": amount
                    }
                }
            }
        }
    }

    # Send the request to the mock terminal and await the response
    async with httpx.AsyncClient(timeout=180.0) as client:
        response = await client.post(ADYEN_TERMINAL_URL, json=payload)
        response.raise_for_status()
        return response.json()
