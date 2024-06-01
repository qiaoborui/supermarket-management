from datetime import datetime
from typing import Optional

from fastapi.exceptions import HTTPException
from app.core.crud import CRUDBase
from app.models.bussiness import Supplier
from app.schemas.suppliers import SupplierCreate, SupplierUpdate


class SupplierController(CRUDBase[Supplier, SupplierCreate, SupplierUpdate]):
    def __init__(self):
        super().__init__(model=Supplier)

    async def create(self, obj_in: SupplierCreate) -> Supplier:
        obj = await super().create(obj_in.create_dict())
        return obj

    async def update(self, obj_in: SupplierUpdate) -> Supplier:
        return await super().update(id=obj_in.id, obj_in=obj_in)
    
    async def delete(self, id: int) -> None:
        obj = await self.get(id=id)
        await obj.delete()

supplier_controller = SupplierController()