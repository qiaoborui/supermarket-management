from tortoise import fields
from .base import BaseModel, TimestampMixin


class DiscountLevel(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=50, description="等级名称")
    discount = fields.FloatField(description="折扣")

    class Meta:
        table = "discount_level"