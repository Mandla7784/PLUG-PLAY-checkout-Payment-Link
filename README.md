# PLUG-PLAY Checkout Payment Link

A plug-and-play checkout and payment-link API that allows merchants to integrate payment functionality into their applications using secure API keys.

The project is being designed as an API-first payment platform with a focus on secure authentication, checkout sessions, payment processing, idempotency, webhooks, and scalable backend architecture.

## Tech Stack

* **Python** — Backend development
* **FastAPI** — REST API framework
* **PostgreSQL** — Persistent relational database
* **Redis** — Caching, rate limiting, sessions, and idempotency support
* **SQLAlchemy** — Database ORM
* **Alembic** — Database migrations
* **Pytest** — Automated testing
* **Docker** — Containerisation and local development
* **OpenAPI / Swagger** — API documentation

## Basic Concept

Merchants will be able to:

* Create and manage checkout sessions
* Generate payment links
* Authenticate using API keys
* Accept customer payment requests
* Receive payment status updates through webhooks
* Safely retry requests using idempotency keys

The goal is to build a realistic, production-oriented backend that demonstrates modern API design, payment-system concepts, security, reliability, and scalable architecture.
