from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from popup_pos.backend.services.adyen import send_payment_request
from popup_pos.utils.utils import calculate_unikko_points
from popup_pos.backend.services.queue import send_payment_event_to_queue

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaymentRequest(BaseModel):
    """
    Data model for a payment request.

    Attributes:
        amount (float): The amount to be charged.
        currency (str): The currency of the transaction.
        email (str): The customer's email address.
    """
    amount: float
    currency: str
    email: str

@app.post("/pay")
async def process_payment(request: PaymentRequest):
    """
    Endpoint for processing a payment.

    This function:
    1. Sends a payment request to the mock Adyen terminal.
    2. Extracts the authorized amount and currency from the response.
    3. Calculates earned Unikko points based on the payment.
    4. Sends a message to RabbitMQ for updating customer.

    Args:
        request (PaymentRequest): The payment request data.

    Returns:
        dict: A success response containing earned Unikko points and status message.

    Raises:
        HTTPException: If any error occurs during payment processing.
    """
    try:
        # Send the payment to the mock Adyen terminal and await response
        print("Received payment request:", request.model_dump())

        result = await send_payment_request(request.amount, request.currency.upper())
        
        # Extract payment result data
        payment_result = result["SaleToPOIResponse"]["PaymentResponse"]["PaymentResult"]
        amount_paid = payment_result["AmountsResp"]["AuthorizedAmount"]
        currency = payment_result["AmountsResp"]["Currency"]

        unikko_points = calculate_unikko_points(amount_paid, currency)

        send_payment_event_to_queue(email=request.email, points=unikko_points)

        return {
            "status": "success",
            "earned_unikko_points": unikko_points,
            "message": "Payment processed. Loyalty sync will follow shortly."
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

