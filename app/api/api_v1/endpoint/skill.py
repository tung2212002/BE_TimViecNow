from fastapi import APIRouter, Depends, Request, Query, Path
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.hepler.response_custom import custom_response_error, custom_response
from app.core import constant
from app.core.skill import service_skill
from app.core.auth.service_business_auth import get_current_superuser

router = APIRouter()


@router.get("", summary="Get list of skills.")
def get_list_skill(
    request: Request,
    skip: int = Query(0, description="The number of skill to skip.", example=0),
    limit: int = Query(
        1000, description="The number of skill to return.", example=1000
    ),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
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
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_skill.get_list_skill(db, args)
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
    status, status_code, response = service_skill.get_skill_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a skill.")
def create_skill(
    name: str = Query(..., description="The name of the skill."),
    slug: str = Query(..., description="The slug of the skill."),
    description: str = Query(None, description="The description of the skill."),
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
    data = {k: v for k, v in locals().items() if k not in ["db"]}
    status, status_code, response = service_skill.create_skill(db, data)
    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
