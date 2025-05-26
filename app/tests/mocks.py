create_mock_product = {
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

duplicate_mock_product = {
    "barcode": "1234567890123",
    "name": "Duplicate Product",
    "description": "A duplicate product for testing",
    "category": "Test Category",
    "price": 19.99,
    "stock": 50,
    "available": True,
    "section": "Test Section",
    "expiration_date": None,
    "image_url": None
}

create_mock_client = {
    "name": "Test Client",
    "email": "test.client@example.com",
    "cpf": "12345678901",
}

create_mock_order = {
    "client_id": 1,
    "items": [
        {
            "product_id": "3210987654321",
            "quantity": 2
        }
    ]
}
