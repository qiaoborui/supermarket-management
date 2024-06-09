from tortoise import fields
from .base import BaseModel, TimestampMixin

class ConsumptionRecords(BaseModel, TimestampMixin):
    member = fields.ForeignKeyField("models.Member", related_name="consumption_records")
    amount = fields.FloatField(description="消费金额")
    discount_level = fields.ForeignKeyField("models.DiscountLevel", related_name="consumption_records")
    real_amount = fields.FloatField(description="实际消费金额")
    class Meta:
        table = "consumption_records"