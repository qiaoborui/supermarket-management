from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

class BaseMember(BaseModel):
    id: int
    realname: str
    phone: str
    personal_id: str
    address: str
    points: Optional[float] = 0
    user_id: int
    discount_level_id: Optional[int] = 0
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class MemberCreate(BaseModel):
    realname: str = Field(example="张三")
    phone: str = Field(example="13800138000")
    personal_id: str = Field(example="110101199003070000")
    address: str = Field(example="北京市朝阳区")
    points: Optional[float] = 0
    user_id: Optional[int]
    discount_level_id: Optional[int] = 0

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    

class MemberUpdate(BaseModel):
    id: int
    realname: str
    phone: str
    personal_id: str
    address: str
    points: float
    user_id: int
    discount_level_id: Optional[int] = 0
    
