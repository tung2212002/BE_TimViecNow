from pydantic import BaseModel, validator, ConfigDict
import re
from typing import Optional, List, Any, Union
from datetime import datetime, date
import json

from app.hepler.enum import (
    SalaryType,
    JobStatus,
    JobType,
    Gender,
    JobApprovalStatus,
    SortByJob,
    OrderType,
    AdminJobApprovalStatus,
)
from app.core import constant


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
    status: JobStatus
    locations: List[object]
    categories: List[object]
    working_times: List[object]
    must_have_skills: List[object]
    should_have_skills: List[object]
    company: object

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


class JobItemResponseGeneral(BaseModel):
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
    status: JobStatus
    campaign_id: Optional[int] = None
    title: Optional[str] = None
    phone_number_contact: str
    full_name_contact: str
    deadline: date


class JobItemResponseUser(BaseModel):
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
    locations: List[object]
    categories: List[object]
    working_times: List[object]
    must_have_skills: List[object]
    should_have_skills: List[object]
    company: object
    title: Optional[str] = None
    max_salary: Optional[int] = 0
    min_salary: Optional[int] = 0
    salary_type: SalaryType = SalaryType.VND
    job_description: str
    job_requirement: str
    job_benefit: str
    employment_type: JobType = JobType
    gender_requirement: Gender = Gender.OTHER
    deadline: date
    quantity: int = 1
    job_location: str
    working_time_text: Optional[str] = None
    job_position_id: int
    job_experience_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")

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


class JobSearchResponseUser(BaseModel):
    id: int
    updated_at: Optional[datetime] = None
    is_featured: bool = False
    is_highlight: bool = False
    is_urgent: bool = False
    is_paid_featured: bool = False
    is_bg_featured: bool = False
    is_vip_employer: bool = False
    is_diamond_employer: bool = False
    is_job_flash: bool = False
    is_new: bool = False
    is_hot: bool = False
    locations: List[object]
    company: object
    title: Optional[str] = None
    max_salary: Optional[int] = 0
    min_salary: Optional[int] = 0
    salary_type: SalaryType = SalaryType.VND
    deadline: date
    quantity: int = 1
    job_position_id: int
    job_experience_id: int

    model_config = ConfigDict(from_attribute=True, extra="ignore")


class JobGetRequest(BaseModel):
    id: int


class PaginationJob(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10
    sort_by: Optional[SortByJob] = SortByJob.CREATED_AT
    order_by: Optional[OrderType] = OrderType.DESC

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("limit")
    def validate_limit(cls, v):
        if v is not None:
            if v < 0 or v > 1000:
                raise ValueError("Invalid limit")
        return v or 10

    @validator("skip")
    def validate_skip(cls, v):
        if v is not None:
            if v < 0:
                raise ValueError("Invalid skip")
        return v or 0

    @validator("sort_by")
    def validate_sort_by(cls, v):
        if v and v == SortByJob.SALARY:
            return "max_salary"
        return v or SortByJob.CREATED_AT

    @validator("order_by")
    def validate_order_by(cls, v):
        return v or OrderType.DESC


class JobFilterByBusiness(PaginationJob):
    job_status: Optional[JobStatus] = None
    job_approve_status: Optional[JobApprovalStatus] = None
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    campaign_id: Optional[int] = None


class JobFilterByUser(PaginationJob):
    job_status: Optional[JobStatus] = None
    job_approve_status: Optional[JobApprovalStatus] = None
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    deadline: Optional[date] = datetime.now().date()
    province_id: Optional[int] = None


class JobCount(BaseModel):
    job_status: Optional[JobStatus] = JobStatus.PUBLISHED
    job_approve_status: Optional[JobApprovalStatus] = JobApprovalStatus.APPROVED
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None
    category_id: Optional[int] = None
    field_id: Optional[int] = None
    employment_type: Optional[JobType] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    salary_type: Optional[SalaryType] = None
    deadline: Optional[date] = datetime.now().date()
    keyword: Optional[str] = None

    model_config = ConfigDict(from_attribute=True, extra="ignore")

    @validator("job_status")
    def validate_job_status(cls, v):
        return v or JobStatus.PUBLISHED

    @validator("job_approve_status")
    def validate_job_approve_status(cls, v):
        return v or JobApprovalStatus.APPROVED

    @validator("deadline")
    def validate_deadline(cls, v):
        return v or datetime.now().date()


class JobSearchByUser(PaginationJob):
    job_status: Optional[JobStatus] = JobStatus.PUBLISHED
    job_approve_status: Optional[JobApprovalStatus] = JobApprovalStatus.APPROVED
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None
    category_id: Optional[int] = None
    field_id: Optional[int] = None
    employment_type: Optional[JobType] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    salary_type: Optional[SalaryType] = None
    deadline: Optional[date] = datetime.now().date()
    keyword: Optional[str] = None
    suggest: Optional[bool] = False

    @validator("deadline")
    def validate_deadline(cls, v):
        return v or datetime.now().date()

    @validator("job_status")
    def validate_job_status(cls, v):
        return v or JobStatus.PUBLISHED

    @validator("job_approve_status")
    def validate_job_approve_status(cls, v):
        return v or JobApprovalStatus.APPROVED


class JobSearchByBusiness(PaginationJob):
    job_status: Optional[JobStatus] = JobStatus.PUBLISHED
    job_approve_status: Optional[JobApprovalStatus] = JobApprovalStatus.APPROVED
    business_id: Optional[int] = None
    company_id: Optional[int] = None
    province_id: Optional[int] = None
    district_id: Optional[int] = None
    category_id: Optional[int] = None
    field_id: Optional[int] = None
    employment_type: Optional[JobType] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    salary_type: Optional[SalaryType] = None
    deadline: Optional[date] = datetime.now().date()
    keyword: Optional[str] = None

    @validator("job_status")
    def validate_deadline(cls, v):
        return v or datetime.now().date()

    @validator("job_status")
    def validate_job_status(cls, v):
        return v or JobStatus.PUBLISHED

    @validator("job_approve_status")
    def validate_job_approve_status(cls, v):
        return v or JobApprovalStatus.APPROVED


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
        return v

    @validator("job_description")
    def validate_job_description(cls, v):
        return json.dumps(v) if isinstance(v, str) else v

    @validator("job_requirement")
    def validate_job_requirement(cls, v):
        return json.dumps(v) if isinstance(v, str) else v

    @validator("job_benefit")
    def validate_job_benefit(cls, v):
        return json.dumps(v) if isinstance(v, str) else v

    @validator("working_times")
    def validate_working_times(cls, v):
        return v or []

    @validator("deadline")
    def validate_deadline(cls, v):
        if v:
            if v < datetime.now().date():
                raise ValueError("Invalid deadline")
        return v


class JobCreate(JobBase):
    email_contact: str
    business_id: int
    campaign_id: int
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
    email_contact: Optional[Any] = None
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
    working_times: Optional[Any] = None
    categories: Optional[Any] = None
    locations: Optional[Any] = None
    must_have_skills: Optional[Any] = None
    should_have_skills: Optional[Any] = None
    job_experience_id: Optional[int] = None
    job_position_id: Optional[int] = None
    job_id: Optional[int] = None

    @validator("email_contact")
    def validate_email_contact(cls, v):
        if v:
            if not isinstance(v, list):
                raise ValueError("Require list email")
            for email in v:
                if not re.match(constant.REGEX_EMAIL, email):
                    raise ValueError("Invalid email")
            if isinstance(v, list):
                v = json.dumps(list(set(v)))
        return v

    @validator("job_description")
    def validate_job_description(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, str) else v
        return v

    @validator("job_requirement")
    def validate_job_requirement(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, str) else v
        return v

    @validator("job_benefit")
    def validate_job_benefit(cls, v):
        if v:
            return json.dumps(v) if isinstance(v, str) else v
        return v

    @validator("working_times")
    def validate_working_times(cls, v):
        if not isinstance(v, list):
            raise ValueError("Require list working times")
        for item in v:
            if not isinstance(item, dict):
                raise ValueError("Require object working times")
        return v

    @validator("categories")
    def validate_categories(cls, v):
        if not isinstance(v, list):
            raise ValueError("Require list categories")
        for item in v:
            if not isinstance(item, int):
                raise ValueError("Require int categories")
        return v

    @validator("locations")
    def validate_locations(cls, v):
        if not isinstance(v, list):
            raise ValueError("Require list locations")
        for item in v:
            if not isinstance(item, dict):
                raise ValueError("Require object locations")
        return v or []

    @validator("must_have_skills")
    def validate_must_have_skills(cls, v):
        if not isinstance(v, list):
            raise ValueError("Require list must have skills")
        for item in v:
            if not isinstance(item, int):
                raise ValueError("Require int must have skills")
        return v

    @validator("should_have_skills")
    def validate_should_have_skills(cls, v):
        if not isinstance(v, list):
            raise ValueError("Require list should have skills")
        for item in v:
            if not isinstance(item, int):
                raise ValueError("Require int should have skills")
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


class JobApproveRequest(BaseModel):
    job_approval_request_id: int
    status: AdminJobApprovalStatus
    reason: Optional[str] = None

    @validator("status")
    def validate_status(cls, v):
        if v not in [AdminJobApprovalStatus.APPROVED, AdminJobApprovalStatus.REJECTED]:
            raise ValueError("Invalid status")
        return v


class JobApproveUpdateJobRequest(BaseModel):
    job_approval_request_id: int
    status: AdminJobApprovalStatus
    reason: Optional[str] = None

    @validator("status")
    def validate_status(cls, v):
        if v not in [AdminJobApprovalStatus.APPROVED, AdminJobApprovalStatus.REJECTED]:
            raise ValueError("Invalid status")
        return v
