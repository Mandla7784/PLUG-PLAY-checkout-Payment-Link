from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import PaymentLink
from ..services.payment_service import create_payment
from ..schemas import CheckoutPaymentCreate, PaymentCreate

router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"],
)


@router.post(
    "/pay",
    status_code=status.HTTP_201_CREATED,
)
def checkout_payment(
    data: PaymentCreate,
    db: Session = Depends(get_db),
):
    payment_link = (
        db.query(PaymentLink)
        .filter(PaymentLink.token == data.payment_link_token)
        .first()
    )

    if not payment_link:
        raise HTTPException(
            status_code=404,
            detail="Payment link not found",
        )

    # The customer must not be allowed to choose
    # their own amount or currency.
    checkout_data = PaymentCreate(
        idempotency_key=data.idempotency_key,
        payment_link_token=data.payment_link_token,
        amount=payment_link.amount,
        currency=payment_link.currency,
    )

    try:
        payment = create_payment(db, checkout_data)

        return {
            "id": payment.id,
            "payment_link_id": payment.payment_link_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status.value,
            "created_at": payment.created_at,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )