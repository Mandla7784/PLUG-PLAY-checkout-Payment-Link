from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PaymentLinkCreate, PaymentLinkResponse
from ..services.payment_link_service import create_payment_link
