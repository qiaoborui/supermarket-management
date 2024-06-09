from fastapi import APIRouter

from .discount_level import router

discount_level_router = APIRouter()
discount_level_router.include_router(router, tags=["折扣等级模块"])

__all__ = ["discount_level_router"]