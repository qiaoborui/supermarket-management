from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class BaseSupplier(BaseModel):
    id: int
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    remark: Optional[str] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class SupplierCreate(BaseModel):
    name: str = Field(example="供应商名称")
    phone: Optional[str] = Field(example="联系电话")
    email: Optional[EmailStr] = Field(example="邮箱")
    address: Optional[str] = Field(example="地址")
    remark: Optional[str] = Field(example="备注")

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    
class SupplierUpdate(BaseModel):
    id: int
    name: str = Field(example="供应商名称")
    phone: Optional[str] = Field(example="联系电话")
    email: Optional[EmailStr] = Field(example="邮箱")
    address: Optional[str] = Field(example="地址")
    remark: Optional[str] = Field(example="备注")

