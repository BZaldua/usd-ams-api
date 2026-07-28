import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import AppModuleException

logger = logging.getLogger("app")


def app_module_exception_handler(request: Request, exc: AppModuleException):
    logger.warning(
        f"Error {exc.status_code} en {request.method} {request.url.path} -> {exc.message}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "error_code": exc.__class__.__name__},
    )


def init_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppModuleException, app_module_exception_handler)
