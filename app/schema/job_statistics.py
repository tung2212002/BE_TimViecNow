from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Union

from app.hepler.enum import SalaryType
from app.core import constant


class JobCountBySalary(BaseModel):
    min_salary: int
    max_salary: int
    salary_type: Union[SalaryType, str]
    count: int
    time_scan: datetime

    model_config = ConfigDict(extra="ignore")
