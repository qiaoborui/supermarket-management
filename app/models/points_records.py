from tortoise import fields
from .base import BaseModel, TimestampMixin

class PointsRecords(BaseModel, TimestampMixin):
    member = fields.ForeignKeyField("models.Member", related_name="points_records")
    points = fields.FloatField(description="积分")
    class Meta:
        table = "points_records"