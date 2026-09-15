from fastapi import FastAPI

from .database import Base, engine
from .routers.payment_links import router as payment_links_router

from .routers.payments import router as payments_router

# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="LinkSecure Pay API",
    description="Secure payment links for buying and selling through WhatsApp.",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "linksecure-pay-api",
    }


app.include_router(
    payment_links_router,
    prefix="/api",
)

app.include_router(
    payments_router,
    prefix="/api",
)