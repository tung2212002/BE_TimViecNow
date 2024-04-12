from fastapi import APIRouter, Depends, Query, Path, Body, Request
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.core import constant
from app.core.job import service_job
from app.core.auth.service_business_auth import get_current_user, get_current_admin
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("", summary="Get list of job.")
def get_job(
    request: Request,
    skip: int = Query(0, description="The number of users to skip.", example=0),
    limit: int = Query(100, description="The number of users to return.", example=100),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    business_id: int = Query(None, description="The business id.", example=1),
    company_id: int = Query(None, description="The company id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of job.

    This endpoint allows getting a list of job.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - business_id (int): The business id.
    - company_id (int): The company id.

    Returns:
    - status_code (200): The list of job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_job.get_list_job(db, {**args}, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{job_id}", summary="Get job by id.")
def get_job_by_id(
    job_id: int = Path(description="The job id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get job by id.

    This endpoint allows getting a job by id.

    Parameters:
    - job_id (int): The job id.

    Returns:
    - status_code (200): The job has been found successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.get_job_by_id(db, job_id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create job.")
def create_job(
    data: dict = Body(
        ...,
        description="The job data.",
        example={
            "campaign_id": 1,
            "categories": [1, 2],
            "title": "Tuyển dụng nhân viên",
            "deadline": "2024-04-10",
            "email_contact": [],
            "employment_type": "intern",
            "full_name_contact": "Nguyen Van A",
            "gender_requirement": "other",
            "job_benefit": "<p>Benefit</p>",
            "job_description": "<p>Description</p>",
            "job_experience": 1,
            "job_position": "Developer",
            "job_requirement": "<p>Requirement</p>",
            "location": [{"province_id": 1, "district": 1, "description": "Address"}],
            "max_salary": 10000000,
            "min_salary": 5000000,
            "must_have_skills": [1, 2],
            "phone_number_contact": "0123456789",
            "quantity": 1,
            "salary_type": "vnd",
            "should_have_skills": [1, 2],
            "title": "Tuyển dụng nhân viên",
            "working_time": [
                {
                    "date_from": "1",
                    "date_to": "5",
                    "start_time": "08:00",
                    "end_time": "17:00",
                }
            ],
            "working_time_text": "Chủ động thời gian làm việc",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create job.

    This endpoint allows creating a job.

    Parameters:
    - campaign_id (int): The campaign id.
    - categories (List[int]): The list of category id.
    - title (str): The title of the job.
    - deadline (str): The deadline of the job.
    - email_contact (List[str]): The list of email contact.
    - employment_type (str): The employment type.
    - full_name_contact (str): The full name contact.
    - gender_requirement (str): The gender requirement.
    - job_benefit (str): The job benefit.
    - job_description (str): The job description.
    - job_experience (int): The job experience id.
    - job_position (str): The job position.
    - job_requirement (str): The job requirement.
    - location (List[dict]): The list of location.
    - max_salary (int): The max salary.
    - min_salary (int): The min salary.
    - must_have_skills (List[int]): The list of must have skill id.
    - phone_number_contact (str): The phone number contact.
    - quantity (int): The quantity.
    - salary_type (str): The salary type.
    - should_have_skills (List[int]): The list of should have skill id.
    - working_time (List[dict]): The list of working time.
    - working_time_text (str): The working time text.

    Returns:
    - status_code (201): The job has been created successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = service_job.create_job(db, data, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{job_id}", summary="Update job.")
def update_job(
    job_id: int = Path(description="The job id.", example=1),
    data: dict = Body(
        ...,
        description="The job data.",
        example={
            "categories": [1, 2],
            "title": "Tuyển dụng nhân viên (Update)",
            "deadline": "2024-04-10",
            "email_contact": [],
            "employment_type": "intern",
            "full_name_contact": "Nguyen Van A",
            "gender_requirement": "other",
            "job_benefit": "<p>Benefit (Update)</p>",
            "job_description": "<p>Description (Update)</p>",
            "job_experience": 1,
            "job_position": "Developer",
            "job_requirement": "<p>Requirement (Update)</p>",
            "location": [{"province_id": 1, "district": 1, "description": "Address"}],
            "max_salary": 10000000,
            "min_salary": 5000000,
            "must_have_skills": [1, 2],
            "phone_number_contact": "0123456789",
            "quantity": 1,
            "salary_type": "vnd",
            "should_have_skills": [1, 2],
            "title": "Tuyển dụng nhân viên (Update)",
            "working_time": [
                {
                    "date_from": "1",
                    "date_to": "5",
                    "start_time": "08:00",
                    "end_time": "17:00",
                }
            ],
            "working_time_text": "Chủ động thời gian làm việc (Update)",
            "is_featured": True,
            "is_highlight": True,
            "is_urgent": True,
            "is_paid_featured": True,
            "is_bg_featured": True,
            "is_vip_employer": True,
            "is_diamond_employer": True,
            "is_job_flash": True,
            "employer_verified": True,
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update job.

    This endpoint allows updating a job.

    Parameters:
    - job_id (int): The job id.
    - categories (List[int]): The list of category id.
    - title (str): The title of the job.
    - deadline (str): The deadline of the job.
    - email_contact (List[str]): The list of email contact.
    - employment_type (str): The employment type.
    - full_name_contact (str): The full name contact.
    - gender_requirement (str): The gender requirement.
    - job_benefit (str): The job benefit.
    - job_description (str): The job description.
    - job_experience (int): The job experience id.
    - job_position (str): The job position.
    - job_requirement (str): The job requirement.
    - location (List[dict]): The list of location.
    - max_salary (int): The max salary.
    - min_salary (int): The min salary.
    - must_have_skills (List[int]): The list of must have skill id.
    - phone_number_contact (str): The phone number contact.
    - quantity (int): The quantity.
    - salary_type (str): The salary type.
    - should_have_skills (List[int]): The list of should have skill id.
    - working_time (List[dict]): The list of working time.
    - working_time_text (str): The working time text.
    - is_featured (bool): The is featured.
    - is_highlight (bool): The is highlight.
    - is_urgent (bool): The is urgent.
    - is_paid_featured (bool): The is paid featured.
    - is_bg_featured (bool): The is bg featured.
    - is_vip_employer (bool): The is vip employer.
    - is_diamond_employer (bool): The is diamond employer.
    - is_job_flash (bool): The is job flash.
    - employer_verified (bool): The employer verified.

    Returns:
    - status_code (200): The job has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.update_job(
        db, {**data, "id": job_id}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{job_id}", summary="Delete job.")
def delete_job(
    job_id: int = Path(description="The job id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete job.

    This endpoint allows deleting a job.

    Parameters:
    - job_id (int): The job id.

    Returns:
    - status_code (200): The job has been deleted successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.delete_job(db, job_id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
