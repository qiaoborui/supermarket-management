from tortoise import fields
from .base import BaseModel, TimestampMixin


class Member(BaseModel, TimestampMixin):
    realname = fields.CharField(max_length=50, description="真实姓名")
    points = fields.FloatField(description="积分")
    user = fields.ForeignKeyField("models.User", related_name="members")
    discount_level = fields.ForeignKeyField("models.DiscountLevel", related_name="members")
    class Meta:
        table = "member"