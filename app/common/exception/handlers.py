import logging

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class ExceptionHandlers:
    """
    Custom exception handlers.

    Usage:
        app.add_exception_handler(NEED_EXCEPTION, ExceptionHandlers.FOO_ERROR_HANDLER)
    """

    @staticmethod
    def unhandled_exception(request: Request, exc: Exception) -> JSONResponse:  # noqa
        ExceptionHandlers._log_error(exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"detail": str(exc)}),
        )

    @staticmethod
    async def validation_exception(request: Request, exc: ValidationException) -> JSONResponse:  # noqa
        ExceptionHandlers._log_error(exc)
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors()}),
        )

    @staticmethod
    def _log_error(exc: Exception, traceback: bool = True) -> None:
        logger.error(f"{exc=}", exc_info=traceback)
