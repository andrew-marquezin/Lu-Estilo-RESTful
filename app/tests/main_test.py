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
        assert len(data["items"]) == 1
        assert data["items"][0]["barcode"] == self.mock["barcode"]

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


class TestClientsRoutes:

    mock = mocks.create_mock_client

    def test_error_create_client(self, client):
        response = client.post(
            "/clients/",
            json={"name": "Invalid Client"}
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_error_read_client(self, client):
        response = client.get("/clients/9999")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"

    def test_error_update_client(self, client):
        response = client.put(
            "/clients/9999",
            json={"name": "Nonexistent Client"}
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert data["detail"] == "Resource not found"

    def test_create_client(self, client):
        response = client.post(
            "/clients/",
            json=self.mock
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["client_id"] == 1

    def test_error_create_client_duplicate_email(self, client):
        response = client.post(
            "/clients/",
            json={
                "name": "Duplicate Email Client",
                "email": self.mock["email"],
                "cpf": "12345678901"
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        error_message = f"Email '{self.mock['email']}' is already registered"
        assert data["detail"] == error_message

    def test_error_create_client_duplicate_cpf(self, client):
        response = client.post(
            "/clients/",
            json={
                "name": "Duplicate CPF Client",
                "email": "duplicate@email.com",
                "cpf": self.mock["cpf"]
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        error_message = f"CPF '{self.mock['cpf']}' is already registered"
        assert data["detail"] == error_message

    def test_read_clients(self, client):
        response = client.get("/clients/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data["items"], list)
        assert len(data["items"]) == 1
        assert data["items"][0]["cpf"] == self.mock["cpf"]

    def test_read_one_client(self, client):
        response = client.get(
            "/clients/1"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cpf"] == self.mock["cpf"]
        assert data["name"] == self.mock["name"]

    def test_update_client(self, client):
        updated_data = dict()
        updated_data["name"] = "Updated Client Name"
        response = client.put(
            "/clients/1",
            json=updated_data
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Client Name"

    def test_delete_client(self, client):
        response = client.delete(
            "/clients/1"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = client.delete(
            "/clients/1"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
