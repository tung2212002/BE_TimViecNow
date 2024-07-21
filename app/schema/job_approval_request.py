from pydantic import BaseModel, ConfigDict, validator
from typing import Optional, List, Any, Union
from datetime import datetime, date
import json
import re

from app.schema.page import Pagination
from app.core import constant
from app.hepler.enum import (
    SalaryType,
    JobType,
    Gender,
    JobApprovalStatus,
)


class JobApprovalRequestBase(BaseModel):
    model_config = ConfigDict(from_attribute=True, extra="ignore")

    job_id: int
    status: Optional[JobApprovalStatus] = None


class JobApprovalRequestUpdate(JobApprovalRequestBase):
    pass


class JobApprovalRequestList(Pagination):
    status: Optional[JobApprovalStatus] = None
    company_id: Optional[int] = None
    business_id: Optional[int] = None


class JobApprovalFilter(Pagination):
    status: Optional[JobApprovalStatus] = None
    job_id: Optional[int] = None


class JobApprovalRequestCreate(BaseModel):
    title: Optional[str] = None
    max_salary: Optional[int] = None
    min_salary: Optional[int] = None
    salary_type: SalaryType = None
    job_description: Optional[str] = None
    job_requirement: Optional[str] = None
    job_benefit: Optional[str] = None
    phone_number_contact: Optional[str] = None
    email_contact: Optional[Any] = None
    full_name_contact: Optional[str] = None
    employment_type: JobType = None
    gender_requirement: Gender = None
    deadline: Optional[date] = None
    is_featured: Optional[bool] = False
    is_highlight: Optional[bool] = False
    is_urgent: Optional[bool] = False
    is_paid_featured: Optional[bool] = False
    is_bg_featured: Optional[bool] = False
    is_job_flash: Optional[bool] = False
    working_time_text: Optional[str] = None
    quantity: Optional[int] = None
    working_times: Optional[Any] = None
    categories: Optional[Any] = None
    work_locations: Optional[Any] = None
    must_have_skills: Optional[Any] = None
    should_have_skills: Optional[Any] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_id: Optional[int] = None

    @validator("working_times")
    def validate_working_times(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, list) else v
        return v

    @validator("categories")
    def validate_categories(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, list) else v
        return v

    @validator("work_locations")
    def validate_work_locations(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, list) else v
        return v

    @validator("must_have_skills")
    def validate_must_have_skills(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, list) else v
        return v

    @validator("should_have_skills")
    def validate_should_have_skills(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, list) else v
        return v

    @validator("email_contact")
    def validate_email_contact(cls, v):
        if isinstance(v, list):
            v = json.dumps(list(set(v)))
        return v


class JobApprovalRequestResponse(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    max_salary: Optional[int] = None
    min_salary: Optional[int] = None
    salary_type: SalaryType = None
    job_description: Optional[str] = None
    job_requirement: Optional[str] = None
    job_benefit: Optional[str] = None
    phone_number_contact: Optional[str] = None
    email_contact: Optional[str] = None
    full_name_contact: Optional[str] = None
    employment_type: JobType = None
    gender_requirement: Gender = None
    deadline: Optional[date] = None
    is_featured: Optional[bool] = None
    is_highlight: Optional[bool] = None
    is_urgent: Optional[bool] = None
    is_paid_featured: Optional[bool] = None
    is_bg_featured: Optional[bool] = None
    is_job_flash: Optional[bool] = None
    working_time_text: Optional[str] = None
    quantity: Optional[int] = None
    working_times: Optional[Any] = None
    categories: Optional[Any] = None
    work_locations: Optional[Any] = None
    must_have_skills: Optional[Any] = None
    should_have_skills: Optional[Any] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_id: Optional[int] = None

    @validator("working_times")
    def validate_working_times(cls, v):
        if v:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("categories")
    def validate_categories(cls, v):
        if v:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("work_locations")
    def validate_locations(cls, v):
        if v:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("must_have_skills")
    def validate_must_have_skills(cls, v):
        if v:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("should_have_skills")
    def validate_should_have_skills(cls, v):
        if v:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("email_contact")
    def validate_email_contact(cls, v):
        return json.loads(v) if isinstance(v, str) else v

    @validator("job_description")
    def validate_job_description(cls, v):
        if v is not None:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("job_requirement")
    def validate_job_requirement(cls, v):
        if v is not None:
            return json.loads(v) if isinstance(v, str) else v
        return v

    @validator("job_benefit")
    def validate_job_benefit(cls, v):
        if v is not None:
            return json.loads(v) if isinstance(v, str) else v
        return v
