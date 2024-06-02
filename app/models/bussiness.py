from tortoise import fields
from .base import BaseModel, TimestampMixin


class Supplier(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=50, description="供应商名称")
    phone = fields.CharField(max_length=20, null=True, blank=True, description="联系电话")
    email = fields.CharField(max_length=255, null=True, blank=True,description="邮箱")
    address = fields.CharField(max_length=255, null=True, blank=True, description="地址")
    remark = fields.TextField(null=True, blank=True, description="备注")

    class Meta:
        table = "supplier"

class Product(BaseModel,TimestampMixin):
    # use supplier_id as foreign key
    name = fields.CharField(max_length=50, description="产品名称")
    description = fields.TextField(null=True, description="描述")
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="价格")
    stock = fields.IntField(description="库存")
    supplier = fields.ForeignKeyField("models.Supplier", related_name="products")
    remark = fields.TextField(null=True, description="备注")