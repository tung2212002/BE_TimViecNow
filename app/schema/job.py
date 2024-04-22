from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional, List, Any
from datetime import datetime, date
import json

from app.hepler.enum import (
    Role,
    SalaryType,
    JobStatus,
    JobType,
    Gender,
    JobApprovalStatus,
)
from app.core import constant
from app.schema.page import Pagination


class JobBase(BaseModel):
    campaign_id: Optional[int] = None
    title: Optional[str] = None
    max_salary: Optional[int] = 0
    min_salary: Optional[int] = 0
    salary_type: SalaryType = SalaryType.VND
    job_description: str
    job_requirement: str
    job_benefit: str
    phone_number_contact: str
    full_name_contact: str
    employment_type: JobType = JobType
    gender_requirement: Gender = Gender.OTHER
    deadline: date
    quantity: int = 1
    job_location: str
    working_time_text: Optional[str] = None
    job_position_id: int
    job_experience_id: int

    @validator("phone_number_contact")
    def validate_phone_number_contact(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v

    @validator("full_name_contact")
    def validate_full_name_contact(cls, v):
        if len(v) < 3:
            raise ValueError("Full name must be at least 3 characters")
        elif len(v) > 50:
            raise ValueError("Full name must be at most 50 characters")
        elif not v.replace(" ", "").isalpha():
            raise ValueError("Full name must be alphabet")
        return v

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class JobItemResponse(JobBase):
    id: int
    updated_at: Optional[datetime] = None
    created_at: datetime
    is_featured: bool = False
    is_highlight: bool = False
    is_urgent: bool = False
    is_paid_featured: bool = False
    is_bg_featured: bool = False
    is_vip_employer: bool = False
    is_diamond_employer: bool = False
    is_job_flash: bool = False
    employer_verified: bool = False
    is_new: bool = False
    is_hot: bool = False
    email_contact: Any
    locations: List[object]
    categories: List[object]
    working_times: List[object]
    must_have_skills: List[object]
    should_have_skills: List[object]

    @validator("email_contact")
    def validate_email_contact(cls, v):
        return json.loads(v) if isinstance(v, str) else v


class JobGetRequest(BaseModel):
    id: int


class JobFilterByBusiness(Pagination):
    job_status: Optional[JobStatus] = None
    job_approve_status: Optional[JobApprovalStatus] = None
    business_id: int = None
    company_id: int = None
    campaign_id: int = None


class JobFilterByUser(Pagination):
    job_status: Optional[JobStatus] = None
    job_approve_status: Optional[JobApprovalStatus] = None
    business_id: int = None
    company_id: int = None


class JobCreateRequest(JobBase):
    working_times: List[object] = []
    working_time_text: Optional[str] = None
    categories: List[int]
    locations: List[object]
    email_contact: List[str]
    must_have_skills: List[int]
    should_have_skills: List[int]

    @validator("email_contact")
    def validate_email_contact(cls, v):
        for email in v:
            if not re.match(constant.REGEX_EMAIL, email):
                raise ValueError("Invalid email")
        if isinstance(v, list):
            v = json.dumps(list(set(v)))
            print(type(v))
        return v


class JobCreate(JobBase):
    email_contact: str
    business_id: int
    employer_verified: bool = False


class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    max_salary: Optional[int] = None
    min_salary: Optional[int] = None
    salary_type: SalaryType = None
    job_description: Optional[str] = None
    job_requirement: Optional[str] = None
    job_benefit: Optional[str] = None
    phone_number_contact: Optional[str] = None
    email_contact: Optional[List[str]] = None
    full_name_contact: Optional[str] = None
    employment_type: JobType = None
    gender_requirement: Gender = None
    deadline: Optional[date] = None
    is_featured: Optional[bool] = None
    is_highlight: Optional[bool] = None
    is_urgent: Optional[bool] = None
    is_paid_featured: Optional[bool] = None
    is_bg_featured: Optional[bool] = None
    is_vip_employer: Optional[bool] = None
    is_diamond_employer: Optional[bool] = None
    is_job_flash: Optional[bool] = None
    employer_verified: Optional[bool] = None
    working_time_text: Optional[str] = None
    quantity: Optional[int] = None
    working_times: Optional[List[object]] = None
    categories: Optional[List[int]] = None
    locations: Optional[List[object]] = None
    must_have_skills: Optional[List[int]] = None
    should_have_skills: Optional[List[int]] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_id: Optional[int] = None

    @validator("email_contact")
    def validate_email_contact(cls, v):
        if v:
            for email in v:
                if not re.match(constant.REGEX_EMAIL, email):
                    raise ValueError("Invalid email")
            if isinstance(v, list):
                v = json.dumps(list(set(v)))
        print(type(v))
        print(v)
        return v


class JobUpdate(BaseModel):
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
    is_vip_employer: Optional[bool] = None
    is_diamond_employer: Optional[bool] = None
    is_job_flash: Optional[bool] = None
    employer_verified: Optional[bool] = None
    working_time_text: Optional[str] = None
    quantity: Optional[int] = None
    locations: Optional[List[object]] = None

    @validator("email_contact")
    def validate_email_contact(cls, v):
        if v and isinstance(v, list):
            for email in v:
                if not re.match(constant.REGEX_EMAIL, email):
                    raise ValueError("Invalid email")
            v = json.dumps(list(set(v)))
        return v
