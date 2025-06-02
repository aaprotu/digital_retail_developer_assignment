from dotenv import load_dotenv
import os
import requests
from popup_pos.utils.utils import determine_loyalty_level

load_dotenv()

# Configuration for Commerce Layer API
AUTH_URL = os.getenv("CL_AUTH_URL")
API_URL = os.getenv("CL_API_URL")
CLIENT_ID = os.getenv("CL_CLIENT_ID")
CLIENT_SECRET = os.getenv("CL_CLIENT_SECRET")
SCOPE = os.getenv("CL_SCOPE")


class CommerceLayerClient:
    """
    A client for interacting with the Commerce Layer API.

    Provides methods for authenticating, retrieving customers by email,
    creating new customers, updating Unikko points, and syncing customer data.
    """

    def __init__(self):
        """
        Initializes the client by obtaining an access token.
        """
        self.token = self.get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/vnd.api+json"
        }

    def get_access_token(self):
        """
        Retrieves an access token using client credentials.

        Returns:
            str: The access token to be used in API calls.

        Raises:
            HTTPError: If the request fails or credentials are invalid.
        """
        response = requests.post(
            AUTH_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def get_customer_by_email(self, email):
        """
        Retrieves a customer from Commerce Layer based on email address.

        Args:
            email (str): The customer's email address.

        Returns:
            dict or None: The customer data if found, otherwise None.
        """
        response = requests.get(
            f"{API_URL}/api/customers",
            headers=self.headers,
            params={"filter[q][email_eq]": email}
        )
        response.raise_for_status()
        data = response.json()
        return data["data"][0] if data["data"] else None
        
    def create_customer(self, email, new_points):
        """
        Creates a new customer in Commerce Layer with initial metadata.

        Args:
            email (str): The customer's email address.
            new_points (int): Amount of earned Unikko points.

        Returns:
            dict: The newly created customer data.
        """
        metadata = {
            "total_unikko_points":new_points,
            "loyalty_level": determine_loyalty_level(new_points)
        }
        payload = {
            "data": {
                "type": "customers",
                "attributes": {
                    "email": email,
                    "metadata": metadata or {}
                }
            }
        }
        response = requests.post(f"{API_URL}/api/customers", headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["data"]
    
    def update_customer_points(self, customer_id, new_points):
        """
        Updates an existing customer's Unikko points and recalculates loyalty level.

        Args:
            customer_id (str): The Commerce Layer customer ID.
            new_points (int): Number of earned Unikko points to add.

        Returns:
            dict: The updated customer data.
        """
        # Get existing customer metadata
        response = requests.get(f"{API_URL}/api/customers/{customer_id}", headers=self.headers)
        response.raise_for_status()
        customer = response.json()["data"]

        current_metadata = customer["attributes"].get("metadata", {})
        existing_points = int(current_metadata.get("total_unikko_points", 0))

        total_points = existing_points + new_points

        level = determine_loyalty_level(total_points)

        # Prepare updated payload
        payload = {
            "data": {
                "id": customer_id,
                "type": "customers",
                "attributes": {
                    "metadata": {
                        "total_unikko_points": total_points,
                        "loyalty_level": level
                    }
                }
            }
        }

        patch_response = requests.patch(
            f"{API_URL}/api/customers/{customer_id}",
            headers=self.headers,
            json=payload
        )
        patch_response.raise_for_status()
        return patch_response.json()["data"]

    def sync_unikko_points(self, customer_email: str, new_points: int):
        """
        Syncs Unikko points to a customer by email.

        If the customer exists, updates their points and recalculates the loyalty level.
        If not, creates a new customer with the given points.

        Args:
            customer_email (str): The customer's email address.
            new_points (int): The amount of Unikko points to add.

        Returns:
            dict: The created or updated customer data.
        """
        customer = self.get_customer_by_email(customer_email)
        if customer:
            return self.update_customer_points(customer["id"], new_points)
        else:
            return self.create_customer(customer_email, new_points)

