from fastapi import FastAPI

from .database import Base, engine
from .routers.payment_links import router as payment_links_router


# Create database tables
Base.metadata.create_all(bind=engine)
