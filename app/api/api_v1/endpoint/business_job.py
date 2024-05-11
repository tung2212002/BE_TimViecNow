from fastapi import (
    APIRouter,
    Depends,
    Request,
    Body,
    Query,
    Path,
)
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.auth.service_business_auth import get_current_user, get_current_business
from app.core import constant
from app.core.job import service_job
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import SortBy, OrderType, JobStatus, JobApprovalStatus

router = APIRouter()


@router.get("", summary="Get list of job.")
def get_job(
    request: Request,
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    business_id: int = Query(None, description="The business id.", example=1),
    company_id: int = Query(None, description="The company id.", example=1),
    job_status: JobStatus = Query(
        None, description="The job status.", example=JobStatus.PUBLISHED
    ),
    job_approve_status: JobApprovalStatus = Query(
        None, description="The job approve status.", example=JobApprovalStatus.PENDING
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of job by business.

    This endpoint allows getting a list of job by business.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - business_id (int): The business id.
    - company_id (int): The company id.
    - job_status (str): The job status.
    - job_approve_status (str): The job approve status.
    - campaign_id (int): The campaign id.

    Returns:
    - status_code (200): The list of job has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_job.get_by_business(
        db, {**args}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{job_id}", summary="Get job by id.")
def get_job_by_id(
    job_id: int = Path(
        ...,
        description="The job id.",
        example=1,
    ),
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
    status, status_code, response = service_job.get_by_id_for_business(
        db, job_id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a new job.")
def create_job(
    data: dict = Body(
        ...,
        description="The information of the job.",
        example={
            "title": "Tuyển thực tập sinh Backend FastAPI ",
            "min_salary": 5000000,
            "max_salary": 10000000,
            "salary_type": "vnd",
            "locations": [
                {"province_id": 1, "district_id": 1, "description": "Địa chỉ 1"},
            ],
            "gender_requirement": "other",
            "job_description": "<p>Job description</p>",
            "job_requirement": "<p>Job requirement</p>",
            "job_benefit": "<p>Job benefit</p>",
            "employment_type": "full_time",
            "deadline": "2024-05-03",
            "full_name_contact": "Nhà tuyển dụng",
            "phone_number_contact": "0328493879",
            "email_contact": ["tung@gmail.com"],
            "campaign_id": 1,
            "quantity": 5,
            "categories": [1, 2, 3],
            "working_times": [
                {
                    "date_from": 1,
                    "date_to": 5,
                    "start_time": "08:30",
                    "end_time": "18:00",
                }
            ],
            "working_time_text": "Thời gian làm việc từ 8h30 đến 18h",
            "must_have_skills": [2, 3],
            "should_have_skills": [1, 4],
            "job_position_id": 1,
            "job_experience_id": 2,
            "job_location": "Chuyên viên Nhân sự",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_business),
):
    """
    Create a new job.

    This endpoint allows creating a new job with the provided information.

    Parameters:
    - data (dict): The information of the job.

    Returns:
    - status_code (201): The job has been created successfully.
    - status_code (401): The job is not authorized.
    - status_code (400): The request is invalid.
    - status_code (409): The job is already registered.

    """
    status, status_code, response = service_job.create(db, data, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{job_id}", summary="Update a new job.")
def Update_job(
    job_id: int = Path(
        ...,
        description="The job id.",
        example=1,
    ),
    data: dict = Body(
        ...,
        description="The information of the job.",
        example={
            "title": "Tuyển thực tập sinh Backend FastAPI ",
            "min_salary": 5000000,
            "max_salary": 10000000,
            "salary_type": "vnd",
            "locations": [
                {"province_id": 1, "district_id": 1, "description": "Địa chỉ 1"},
            ],
            "gender_requirement": "other",
            "job_description": "<p>Job description</p>",
            "job_requirement": "<p>Job requirement</p>",
            "job_benefit": "<p>Job benefit</p>",
            "employment_type": "full_time",
            "deadline": "2024-05-03",
            "full_name_contact": "Nhà tuyển dụng",
            "phone_number_contact": "0328493879",
            "email_contact": ["tung@gmail.com"],
            "quantity": 5,
            "categories": [1, 2, 3],
            "working_times": [
                {
                    "date_from": 1,
                    "date_to": 5,
                    "start_time": "08:30",
                    "end_time": "18:00",
                }
            ],
            "working_time_text": "Thời gian làm việc từ 8h30 đến 18h",
            "must_have_skills": [2, 3],
            "should_have_skills": [1, 4],
            "job_position_id": 1,
            "job_experience_id": 2,
            "job_location": "Chuyên viên Nhân sự",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_business),
):
    """
    Update a new job.

    This endpoint allows update a new job with the provided information.

    Parameters:
    - job_id (int): The job id.
    - data (dict): The information of the job.

    Returns:
    - status_code (200): The job has been updated successfully.
    - status_code (401): The job is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The job is not found.

    """
    status, status_code, response = service_job.update(
        db, {**data, "job_id": job_id}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{job_id}", summary="Delete a job.")
def delete_job(
    job_id: int = Path(
        ...,
        description="The job id.",
        example=1,
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a job.

    This endpoint allows delete a job with the provided information.

    Parameters:
    - job_id (int): The job id.

    Returns:
    - status_code (200): The job has been deleted successfully.
    - status_code (401): The job is not authorized.
    - status_code (404): The job is not found.
    - status_code (403): The permission is denied.

    """
    status, status_code, response = service_job.delete(db, job_id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
