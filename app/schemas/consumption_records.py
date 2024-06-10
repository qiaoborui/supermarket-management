from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseConsumptionRecord(BaseModel):
    id: int
    member_id: int
    amount_spent: float
    discount_level_id: int
    actual_amount_spent: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class ConsumptionRecordCreate(BaseModel):
    member_id: int
    amount_spent: float
    discount_level_id: int
    actual_amount_spent: float

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    

class ConsumptionRecordUpdate(BaseModel):
    id: int
    member_id: int
    amount_spent: float
    discount_level_id: int
    actual_amount_spent: float
    