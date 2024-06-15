from typing import List, Optional, Tuple

from tortoise.expressions import Q

from app.core.crud import CRUDBase, Total
from app.models.points_transactions import PointsTransaction
from app.schemas.points_transactions import PointsTransactionCreate, PointsTransactionUpdate
from app.models.members import Member

class PointsTransactionController(CRUDBase[PointsTransaction, PointsTransactionCreate, PointsTransactionUpdate]):
    def __init__(self):
        super().__init__(model=PointsTransaction)

    async def is_exist(self, user_id: int) -> bool:
        return await self.model.filter(user_id=user_id).exists()
    
    async def create(self, obj_in: PointsTransactionCreate) -> PointsTransaction:
        return await super().create(obj_in)
    
    async def update(self, obj_in: PointsTransactionUpdate) -> PointsTransaction:
        return await super().update(id=obj_in.id, obj_in=obj_in)
    
    async def delete(self, id: int) -> None:
        await super().remove(id=id)


points_transaction_controller = PointsTransactionController()