import logging

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q

from app.controllers import discount_level_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.discount_level import *

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看折扣等级列表")
async def list_discount_level(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="等级名称，用于查询"),
):
    q = Q()
    if name:
        q = Q(name__contains=name)
    total, discount_level_objs = await discount_level_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in discount_level_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看折扣等级")
async def get_discount_level(
    discount_level_id: int = Query(..., description="折扣等级ID"),
):
    discount_level_obj = await discount_level_controller.get(id=discount_level_id)
    return Success(data=await discount_level_obj.to_dict())


@router.post("/create", summary="创建折扣等级")
async def create_discount_level(discount_level_in: DiscountLevelCreate):
    if await discount_level_controller.is_exist(name=discount_level_in.name):
        raise HTTPException(
            status_code=400,
            detail="The discount level with this name already exists in the system.",
        )
    await discount_level_controller.create(obj_in=discount_level_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新折扣等级")
async def update_discount_level(discount_level_in: DiscountLevelUpdate):
    await discount_level_controller.update(obj_in=discount_level_in)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除折扣等级")
async def delete_discount_level(
    discount_level_id: int = Query(..., description="折扣等级ID"),
):
    await discount_level_controller.remove(id=discount_level_id)
    return Success(msg="Deleted Success")