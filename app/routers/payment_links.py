from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import PaymentLink, PaymentLinkStatus
from ..database import get_db
from ..schemas import PaymentLinkCreate, PaymentLinkResponse
from ..services.payment_link_service import create_payment_link

from datetime import datetime, timezone

from ..models import PaymentLink
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
    


# endpoint for getting the payment link by token


@router.get(
    "/{token}",
    response_model=PaymentLinkResponse,
)
def get_payment_link(
    token: str,
    db: Session = Depends(get_db),
):
    payment_link = (
        db.query(PaymentLink)
        .filter(PaymentLink.token == token)
        .first()
    )

    if not payment_link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment link not found",
        )
        
        
    if payment_link.expires_at < datetime.now(timezone.utc):
        payment_link.status = PaymentLinkStatus.EXPIRED
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Payment link has expired",
        )
            
        
        

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