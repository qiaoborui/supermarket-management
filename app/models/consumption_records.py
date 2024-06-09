from tortoise import fields
from .base import BaseModel, TimestampMixin

class ConsumptionRecords(BaseModel, TimestampMixin):
    member = fields.ForeignKeyField("models.Member", related_name="consumption_records",on_delete=fields.CASCADE)
    amount_spent = fields.FloatField(description="消费金额")
    discount_level = fields.ForeignKeyField("models.DiscountLevel", related_name="consumption_records",on_delete=fields.RESTRICT)
    actual_amount_spent = fields.FloatField(description="实际消费金额")
    class Meta:
        table = "consumption_records"