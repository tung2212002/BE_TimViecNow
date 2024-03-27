from sqlalchemy.orm import Session

from app.core.security import pwd_context
from app.crud import user as userCRUD
from app.core import constant
from app.schema import user as schema_user, page as schema_page
from app.core.auth.service_user_auth import signJWT
from app.hepler.exception_handler import get_message_validation_error


def get_me(current_user):
    if current_user is None:
        return constant.ERROR, 401, "Unauthorized"
    user = schema_user.UserItemResponse(**current_user.__dict__)
    return constant.SUCCESS, 200, user


def get_user_by_email(db: Session, data: dict):
    try:
        user_data = schema_user.UserGetRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    user = userCRUD.get_by_email(db, user_data.email)
    if not user:
        return constant.ERROR, 404, "User not found"
    user = schema_user.UserItemResponse(**user.__dict__)
    return constant.SUCCESS, 200, user


def get_user_by_id(db: Session, id: int):
    user = userCRUD.get(db, id)
    if not user:
        return constant.ERROR, 404, "User not found"
    user = schema_user.UserItemResponse(**user.__dict__)
    return constant.SUCCESS, 200, user


def get_list_user(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    users = userCRUD.get_multi(db, **page.dict())
    if not users:
        return constant.ERROR, 404, "Users not found"
    users = [schema_user.UserItemResponse(**user.__dict__) for user in users]
    return constant.SUCCESS, 200, users


def create_user(db: Session, data: dict):
    try:
        user_data = schema_user.UserCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    user = userCRUD.get_by_email(db, user_data.email)
    if user:
        return constant.ERROR, 409, "Email already registered"

    user = userCRUD.create(db, obj_in=user_data)
    user = schema_user.UserItemResponse(**user.__dict__)

    access_token = signJWT(
        {
            "email": user.email,
            "id": user.id,
            "is_active": user.is_active,
            "role": user.role,
            "type": "access_token",
        }
    )
    refresh_token = signJWT(
        {
            "email": user.email,
            "id": user.id,
            "is_active": user.is_active,
            "role": user.role,
            "type": "refresh_token",
        }
    )
    response = (
        constant.SUCCESS,
        201,
        {"access_token": access_token, "refresh_token": refresh_token, "user": user},
    )
    return response


def update_user(db: Session, id: int, data: dict, current_user):
    if current_user is None or current_user.id != id:
        return constant.ERROR, 401, "Unauthorized"
    try:
        user = schema_user.UserUpdateRequest(**data)
    except Exception as e:
        error = [f'{error["loc"][0]}: {error["msg"]}' for error in e.errors()]
        return constant.ERROR, 400, error

    user_update = userCRUD.update(db=db, db_obj=current_user, obj_in=user)
    user_update = schema_user.UserItemResponse(**user_update.__dict__)
    response = (constant.SUCCESS, 200, user_update)
    return response


def delete_user(db: Session, id: int, current_user):
    if current_user is None:
        return constant.ERROR, 404, "User not found"
    if current_user.id != id:
        return constant.ERROR, 401, "Unauthorized"
    if id is None:
        return constant.ERROR, 400, "Id is required"
    userCRUD.remove(db=db, id=id)
    response = constant.SUCCESS, 200, "User has been deleted successfully"
    return response


def set_user_active(db: Session, id: int, active: bool):
    if id is None:
        return constant.ERROR, 400, "Id is required"
    response = constant.SUCCESS, 200, userCRUD.set_active(db, id, active)
    return response
