from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

class BasePointsRecords(BaseModel):
    id: int
    member: int
    points: float
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class PointsRecordsCreate(BaseModel):
    member: int
    points: float

    def create_dict(self):
        return self.model_dump(exclude_unset=True)
    
class PointsRecordsUpdate(BaseModel):
    id: int
    member: int
    points: float