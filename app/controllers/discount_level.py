from typing import List

from app.core.crud import CRUDBase
from app.models.discount_level import DiscountLevel
from app.schemas.discount_level import DiscountLevelCreate, DiscountLevelUpdate


class DiscountLevelController(CRUDBase[DiscountLevel, DiscountLevelCreate, DiscountLevelUpdate]):
    def __init__(self):
        super().__init__(model=DiscountLevel)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()
    
    async def create(self, obj_in: DiscountLevelCreate) -> DiscountLevel:
        return await super().create(obj_in)
    
    async def update(self, obj_in: DiscountLevelUpdate) -> DiscountLevel:
        return await super().update(id=obj_in.id, obj_in=obj_in)
    
    async def delete(self, id: int) -> None:
        await super().delete(id=id)


discount_level_controller = DiscountLevelController()