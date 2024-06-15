import logging

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q

from app.controllers import points_transaction_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.points_transactions import *
from app.models.members import Member

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看积分交易列表")
async def list_points_transaction(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    realname: str = Query("", description="会员名，用于查询"),
    phone: str = Query("", description="手机号，用于查询"),
):
    q = Q()
    if realname:
        q &= Q(realname__contains=realname)
    if phone:
        q &= Q(phone__contains=phone)
    # 先获取 member_id
    member_objs = await Member.filter(q)
    member_ids = [obj.id for obj in member_objs]
    q = Q()
    if member_ids:
        q &= Q(member_id__in=member_ids)
    total, points_transaction_objs = await points_transaction_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict(m2m=True) for obj in points_transaction_objs]
    # 获取积分交易的会员信息
    for obj in data:
        member_obj = await Member.get(id=obj["member_id"])
        obj["realname"] = member_obj.realname
        obj["phone"] = member_obj.phone
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)
