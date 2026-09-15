from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PaymentLinkCreate, PaymentLinkResponse
from ..services.payment_link_service import create_payment_link


router = APIRouter(
    prefix="/payment-links",
    tags=["Payment Links"],
)


@router.post(
    "",
    response_model=PaymentLinkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment_link_endpoint(
    data: PaymentLinkCreate,
    db: Session = Depends(get_db),
):
    payment_link = create_payment_link(db, data)

    return PaymentLinkResponse(
        id=payment_link.id,
        product_name=payment_link.product_name,
        description=payment_link.description,
        amount=payment_link.amount,
        currency=payment_link.currency,
        token=payment_link.token,
        payment_url=f"http://localhost:8000/pay/{payment_link.token}",
        status=payment_link.status.value,
        expires_at=payment_link.expires_at,
        created_at=payment_link.created_at,
    )