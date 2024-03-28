from enum import Enum


class Role(str, Enum):
    SUPER_USER = "super_user"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"
    REPRESENTATIVE = "representative"


class SortType(str, Enum):
    ASC = "asc"
    DESC = "desc"


class OrderBy(str, Enum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SocialType(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class JobStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    TEMPORARY = "temporary"
    REMOTE = "remote"


class JobApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class SalaryType(str, Enum):
    VND = "vnd"
    USD = "usd"


class HistoryType(str, Enum):
    REGISTER = "register"
    LOGIN = "login"
    VERIFY_SUCCESS = "verify_success"
    CREATE_NEW_CAMPAIGN = "create_new_campaign"
    OFF_CAMPAIGN = "off_campaign"
    ON_CAMPAIGN = "on_campaign"
    DELETE_CAMPAIGN = "delete_campaign"
    UPDATE_CAMPAIGN = "update_campaign"
    APPROVE_JOB = "approve_job"
    REJECT_JOB = "reject_job"


class TypeAccount(str, Enum):
    NORMAL = "normal"
    BUSINESS = "business"
