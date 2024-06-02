from fastapi import APIRouter

from .products import router

products_router = APIRouter()
products_router.include_router(router, tags=["产品模块"])

__all__ = ["products_router"]