import secrets

from sqlalchemy.orm import Session

from ..models import Merchant


#function to generate api kwy 

def generate_api_key() -> str:
    return f"lsp_live_{secrets.token_urlsafe(32)}"


def create_merchant(
    db: Session,
    name: str,
) -> Merchant:
    merchant = Merchant(
        name=name,
        api_key=generate_api_key(),
    )
    db.add(merchant)
    db.commit()
    db.refresh(merchant)

    return merchant


def get_merchant_by_api_key(
    db: Session,
    api_key: str,
) -> Merchant | None:
    return (
        db.query(Merchant)
        .filter(Merchant.api_key == api_key)
        .first()
    )