from fastapi import FastAPI
from fastapi.exceptions import ValidationException

from app.configs import settings
from app.routers import api_router
from app.common.exception.handlers import ExceptionHandlers


def create_application() -> FastAPI:
    app = FastAPI(
        title="HD Rest API",
        description="HD Rest API",
        version="1.0.0",
        openapi_url=f"{settings.API_STR}/openai.json",
        docs_url=f"{settings.API_STR}/docs",
    )

    # Include routers to application.
    app.include_router(api_router, prefix=settings.API_STR)

    # Add custom exception handlers.
    app.add_exception_handler(Exception, ExceptionHandlers.unhandled_exception)
    app.add_exception_handler(ValidationException, ExceptionHandlers.validation_exception)

    return app
