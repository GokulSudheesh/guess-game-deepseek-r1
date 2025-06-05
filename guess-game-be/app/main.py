from fastapi import FastAPI, Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.main import api_router
from app.core.config import Environment, settings
import logging

app = FastAPI(title=settings.PROJECT_NAME)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception):
    """
    Handles all unhandled exceptions and returns a 500 status code.
    """
    logging.error(f"{exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc) if settings.ENVIRONMENT == Environment.LOCAL else "Something went wrong please try again."})

app.include_router(api_router, prefix=settings.API_V1_STR)
