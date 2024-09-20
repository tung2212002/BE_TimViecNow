from fastapi import APIRouter, Depends, Query, Path, Body
from redis.asyncio import Redis

from app.db.base import CurrentSession
from app.core.auth.user_manager_service import user_manager_service
from app.storage.redis import get_redis
from app.core import constant
from app.core.skill.skill_service import skill_service
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType

router = APIRouter()


@router.get("", summary="Get list of skills.")
async def get_list_skill(
    db: CurrentSession,
    redis: Redis = Depends(get_redis),
    skip: int = Query(None, description="The number of skill to skip.", example=0),
    limit: int = Query(
        None, description="The number of skill to return.", example=1000
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
):
    """
    Get list of skills.

    This endpoint allows getting a list of skills.

    Parameters:
    - skip (int): The number of skills to skip.
    - limit (int): The number of skills to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Return:
    - status_code (200): The list of skills has been found successfully.

    """
    args = locals()

    status, status_code, response = await skill_service.get(db, redis, args)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get skill by id.")
async def get_skill_by_id(
    db: CurrentSession,
    id: int = Path(..., description="The skill id."),
):
    """
    Get skill by id.

    This endpoint allows getting a skill by id.

    Parameters:
    - id (int): The skill id.

    Return:
    - status_code (200): The skill has been found successfully.
    - status_code (404): The skill is not found.

    """
    status, status_code, response = await skill_service.get_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a skill.")
async def create_skill(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_superuser),
    data: dict = Body(
        ...,
        description="The data to create a skill.",
        example={
            "name": "",
            "slug": "",
            "description": "",
        },
    ),
):
    """
    Create a skill.

    This endpoint allows creating a new skill.

    Parameters:
    - name (str): The name of the skill.
    - slug (str): The slug of the skill.
    - description (str): The description of the skill.

    Return:
    - status_code (201): The skill has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The skill is already created.

    """
    status, status_code, response = await skill_service.create(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a skill by id.")
async def update_skill(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_superuser),
    id: int = Path(..., description="The skill id."),
    data: dict = Body(
        ...,
        description="The data to update a skill.",
        example={
            "name": "",
            "slug": "",
            "description": "",
        },
    ),
):
    """
    Update a skill by id.

    This endpoint allows updating a skill by id.

    Parameters:
    - id (int): The skill id.
    - name (str): The name of the skill.
    - slug (str): The slug of the skill.
    - description (str): The description of the skill.

    Return:
    - status_code (200): The skill has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (404): The skill is not found.

    """
    status, status_code, response = await skill_service.update(db, id, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a skill by id.")
async def delete_skill_by_id(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_superuser),
    id: int = Path(..., description="The skill id."),
):
    """
    Delete a skill by id.

    This endpoint allows deleting a skill by id.

    Parameters:
    - id (int): The skill id.

    Return:
    - status_code (200): The skill has been deleted successfully.
    - status_code (404): The skill is not found.

    """
    status, status_code, response = await skill_service.delete(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
