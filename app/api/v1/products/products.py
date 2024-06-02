import logging
from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q
from app.schemas.base import Success, SuccessExtra

from app.controllers.product import product_controller
from app.schemas.products import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看产品列表")
async def list_product(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="产品名称，用于搜索"),
):
    q = Q()
    if name:
        q &= Q(name__contains=name)
    total, product_objs = await product_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in product_objs]
    print(data)
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看产品")
async def get_product(
    product_id: int = Query(..., description="产品ID"),
):
    product_obj = await product_controller.get(id=product_id)
    product_dict = await product_obj.to_dict()
    return Success(data=product_dict)


@router.post("/create", summary="创建产品")
async def create_product(
    product_in: ProductCreate,
):
    print(product_in)
    product = await product_controller.create(product_in)
    return Success(data=await product.to_dict())


@router.post("/update", summary="更新产品")
async def update_product(
    product_in: ProductUpdate,
):
    product = await product_controller.update(product_in)
    return Success(data=await product.to_dict())


@router.delete("/delete", summary="删除产品")
async def delete_product(
    product_id: int = Query(..., description="产品ID"),
):
    await product_controller.remove(id=product_id)
    return Success(msg="Deleted Success")