from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..models import PaymentLink, PaymentLinkStatus
from ..database import get_db
from ..schemas import PaymentLinkCreate, PaymentLinkResponse
from ..services.payment_link_service import create_payment_link



from datetime import datetime, timezone

from ..models import PaymentLink


from ..schemas import (
    PaymentCreate,
    PaymentLinkCreate,
    PaymentLinkResponse,
    PaymentResponse,
)

from ..services.payment_service import create_payment, confirm_payment


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
        
    expires_at = payment_link.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
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
 
#  payment endpoint 

@router.post(
    "/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
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
    "/payments/{payment_id}/confirm",
    response_model=PaymentResponse,
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