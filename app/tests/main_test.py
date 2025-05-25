from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestProduct:

    def test_create_product():
        response = client.post(
            "/products/",
            json={
                "barcode": "1234567890123",
                "name": "Test Product",
                "description": "A product for testing",
                "category": "Test Category",
                "price": 19.99,
                "stock": 100,
                "available": True,
                "section": "Test Section",
                "expiration_date": None,
                "image_url": None
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_id"] == "1234567890123"

    def test_read_products():
        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        print("🍌", data)
        assert isinstance(data["items"], list)
