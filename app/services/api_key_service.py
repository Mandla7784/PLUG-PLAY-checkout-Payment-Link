import secrets

from sqlalchemy.orm import Session

from ..models import Merchant


#function to generate api kwy 

def generate_api_key() -> str:
    return f"lsp_live_{secrets.token_urlsafe(32)}"