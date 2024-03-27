from pydantic import BaseModel, Field, validator, ConfigDict
import re
from fastapi import File, UploadFile
from typing import Optional
from datetime import datetime

from app.hepler.enum import Role, SalaryType, JobStatus, JobType
from app.core import constant


class JobBase(BaseModel):
    company_id: int
    title: Optional[str] = None
    max_salary: Optional[int] = 0
    min_salary: Optional[int] = 0
    salary_type: SalaryType = SalaryType.VND
    job_description: str
    job_requirement: str
    job_benefit: str
    address: str
    phone_number_contact: str
    email_contact: str
    full_name_contact: str
    status: JobStatus = JobStatus.PENDING
    employment_type: JobType = JobType
    gender_requirement: Role = Role.OTHER
    deadline: str
    is_featured: bool = False
    is_highlight: bool = False
    is_urgent: bool = False
    is_paid_featured = bool = False
    is_bg_featured = bool = False
    is_vip_employer = bool = False
    is_diamond_employer = bool = False
    is_job_flash = bool = False
    employer_verified = bool = False
    apply_url = Optional[str] = None

    @validator("deadline")
    def validate_deadline(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return v

    @validator("phone_number_contact")
    def validate_phone_number_contact(cls, v):
        if not re.match(constant.REGEX_PHONE_NUMBER, v):
            raise ValueError("Invalid phone number")
        return v

    @validator("email_contact")
    def validate_email_contact(cls, v):
        if not re.match(constant.REGEX_EMAIL, v):
            raise ValueError("Invalid email")
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
    updated_at: str
    created_at: str
    is_new: bool = False
    is_hot: bool = False


class JobGetRequest(BaseModel):
    id: int


class JobCreateRequest(JobBase):
    pass


class JobUpdateRequest(BaseModel):
    id: int
    title: Optional[str] = None
    company_short_description = Optional[str] = None
    cities = Optional[str] = None
    short_cities = Optional[str] = None
    salary: Optional[str] = None
    is_featured: Optional[bool] = None
    is_highlight: Optional[bool] = None
    is_urgent: Optional[bool] = None
    is_paid_featured = Optional[bool] = None
    is_bg_featured = Optional[bool] = None
    is_remote = Optional[bool] = None
    deadline = Optional[str] = None
    is_vip_employer = Optional[bool] = None
    is_diamond_employer = Optional[bool] = None
    is_job_flash = Optional[bool] = None
    employer_verified = Optional[bool] = None
    apply_url = Optional[str] = None
