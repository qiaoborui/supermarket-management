from tortoise import fields
from .base import BaseModel, TimestampMixin


class Member(BaseModel, TimestampMixin):
    realname = fields.CharField(max_length=50, description="真实姓名")
    phone = fields.CharField(max_length=50, description="手机号")
    personal_id = fields.CharField(max_length=50, description="身份证号")
    address = fields.CharField(max_length=50, description="地址")
    points = fields.FloatField(description="积分")
    user = fields.ForeignKeyField("models.User", related_name="members",on_delete=fields.CASCADE)
    discount_level = fields.ForeignKeyField("models.DiscountLevel", related_name="members",on_delete=fields.RESTRICT)
    class Meta:
        table = "member"