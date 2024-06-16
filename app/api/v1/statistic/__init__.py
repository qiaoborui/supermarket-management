from fastapi import APIRouter
from .statistic import router

statistic_router = APIRouter()
statistic_router.include_router(router, tags=["统计模块"])

__all__ = ["statistic_router"]
