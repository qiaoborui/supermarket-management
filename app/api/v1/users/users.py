import logging

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from app.controllers.user import UserController
from app.schemas.base import Success, SuccessExtra
from app.schemas.users import *
from app.controllers.dept import dept_controller
from fastapi import File, UploadFile
import csv
import io
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/list", summary="查看用户列表")
async def list_user(
    page: int = Query(1, description="页码"),
    page_size: int = Query(10, description="每页数量"),
    username: str = Query("", description="用户名称，用于搜索"),
    email: str = Query("", description="邮箱地址"),
    dept_id: int = Query(None, description="部门ID")
):
    user_controller = UserController()
    q = Q()
    if username:
        q &= Q(username__contains=username)
    if email:
        q &= Q(email__contains=email)
    if dept_id is not None:
        q &= Q(dept_id=dept_id)
    total, user_objs = await user_controller.list(page=page, page_size=page_size, search=q)
    data = [await obj.to_dict(m2m=True, exclude_fields=["password"]) for obj in user_objs]
    for item in data:
        dept_id = item.pop("dept_id", None)
        item["dept"] = await (await dept_controller.get(id=dept_id)).to_dict() if dept_id else {}

    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="查看用户")
async def get_user(
    user_id: int = Query(..., description="用户ID"),
):
    user_controller = UserController()
    user_obj = await user_controller.get(id=user_id)
    user_dict = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=user_dict)


@router.post("/create", summary="创建用户")
async def create_user(
    user_in: UserCreate,
):
    user_controller = UserController()
    user = await user_controller.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    new_user = await user_controller.create(obj_in=user_in)
    await user_controller.update_roles(new_user, user_in.role_ids)
    return Success(msg="Created Successfully")


@router.post("/update", summary="更新用户")
async def update_user(
    user_in: UserUpdate,
):
    user_controller = UserController()
    user = await user_controller.update(obj_in=user_in)
    await user_controller.update_roles(user, user_in.role_ids)
    return Success(msg="Updated Successfully")


@router.delete("/delete", summary="删除用户")
async def delete_user(
    user_id: int = Query(..., description="用户ID"),
):
    user_controller = UserController()
    await user_controller.remove(id=user_id)
    return Success(msg="Deleted Successfully")

# upload csv file to create users
@router.post("/upload", summary="上传用户")
async def upload_user(
    file: UploadFile = File(...),
):
    user_controller = UserController()
    # use csv package to read the file
    content = await file.read()
    content = content.decode('utf-8')
    f = io.StringIO(content)
    reader = csv.reader(f)
    # skip the header
    next(reader)
    try:
        for row in reader:
            user_in = UserCreate(
                username=row[0],
                email=row[1],
                password=row[2],
                dept_id=int(row[3]) if row[3] else None,
                role_ids=[int(role_id) for role_id in row[4].split(",")] if row[4] else []
            )
            user = await user_controller.get_by_email(user_in.email)
            if user:
                continue
            await user_controller.create(obj_in=user_in)
    except csv.Error as e:
        return HTTPException(status_code=400, detail=f"CSV file error: {str(e)}")

    return Success(msg="Created Successfully")