import logging

from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q

from app.controllers import consumption_record_controller
from app.controllers import member_controller, discount_level_controller
from app.schemas.base import Success, SuccessExtra
from app.schemas.consumption_records import *
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="查看消费记录列表")
async def list_consumption_record(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    member_id: int = Query(None, description="会员ID，用于查询"),
):
    q = Q()
    if member_id:
        q = Q(member_id=member_id)
    total, consumption_record_objs = await consumption_record_controller.list(page=page, page_size=page_size, search=q)
    # 连接查询 member 表 拿到会员名， 连接查询 discount_level 表 拿到折扣等级名
    consumption_record_list = []
    for consumption_record_obj in consumption_record_objs:
        consumption_record_dict = await consumption_record_obj.to_dict()
        member_obj = await member_controller.get(id=consumption_record_dict['member_id'])
        consumption_record_dict['member_name'] = member_obj.realname
        discount_level_obj = await discount_level_controller.get(id=member_obj.discount_level_id)
        consumption_record_dict['discount_level_name'] = discount_level_obj.name
        consumption_record_list.append(consumption_record_dict)
    return SuccessExtra(data=consumption_record_list, total=total)


@router.get("/get", summary="查看消费记录")
async def get_consumption_record(
    consumption_record_id: int = Query(..., description="消费记录ID"),
):
    consumption_record_obj = await consumption_record_controller.get(id=consumption_record_id)
    return Success(data=await consumption_record_obj.to_dict())


@router.post("/create", summary="创建消费记录")
async def create_consumption_record(consumption_record_in: ConsumptionRecordCreate):
    await consumption_record_controller.create(obj_in=consumption_record_in)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新消费记录")
async def update_consumption_record(consumption_record_in: ConsumptionRecordUpdate):
    await consumption_record_controller.update(obj_in=consumption_record_in)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除消费记录")
async def delete_consumption_record(consumption_record_id: int = Query(..., description="消费记录ID")):
    await consumption_record_controller.delete(id=consumption_record_id)
    return Success(msg="Deleted Successfully")