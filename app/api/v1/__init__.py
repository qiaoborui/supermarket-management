from fastapi import APIRouter

from app.core.dependency import DependPermisson

from .apis import apis_router
from .base import base_router
from .menus import menus_router
from .roles import roles_router
from .users import users_router
from .discount_level import discount_level_router
from .members import members_router
from .consumption_record import consumption_record_router
from .point_transaction import point_transaction_router
from .statistic import statistic_router

v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermisson])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermisson])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermisson])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermisson])
v1_router.include_router(discount_level_router, prefix="/discount_level", dependencies=[DependPermisson])
v1_router.include_router(members_router, prefix="/member", dependencies=[DependPermisson])
v1_router.include_router(consumption_record_router, prefix="/consumption_record", dependencies=[DependPermisson])
v1_router.include_router(point_transaction_router, prefix="/point_transaction", dependencies=[DependPermisson])
v1_router.include_router(statistic_router, prefix="/statistic", dependencies=[DependPermisson])