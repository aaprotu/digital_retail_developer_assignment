from unittest.mock import patch, MagicMock
from popup_pos.backend.services.commerce_layer import CommerceLayerClient


@patch.object(CommerceLayerClient, 'get_access_token', return_value="fake-token")
def test_sync_unikko_points_create(mock_token):
    client = CommerceLayerClient()

    with patch.object(client, "get_customer_by_email", return_value=None) as mock_get_customer, \
         patch.object(client, "create_customer", return_value={"id": "created_customer"}) as mock_create, \
         patch.object(client, "update_customer_points") as mock_update:

        result = client.sync_unikko_points("matti.meikalainen@example.com", 100)

        mock_get_customer.assert_called_once_with("matti.meikalainen@example.com")
        mock_create.assert_called_once_with("matti.meikalainen@example.com", 100)
        mock_update.assert_not_called()
        assert result["id"] == "created_customer"


@patch.object(CommerceLayerClient, 'get_access_token', return_value="fake-token")
def test_sync_unikko_points_update(mock_token):
    client = CommerceLayerClient()

    with patch.object(client, "get_customer_by_email", return_value={"id": "existing_id"}) as mock_get_customer, \
         patch.object(client, "update_customer_points", return_value={"id": "updated_customer"}) as mock_update, \
         patch.object(client, "create_customer") as mock_create:

        result = client.sync_unikko_points("existing@example.com", 50)

        mock_get_customer.assert_called_once_with("existing@example.com")
        mock_update.assert_called_once_with("existing_id", 50)
        mock_create.assert_not_called()
        assert result["id"] == "updated_customer"
