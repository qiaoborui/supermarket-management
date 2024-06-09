import logging

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q

from app.controllers import member_controller
from app.controllers import user_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.members import *
from app.schemas.users import UserCreate

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看会员列表")
async def list_members(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="会员姓名，用于查询"),
):
    q = Q()
    if name:
        q = Q(name__contains=name)
    total, member_objs = await member_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in member_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看会员")
async def get_member(
    member_id: int = Query(..., description="会员ID"),
):
    member_obj = await member_controller.get(id=member_id)
    return Success(data=await member_obj.to_dict())



@router.post("/create", summary="创建会员")
async def create_member(member_in: MemberCreate):
    if await member_controller.is_exist(user_id=member_in.user_id):
        raise HTTPException(
            status_code=400,
            detail="The member with this user_id already exists in the system.",
        )
    await member_controller.create(obj_in=member_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新会员")
async def update_member(member_in: MemberUpdate):
    await member_controller.update(obj_in=member_in)
    return Success(msg="Updated Successfully")