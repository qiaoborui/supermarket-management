from fastapi import APIRouter

from .members import router

members_router = APIRouter()
members_router.include_router(router, tags=["会员模块"])

__all__ = ["members_router"]