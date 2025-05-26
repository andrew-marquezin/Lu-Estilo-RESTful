from contextlib import asynccontextmanager

from fastapi import FastAPI

from .db import create_db_and_tables
from .auth.routes import router as auth_router
from .routes import clients, orders, products
from .utils.middleware import AuthMiddleware

description = """
Lu Estilo API is a RESTful API for managing clients, orders, and products.
It provides endpoints for user authentication, client management,
order processing, and product inventory.

## Features
- User authentication with JWT tokens
- Client management (CRUD operations)
- Order processing with item management
- Product inventory management (CRUD operations)

## Authentication
Users can register and log in to obtain JWT
tokens for secure access to the API.
- Register a new user: `/auth/register`
- Log in to obtain a token: `/auth/token`
- Token-based authentication for protected routes
- Admin-only routes for managing clients, orders, and products

## Endpoints
- Clients: `/clients`
  - Create, read, update, and delete clients
  - Search clients by name or email
- Products: `/products`
  - Create, read, update, and delete products
  - Search products by category, price range, and availability
- Orders: `/orders`
  - Create, read, update, and delete orders
- Search products by category, price range, and availability
- Pagination support for large datasets
- Error handling with custom responses
- Swagger UI for API documentation
"""


@asynccontextmanager
async def lifespan(app):
    print("executing pre-startup code")
    create_db_and_tables()
    yield
    # Cleanup code


app = FastAPI(
    title="Lu Estilo API",
    description=description,
    lifespan=lifespan
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Lu Estilo API"}


app.add_middleware(AuthMiddleware)
app.include_router(auth_router, prefix="/auth")
app.include_router(clients.router, prefix="/clients")
app.include_router(orders.router, prefix="/orders")
app.include_router(products.router, prefix="/products")
