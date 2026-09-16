from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.api_key_service import create_merchant

router = APIRouter(
    prefix="/merchants",
    tags=["Merchants"],
)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_merchant_endpoint(
    name: str,
    db: Session = Depends(get_db),
):
    merchant = create_merchant(db, name)

    return {
        "id": merchant.id,
        "name": merchant.name,
        "api_key": merchant.api_key,
        "created_at": merchant.created_at,
    }