from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

class BasePointsRecords(BaseModel):
    id: int
    member_id: int
    points_changed: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PointsTransactionCreate(BaseModel):
    member_id: int
    points_changed: float

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    
class PointsTransactionUpdate(BaseModel):
    id: int
    member_id: int
    points_changed: float