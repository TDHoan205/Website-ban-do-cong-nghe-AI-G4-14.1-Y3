from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.routers import (
    auth_router,
    products_router,
    categories_router,
    cart_router,
    orders_router,
    chat_router,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="API for Tech Store with AI Chatbot Support",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(products_router, prefix=settings.API_V1_STR)
    app.include_router(categories_router, prefix=settings.API_V1_STR)
    app.include_router(cart_router, prefix=settings.API_V1_STR)
    app.include_router(orders_router, prefix=settings.API_V1_STR)
    app.include_router(chat_router, prefix=settings.API_V1_STR)

    @app.on_event("startup")
    async def startup_event():
        init_db()

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Tech Store API",
            "version": settings.VERSION,
            "docs": "/docs",
        }

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
