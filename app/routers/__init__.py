from fastapi import APIRouter

from app.routers.wallet import wallet_router

api_router = APIRouter()
api_router.include_router(wallet_router, tags=["Wallet"])
