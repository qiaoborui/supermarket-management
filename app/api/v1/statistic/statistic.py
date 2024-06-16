import logging
from collections import defaultdict
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Query, HTTPException
from tortoise.expressions import Q

from app.controllers import consumption_record_controller, discount_level_controller
from app.controllers import member_controller
from app.schemas.base import Success, SuccessExtra

logger = logging.getLogger(__name__)
router = APIRouter()

from datetime import datetime, timedelta

def generate_date_range(start_date, end_date):
    delta = end_date - start_date
    return [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

class DailyConsumption(BaseModel):
    date: str
    total_amount: float


@router.get("/amount", summary="获取消费总额")
async def get_consumption_amount(
    start_time: Optional[str] = Query(None, description="开始时间"),
    end_time: Optional[str] = Query(None, description="结束时间")
):
    q = Q()
    if start_time:
        q &= Q(created_at__gte=start_time)
    if end_time:
        q &= Q(created_at__lte=end_time)

    # 假设consumption_record_controller.list 返回的是一个包含记录的列表
    total, consumption_record_objs = await consumption_record_controller.list(page=1, page_size=10000, search=q)
    if not consumption_record_objs:
        return SuccessExtra(data=[], total=0, page=1, page_size=10000)

    # 解析时间字符串并生成日期范围
    start_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f").date()
    end_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f").date()
    date_range = generate_date_range(start_date, end_date)
    daily_totals = {date: 0 for date in date_range}

    for record in consumption_record_objs:
        date_str = record.created_at.strftime("%Y-%m-%d")
        daily_totals[date_str] += record.actual_amount_spent

    daily_consumptions = [DailyConsumption(date=date, total_amount=amount) for date, amount in daily_totals.items()]
    # convert to dict
    daily_consumptions = [item.dict() for item in daily_consumptions]

    return Success(data=daily_consumptions)


@router.get("/member", summary="获取各个等级会员的数量")
async def get_member_count():
    # 假设member_controller.list 返回的是一个包含记录的列表
    total, member_objs = await member_controller.list(page=1, page_size=10000)
    if not member_objs:
        return SuccessExtra(data=[], total=0, page=1, page_size=10000)

    # 连接 member 和 discount_level 表 拿到会员等级 
    """
    返回一个列表，列表中的每个元素是一个字典，字典的键是等级名称，值是该等级的会员数量
    """
    total,discount_level_objs = await discount_level_controller.list(page=1, page_size=10000)
    # return  Success(data=[{"level": obj.name, "count": 0} for obj in discount_level_objs])
    print(discount_level_objs)
    discount_levels = {obj.id: obj.name for obj in discount_level_objs}
    member_count = defaultdict(int)
    for member in member_objs:
        member_count[discount_levels[member.discount_level_id]] += 1

    return Success(data=[{"level": level, "count": count} for level, count in member_count.items()])


@router.get("/discount", summary="获取时间段内每天优惠总额") 
async def get_discount_amount(
    start_time: Optional[str] = Query(None, description="开始时间"),
    end_time: Optional[str] = Query(None, description="结束时间")
):
    q = Q()
    if start_time:
        q &= Q(created_at__gte=start_time)
    if end_time:
        q &= Q(created_at__lte=end_time)

    # 假设consumption_record_controller.list 返回的是一个包含记录的列表
    total, consumption_record_objs = await consumption_record_controller.list(page=1, page_size=10000, search=q)
    if not consumption_record_objs:
        return SuccessExtra(data=[], total=0, page=1, page_size=10000)
    
    # 解析时间字符串并生成日期范围
    start_date = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f").date()
    end_date = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f").date()
    date_range = generate_date_range(start_date, end_date)

    for record in consumption_record_objs:
        record.discount_amount = record.amount_spent - record.actual_amount_spent

    daily_discounts = {date: 0 for date in date_range}
    for record in consumption_record_objs:
        date_str = record.created_at.strftime("%Y-%m-%d")
        daily_discounts[date_str] += record.discount_amount
    
    daily_discounts = [DailyConsumption(date=date, total_amount=amount) for date, amount in daily_discounts.items()]
    # convert to dict
    daily_discounts = [item.dict() for item in daily_discounts]

    return Success(data=daily_discounts)