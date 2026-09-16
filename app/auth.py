from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import Merchant
from .services.api_key_service import get_merchant_by_api_key

def get_current_merchant(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> Merchant:
    merchant = get_merchant_by_api_key(db, x_api_key)

    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return merchant