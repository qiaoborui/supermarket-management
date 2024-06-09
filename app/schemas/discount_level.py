from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseDiscountLevel(BaseModel):
    id: int
    name: str
    discount: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DiscountLevelCreate(BaseModel):
    name: str = Field(example="VIP会员")
    discount: float = Field(example=0.9)

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    

class DiscountLevelUpdate(BaseModel):
    id: int
    name: str
    discount: float