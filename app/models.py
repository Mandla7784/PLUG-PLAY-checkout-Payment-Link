import enum
import secrets
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import DateTime, Enum, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

 #maping all the fields in the database to the model class PaymentLink
class PaymentLinkStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    PAID = "PAID"


def generate_token() -> str:
    return secrets.token_urlsafe(12)


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class PaymentLink(Base):
    __tablename__ = "payment_links"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    product_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        default="ZAR",
        nullable=False,
    )

    token: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        index=True,
        nullable=False,
        default=generate_token,
    )

    status: Mapped[PaymentLinkStatus] = mapped_column(
        Enum(PaymentLinkStatus),
        default=PaymentLinkStatus.ACTIVE,
        nullable=False,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
    
    
    #  Payment databasemodel 


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    payment_link_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )