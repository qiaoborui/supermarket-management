import logging
from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q
from app.schemas.base import Success, SuccessExtra

from app.controllers.suppliers import supplier_controller
from app.schemas.suppliers import SupplierCreate, SupplierUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看供应商列表")
async def list_supplier(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    name: str = Query("", description="供应商名称，用于搜索"),
    contact: str = Query("", description="联系人"),
    phone: str = Query("", description="联系电话"),
):
    q = Q()
    if name:
        q &= Q(name__contains=name)
    if contact:
        q &= Q(contact__contains=contact)
    if phone:
        q &= Q(phone__contains=phone)
    total, supplier_objs = await supplier_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict() for obj in supplier_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看供应商")
async def get_supplier(
    supplier_id: int = Query(..., description="供应商ID"),
):
    supplier_obj = await supplier_controller.get(id=supplier_id)
    supplier_dict = await supplier_obj.to_dict()
    return Success(data=supplier_dict)


@router.post("/create", summary="创建供应商")
async def create_supplier(
    supplier_in: SupplierCreate,
):
    print(supplier_in)
    supplier = await supplier_controller.create(supplier_in)
    return Success(data=await supplier.to_dict())


@router.post("/update", summary="更新供应商")
async def update_supplier(
    supplier_in: SupplierUpdate,
):
    supplier = await supplier_controller.update(supplier_in)
    return Success(data=await supplier.to_dict())


@router.delete("/delete", summary="删除供应商")
async def delete_supplier(
    supplier_id: int = Query(..., description="供应商ID"),
):
    supplier = await supplier_controller.delete(id=supplier_id)
    return Success(msg="Deleted Successfully")

