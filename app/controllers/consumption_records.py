from typing import List, Optional

from app.core.crud import CRUDBase
from app.models.consumption_records import ConsumptionRecords
from app.schemas.consumption_records import ConsumptionRecordCreate, ConsumptionRecordUpdate


class ConsumptionRecordController(CRUDBase[ConsumptionRecords, ConsumptionRecordCreate, ConsumptionRecordUpdate]):
    def __init__(self):
        super().__init__(model=ConsumptionRecords)

    async def is_exist(self, user_id: int) -> bool:
        return await self.model.filter(user_id=user_id).exists()
    
    async def create(self, obj_in: ConsumptionRecordCreate) -> ConsumptionRecords:
        return await super().create(obj_in)
    
    async def update(self, obj_in: ConsumptionRecordUpdate) -> ConsumptionRecords:
        return await super().update(id=obj_in.id, obj_in=obj_in)
    
    async def delete(self, id: int) -> None:
        await super().remove(id=id)


consumption_record_controller = ConsumptionRecordController()