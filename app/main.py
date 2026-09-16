from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers.payment_links import router as payment_links_router

from .routers.payments import router as payments_router
from .routers.merchants import router as merchants_router
# Create database tables
Base.metadata.create_all(bind=engine)
from .routers.checkout import router as checkout_router

app = FastAPI(
    title="LinkSecure Pay API",
    description="Secure payment links for buying and selling through WhatsApp.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "linksecure-pay-api",
    }


app.include_router(
    payment_links_router,
    prefix="/api/v1",
)

app.include_router(
    payments_router,
    prefix="/api/v1",
)

app.include_router(
    merchants_router,
    prefix="/api/v1",
)


app.include_router(
    checkout_router,
    prefix="/api/v1",
)