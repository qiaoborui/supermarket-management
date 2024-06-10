from fastapi import APIRouter

from .consumption_record import router

consumption_record_router = APIRouter()
consumption_record_router.include_router(router, tags=["消费记录模块"])

__all__ = ["consumption_record_router"]