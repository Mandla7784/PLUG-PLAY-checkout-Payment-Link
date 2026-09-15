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

    # 1. Checked that the payment link exists
    if not payment_link:
        raise ValueError("Payment link not found")

    # 2. Checked if the payment link is already paid
    if payment_link.status == PaymentLinkStatus.PAID:
        raise ValueError("Payment link has already been paid")

    # 3. Check if the payment link is already expired
    if payment_link.status == PaymentLinkStatus.EXPIRED:
        raise ValueError("Payment link has expired")

    # 4. Checked expiration time
    expires_at = payment_link.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        payment_link.status = PaymentLinkStatus.EXPIRED
        db.commit()

        raise ValueError("Payment link has expired")

    # 5. Make sure payment amount matches the payment link
    if data.amount != payment_link.amount:
        raise ValueError("Payment amount does not match payment link's amount ")

    # 6. Make sure currency matches
    if data.currency != payment_link.currency:
        raise ValueError("Payment currency does not match payment link's currency")

    # 7. Create payment
    payment = Payment(
        payment_link_id=payment_link.id,
        amount=data.amount,
        currency=data.currency,
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment


# payment confirmation 
def confirm_payment(
    db: Session,
    payment_id: str,
) -> Payment:
    payment = (
        db.query(Payment)
        .filter(Payment.id == payment_id)
        .first()
    )