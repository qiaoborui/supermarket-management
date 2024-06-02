from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class BaseProduct(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    supplier: Optional[int] = None
    remark: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class ProductCreate(BaseModel):
    name: str = Field(example="产品名称")
    description: Optional[str] = Field("",example="描述")
    price: float = Field(...,example="价格")
    stock: int = Field(...,example="库存")
    supplier: int = Field(...,example="供应商ID")
    remark: Optional[str] = Field("",example="备注")
    
    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    
class ProductUpdate(BaseModel):
    id: int
    name: str = Field(example="产品名称")
    description: Optional[str] = Field(example="描述")
    price: float = Field(example="价格")
    stock: int = Field(example="库存")
    supplier: int = Field(example="供应商ID")
    remark: Optional[str] = Field(example="备注")
