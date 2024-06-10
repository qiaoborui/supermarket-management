from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise
from app.api import api_router
from app.controllers.user import UserCreate, user_controller
from app.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from app.models.admin import Menu
from app.schemas.menus import MenuType
from app.settings.config import settings
from app.models.admin import Role
from app.models.discount_level import DiscountLevel

from .middlewares import BackGroundTaskMiddleware


def make_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        Middleware(BackGroundTaskMiddleware),
    ]
    return middleware


def register_db(app: FastAPI, db_url=None):
    register_tortoise(
        app,
        # db_url='sqlite://db.sqlite3',
        # modules={'models':['app.models', "aerich.models"]},
        config=settings.TORTOISE_ORM,
        generate_schemas=True,
    )


def register_exceptions(app: FastAPI):
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)


def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


async def init_superuser():
    user = await user_controller.model.exists()
    if not user:
        await user_controller.create(
            UserCreate(
                username="admin",
                email="admin@admin.com",
                password="123456",
                is_active=True,
                is_superuser=True,
            )
        )

async def init_roles():
    await Role.get_or_create(name="普通会员")

async def init_discount():
    discount = await DiscountLevel.exists()
    if not discount:
        await DiscountLevel.create(
            name="普通会员",
            discount=1,
            points_required=0,
        )
        await DiscountLevel.create(
            name="红海会员",
            discount=0.9,
            points_required=500,
        )
        await DiscountLevel.create(
            name="银海会员",
            discount=0.8,
            points_required=1000,
        )
        await DiscountLevel.create(
            name="金海会员",
            discount=0.7,
            points_required=2000,
        )
        await DiscountLevel.create(
            name="黑海会员",
            discount=0.6,
            points_required=5000,
        )

async def createTrigger():
    connection = Tortoise.get_connection("mysql")
    await connection.execute_script(
        """
CREATE TRIGGER IF NOT EXISTS `after_consumption_insert`
AFTER INSERT ON `consumption_records`
FOR EACH ROW
BEGIN
  DECLARE new_points INT;
  SET new_points = NEW.actual_amount_spent;
  UPDATE `member`
    SET `points` = `points` + new_points
    WHERE `id` = NEW.member_id;
  INSERT INTO `points_transactions`(`member_id`, `points_changed`, `transaction_type`)
    VALUES (NEW.member_id, new_points, 'add');
END;
        """)
    await connection.execute_script(
        """
CREATE TRIGGER IF NOT EXISTS `after_consumption_delete`
AFTER DELETE ON `consumption_records`
FOR EACH ROW
BEGIN
  DECLARE lost_points INT;
  SET lost_points = OLD.actual_amount_spent;
  UPDATE `member`
    SET `points` = `points` - lost_points
    WHERE `id` = OLD.member_id;
  INSERT INTO `points_transactions`(`member_id`, `points_changed`, `transaction_type`)
    VALUES (OLD.member_id, -lost_points, 'subtract');
END;
""")
    await connection.execute_script(
        """
CREATE TRIGGER IF NOT EXISTS `after_consumption_update`
AFTER UPDATE ON `consumption_records`
FOR EACH ROW
BEGIN
  DECLARE diff_points INT;
  SET diff_points = NEW.actual_amount_spent - OLD.actual_amount_spent;
  UPDATE `member`
    SET `points` = `points` + diff_points
    WHERE `id` = NEW.member_id;
  IF diff_points != 0 THEN
    INSERT INTO `points_transactions`(`member_id`, `points_changed`, `transaction_type`)
      VALUES (NEW.member_id, diff_points, IF(diff_points > 0, 'add', 'subtract'));
  END IF;
END;
""")
    await connection.execute_script(
        """
CREATE TRIGGER IF NOT EXISTS `after_points_spend`
AFTER UPDATE ON `member`
FOR EACH ROW
BEGIN
  DECLARE point_diff INT;
  SET point_diff = OLD.points - NEW.points;

  IF point_diff > 0 THEN
    INSERT INTO `points_transactions`(`member_id`, `points_changed`, `transaction_type`)
    VALUES (NEW.id, -point_diff, 'spend');
  END IF;
END;
""")
    await connection.execute_script(
        """
SET GLOBAL event_scheduler = ON;
 """)
    await connection.execute_script(
        """
CREATE EVENT IF NOT EXISTS `check_and_update_member_levels`
ON SCHEDULE EVERY 5 MINUTE 
STARTS CURRENT_TIMESTAMP
DO
BEGIN
  UPDATE `member` m
  JOIN `discount_levels` dl
  ON m.`discount_level_id` = dl.`level_id`
  JOIN `discount_levels` dl2
  ON dl2.`points_required` > dl.`points_required` AND m.`points` >= dl2.`points_required`
  SET m.`discount_level_id` = dl2.`level_id`
  WHERE dl2.`points_required` = (
    SELECT MIN(`points_required`)
    FROM `discount_levels`
    WHERE `points_required` > dl.`points_required` AND `points_required` <= m.`points`
  );
END;
""")

async def init_menus():
    menus = await Menu.exists()
    if not menus:
        parent_menu = await Menu.create(
            menu_type=MenuType.CATALOG,
            name="系统管理",
            path="/system",
            order=1,
            parent_id=0,
            icon="carbon:gui-management",
            is_hidden=False,
            component="Layout",
            keepalive=True,
            redirect="/system/user",
        )
        children_menu = [
            Menu(
                menu_type=MenuType.MENU,
                name="用户管理",
                path="user",
                order=1,
                parent_id=parent_menu.id,
                icon="material-symbols:person-outline-rounded",
                is_hidden=False,
                component="/system/user",
                keepalive=True,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="角色管理",
                path="role",
                order=2,
                parent_id=parent_menu.id,
                icon="carbon:user-role",
                is_hidden=False,
                component="/system/role",
                keepalive=True,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="菜单管理",
                path="menu",
                order=3,
                parent_id=parent_menu.id,
                icon="material-symbols:list-alt-outline",
                is_hidden=False,
                component="/system/menu",
                keepalive=True,
            ),
            Menu(
                menu_type=MenuType.MENU,
                name="API管理",
                path="api",
                order=4,
                parent_id=parent_menu.id,
                icon="ant-design:api-outlined",
                is_hidden=False,
                component="/system/api",
                keepalive=True,
            ),
        ]
        await Menu.bulk_create(children_menu)
        parent_menu = await Menu.create(
            menu_type=MenuType.CATALOG,
            name="一级菜单",
            path="/",
            order=2,
            parent_id=0,
            icon="mdi-fan-speed-1",
            is_hidden=False,
            component="Layout",
            keepalive=True,
            redirect="",
        )
        await Menu.create(
            menu_type=MenuType.MENU,
            name="一级菜单",
            path="top-menu",
            order=1,
            parent_id=parent_menu.id,
            icon="mdi-fan-speed-1",
            is_hidden=False,
            component="/top-menu",
            keepalive=True,
        )