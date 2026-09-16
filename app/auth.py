from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from .database import get_db
from .models import Merchant
from .services.api_key_service import get_merchant_by_api_key



# for reusable authentication dependency

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=True,
)
def get_current_merchant(
  x_api_key: str = Depends(api_key_header),
    db: Session = Depends(get_db),
) -> Merchant:
    merchant = get_merchant_by_api_key(db, x_api_key)

    if not merchant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return merchant