from fastapi import FastAPI

from .database import Base, engine
from .routers.payment_links import router as payment_links_router