# This is where i work on generaoing the payment link for the user to pay for the order. I will be using the payment gateway API to generate the payment link and return it to the user.
# calaculating expriation 

#creates the payment link
#saves it to SQLite
#returns the created record

import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from ..models import PaymentLink
from ..schemas import PaymentLinkCreate



#function to create payment link


def create_payment_link(
    db: Session,
    data: PaymentLinkCreate,
       merchant_id: str,
) -> PaymentLink:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=data.expires_in_minutes
    )

    payment_link = PaymentLink(
        merchant_id=merchant_id,
        expires_at=expires_at,
        product_name=data.product_name,
        description=data.description,
        amount=data.amount,
        currency=data.currency,
        token=secrets.token_urlsafe(12),
 
    )

    db.add(payment_link)
    db.commit()
    db.refresh(payment_link)

    return payment_link