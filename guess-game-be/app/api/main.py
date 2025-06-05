from fastapi import APIRouter
from app.api.routes import guess

api_router = APIRouter()
api_router.include_router(guess.router)
