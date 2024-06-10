from typing import List, Optional

from app.core.crud import CRUDBase
from app.models.members import Member
from app.schemas.members import MemberCreate, MemberUpdate

class MemberController(CRUDBase[Member, MemberCreate, MemberUpdate]):
    def __init__(self):
        super().__init__(model=Member)

    async def is_exist(self, user_id: int) -> bool:
        return await self.model.filter(user_id=user_id).exists()
    
    async def create(self, obj_in: MemberCreate) -> Member:
        return await super().create(obj_in)
    
    async def update(self, obj_in: MemberUpdate) -> Member:
        return await super().update(id=obj_in.id, obj_in=obj_in)
    
    async def delete(self, id: int) -> None:
        await super().remove(id=id)


member_controller = MemberController()