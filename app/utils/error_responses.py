from fastapi import HTTPException


EXCEPTION_404 = HTTPException(
    status_code=404,
    detail="Resource not found"
)

EXCEPTION_400 = HTTPException(
    status_code=400,
    detail="Bad request"
)

EXCEPTION_500 = HTTPException(
    status_code=500,
    detail="Internal server error"
)

EXCEPTION_401 = HTTPException(
    status_code=401,
    detail="Unauthorized"
)

EXCEPTION_422 = HTTPException(
    status_code=422,
    detail="Invalid input data"
)


def email_already_exists(email: str) -> HTTPException:
    return HTTPException(
        status_code=400,
        detail=f"Email '{email}' is already registered"
    )


def cpf_already_exists(cpf: str) -> HTTPException:
    return HTTPException(
        status_code=400,
        detail=f"CPF '{cpf}' is already registered"
    )


def barcode_already_exists(barcode: str) -> HTTPException:
    return HTTPException(
        status_code=400,
        detail=f"Barcode '{barcode}' is already registered"
    )


def product_not_found(barcode: str) -> HTTPException:
    return HTTPException(
        status_code=404,
        detail=f"Product with barcode '{barcode}' not found"
    )


def insufficient_stock(barcode: str, name: str) -> HTTPException:
    return HTTPException(
        status_code=400,
        detail=f"Insufficient stock for product '{barcode}'"
    )
