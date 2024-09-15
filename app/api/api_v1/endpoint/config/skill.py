from fastapi import APIRouter, Depends, Request, Query, Path, Body
from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.db.base import get_db
from app.storage.redis import get_redis
from app.core import constant
from app.core.skill import service_skill
from app.core.auth.service_business_auth import get_current_superuser
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType, SortBy

router = APIRouter()


@router.get("", summary="Get list of skills.")
async def get_list_skill(
    request: Request,
    skip: int = Query(None, description="The number of skill to skip.", example=0),
    limit: int = Query(
        None, description="The number of skill to return.", example=1000
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
    redis: Redis = Depends(get_redis),
    db: Session = Depends(get_db),
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

    status, status_code, response = await service_skill.get(db, redis, args)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get skill by id.")
def get_skill_by_id(
    id: int = Path(..., description="The skill id."),
    db: Session = Depends(get_db),
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
    status, status_code, response = service_skill.get_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a skill.")
def create_skill(
    data: dict = Body(
        ...,
        description="The data to create a skill.",
        example={
            "name": "",
            "slug": "",
            "description": "",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
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
    status, status_code, response = service_skill.create(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a skill by id.")
def update_skill(
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
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
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
    status, status_code, response = service_skill.update(db, id, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a skill by id.")
def delete_skill_by_id(
    id: int = Path(..., description="The skill id."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_superuser),
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
    status, status_code, response = service_skill.delete(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
