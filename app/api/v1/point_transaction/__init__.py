from fastapi import APIRouter

from .point_transaction import router

point_transaction_router = APIRouter()
point_transaction_router.include_router(router, tags=["积分交易模块"])

__all__ = ["point_transaction_router"]