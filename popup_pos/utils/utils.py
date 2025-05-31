def calculate_unikko_points(amount: float, currency: str) -> int:
    """
    Calculates Unikko loyalty points based on the paid amount and currency.

    Each currency has a defined rate which determines how many points are earned
    per unit of currency. If the currency is not recognized, the rate defaults to 0.

    Args:
        amount (float): The amount paid by the customer.
        currency (str): The currency in which the payment was made (e.g. "EUR", "SEK").

    Returns:
        int: The amount of Unikko points earned.
    """
    rates = {
        "EUR": 1,
        "SEK": 0.1,
        "NOK": 0.1,
        "DKK": 0.1,
        "GBP": 1,
        "USD": 1,
        "AUD": 1,
        "NZD": 1
    }
    # Get rate for currency (default to 0 if unknown)
    rate = rates.get(currency.upper(), 0)

    return int(amount * rate)


def determine_loyalty_level(points: int) -> str:
    """
    Determines the loyalty level based on the total amount of Unikko points.

    Args:
        points (int): The total amount of Unikko points.

    Returns:
        str: The loyalty level as a string.
    """
    if points >= 1000:
        return "Level 3"
    elif points >= 500:
        return "Level 2"
    elif points >= 1:
        return "Level 1"
    else:
        return "No level"