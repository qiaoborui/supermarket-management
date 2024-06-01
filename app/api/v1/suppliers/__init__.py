from fastapi import APIRouter

from .suppliers import router

suppliers_router = APIRouter()
suppliers_router.include_router(router, tags=["供应商模块"])

__all__ = ["suppliers_router"]