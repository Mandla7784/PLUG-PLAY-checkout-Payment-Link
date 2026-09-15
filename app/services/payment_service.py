from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import Payment, PaymentLink, PaymentLinkStatus
from ..schemas import PaymentCreate
def create_payment(
    db: Session,
    data: PaymentCreate,
) -> Payment:
    payment_link = (
        db.query(PaymentLink)
        .filter(PaymentLink.token == data.payment_link_token)
        .first()
    )

    if not payment_link:
        raise ValueError("Payment link not found")

   # 2. Check if the payment link is already paid
    if payment_link.status == PaymentLinkStatus.PAID:
        raise ValueError("Payment link has already been paid")
    
    
    
    
    # 3. Check if the payment link is already expired
    
    if payment_link.status == PaymentLinkStatus.EXPIRED:
        raise ValueError("Payment link has already been expired")


    payment = Payment(
        payment_link_id=payment_link.id,
        amount=data.amount,
        currency=data.currency,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment