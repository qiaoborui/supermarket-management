from app.core.crud import CRUDBase
from app.models.bussiness import Product
from app.schemas.products import ProductCreate, ProductUpdate


class ProductController(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def __init__(self):
        super().__init__(model=Product)

    async def create(self, obj_in: ProductCreate) -> Product:
        obj = await super().create(obj_in.create_dict())
        return obj

    async def update(self, obj_in: ProductUpdate) -> Product:
        return await super().update(id=obj_in.id, obj_in=obj_in)
    
    async def delete(self, id: int) -> None:
        obj = await self.get(id=id)
        await obj.delete()

product_controller = ProductController()