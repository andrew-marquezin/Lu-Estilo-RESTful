import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.db import get_session
from . import mocks


@pytest.fixture(scope="session")
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


class TestProductsRoutes:

    mock = mocks.create_mock_product
    duplicated_product = mocks.duplicate_mock_product

    def test_error_create_product(self, client):
        response = client.post(
            "/products/",
            json={"name": "Invalid Product"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_error_read_product(self, client):
        response = client.get("/products/9999999999999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"

    def test_error_update_product(self, client):
        response = client.put(
            "/products/9999999999",
            json={"name": "Nonexistent Product"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"

    def test_create_product(self, client):
        response = client.post(
            "/products/",
            json=self.mock
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["product_id"] == self.mock["barcode"]

    def test_error_create_product_duplicate_barcode(self, client):
        response = client.post(
            "/products/",
            json=self.duplicated_product
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        error_msg = f"Barcode '{self.mock['barcode']}' is already registered"
        assert data["detail"] == error_msg

    def test_read_products(self, client):
        response = client.get("/products/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) == 2
        assert data["items"][1]["barcode"] == self.mock["barcode"]

    def test_read_one_product(self, client):
        response = client.get(
            f"/products/{self.mock['barcode']}"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["barcode"] == self.mock["barcode"]
        assert data["name"] == self.mock["name"]
        assert data["price"] == '19.9900'  # Decimal retorna como string

    def test_update_product(self, client):
        updated_data = dict()
        updated_data["name"] = "Updated Product Name"
        response = client.put(
            f"/products/{self.mock['barcode']}",
            json=updated_data
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Product Name"

    def test_delete_product(self, client):
        response = client.delete(
            f"/products/{self.mock['barcode']}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.delete(
            f"/products/{self.mock['barcode']}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
