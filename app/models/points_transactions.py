from tortoise import fields
from .base import BaseModel, TimestampMixin

class PointsTransaction(BaseModel, TimestampMixin):
    member = fields.ForeignKeyField("models.Member", related_name="points_transactions",on_delete=fields.CASCADE)
    points_changed = fields.FloatField(description="积分")
    transaction_type = fields.CharField(max_length=50, description="交易类型")
    class Meta:
        table = "points_transactions"