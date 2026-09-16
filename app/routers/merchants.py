from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.api_key_service import create_merchant

router = APIRouter(
    prefix="/merchants",
    tags=["Merchants"],
)