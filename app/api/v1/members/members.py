import logging

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q

from app.controllers import member_controller
from app.controllers import user_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.members import *
from app.controllers import discount_level_controller

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看会员列表")
async def list_members(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="会员姓名，用于查询"),
    user_id: int = Query(None, description="用户ID，用于查询"),
):
    q = Q()
    if name:
        q = Q(realname__icontains=name)
    if user_id:
        user_obj = await user_controller.get(id=user_id)
        q = q & Q(user=user_obj)
    total, member_objs = await member_controller.list(page=page, page_size=page_size, search=q)
    for member_obj in member_objs:
        if member_obj.discount_level_id:
            discount_level_obj = await discount_level_controller.get(id=member_obj.discount_level_id)
            member_obj.discount_level_name = discount_level_obj.name
    return SuccessExtra(data=[{
        **await member_obj.to_dict(),
        'discount_level_name': getattr(member_obj, 'discount_level_name', None)
    } for member_obj in member_objs], total=total)

@router.get("/get", summary="查看会员")
async def get_member(
    member_id: int = Query(..., description="会员ID"),
):
    member_obj = await member_controller.get(id=member_id)
    return Success(data=await member_obj.to_dict())



@router.post("/create", summary="创建会员")
async def create_member(member_in: MemberCreate):
    await member_controller.create(obj_in=member_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新会员")
async def update_member(member_in: MemberUpdate):
    await member_controller.update(obj_in=member_in)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除会员")
async def delete_member(member_id: int = Query(..., description="会员ID")):
    await member_controller.delete(id=member_id)
    return Success(msg="Deleted Successfully")