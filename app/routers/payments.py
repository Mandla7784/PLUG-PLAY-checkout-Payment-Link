from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PaymentCreate, PaymentResponse
from ..services.payment_service import create_payment, confirm_payment


router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Invalid payment details"},
        404: {"description": "Payment link not found"},
        409: {"description": "Payment link has already been paid"},
        410: {"description": "Payment link has expired"},
    },
)
def create_payment_endpoint(
    data: PaymentCreate,
    db: Session = Depends(get_db),
):
    try:
        payment = create_payment(db, data)

    except ValueError as error:
        message = str(error)

        if message == "Payment link not found":
            status_code = status.HTTP_404_NOT_FOUND

        elif message == "Payment link has expired":
            status_code = status.HTTP_410_GONE

        elif message == "Payment link has already been paid":
            status_code = status.HTTP_409_CONFLICT

        else:
            status_code = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=status_code,
            detail=message,
        )

    return PaymentResponse(
        id=payment.id,
        payment_link_id=payment.payment_link_id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status.value,
        created_at=payment.created_at,
    )


@router.post(
    "/{payment_id}/confirm",
    response_model=PaymentResponse,
    responses={
        400: {"description": "Invalid payment confirmation"},
    },
)
def confirm_payment_endpoint(
    payment_id: str,
    db: Session = Depends(get_db),
):
    try:
        payment = confirm_payment(db, payment_id)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    return PaymentResponse(
        id=payment.id,
        payment_link_id=payment.payment_link_id,
        amount=payment.amount,
        currency=payment.currency,
        status=payment.status.value,
        created_at=payment.created_at,
    )