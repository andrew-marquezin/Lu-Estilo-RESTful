import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.db import get_session
from . import mocks


@pytest.fixture(scope="class")
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


class TestOrdersRoutes:

    mock = mocks.create_mock_order

    def test_error_create_order(self, client):
        response = client.post(
            "/orders/",
            json={"client_id": 1, "items": [
                {"product_id": "9999999999999", "quantity": 2}]}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        error_msg = "Product with barcode '9999999999999' not found"
        assert data["detail"] == error_msg

    def test_error_invalid_client(self, client):
        response = client.post(
            "/orders/",
            json={"client_id": 9999, "items": [
                {"product_id": "1234567890123", "quantity": 2}]}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_error_invalid_quantity(self, client):
        response = client.post(
            "/orders/",
            json={"client_id": 1, "items": [
                {"product_id": "3210987654321", "quantity": 0}]}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(
            "/orders/",
            json={"client_id": 1, "items": [
                {"product_id": "3210987654321", "quantity": 1000}]}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        error_msg = "Insufficient stock for product '3210987654321'"
        assert data["detail"] == error_msg

    def test_error_read_order(self, client):
        response = client.get("/orders/9999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"

    def test_error_update_order(self, client):
        response = client.put(
            "/orders/9999?status=in_progress"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"

    def test_create_order(self, client):
        response = client.post(
            "/orders/",
            json={"client_id": 1, "items": [
                {"product_id": "3210987654321", "quantity": 2}]}
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["order_id"] == 1

    def test_read_orders(self, client):
        response = client.get("/orders/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) == 1
        assert data["items"][0]["client_id"] == 1

    def test_read_one_order(self, client):
        response = client.get("/orders/1")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["client_id"] == 1
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == "3210987654321"
        assert data["items"][0]["quantity"] == 2

    def test_update_order(self, client):
        response = client.put(
            "/orders/1?status=canceled"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "canceled"

    def test_delete_order(self, client):
        response = client.delete("/orders/1")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.delete("/orders/1")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"
