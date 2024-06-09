from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseDiscountLevel(BaseModel):
    id: int
    name: str
    discount: float
    points_required: float
    created_at: datetime
    updated_at: datetime

class DiscountLevelCreate(BaseModel):
    name: str = Field(..., max_length=50)
    discount: float
    points_required: float

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    

class DiscountLevelUpdate(BaseModel):
    id: int
    name: str
    discount: float
    points_required: float

    def update_dict(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})
    