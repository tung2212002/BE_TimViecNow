from enum import Enum


class Role(str, Enum):
    SUPER_USER = "super_user"
    ADMIN = "admin"
    USER = "user"
    SOCIAL_NETWORK = "social_network"
    GUEST = "guest"
    BUSINESS = "business"


class OrderType(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortBy(str, Enum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class SortByJob(str, Enum):
    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    DEADLINE = "deadline"
    QUANTITY = "quantity"
    SALARY = "salary"


class Provider(str, Enum):
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
    PUBLISHED = "published"
    REJECTED = "rejected"
    EXPIRED = "expired"
    DRAFT = "draft"
    BANNED = "banned"
    STOPPED = "stopped"
    ALL = "all"


class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    INTERNSHIP = "internship"


class JobApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    STOPPED = "stopped"
    ALL = "all"


class SalaryType(str, Enum):
    VND = "vnd"
    USD = "usd"
    DEAL = "deal"


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


class TokenType(str, Enum):
    ACCESS = "access_token"
    REFRESH = "refresh_token"


class CampaignStatus(str, Enum):
    STOPPED = "stopped"
    OPEN = "open"
    ALL = "all"


class FilterCampaign(str, Enum):
    ALL = "all"
    ONLY_OPEN = "only_open"
    HAS_NEW_CV = "has_new_cv"
    ACTIVED_CV_COUT = "actived_cv_count"
    HAS_PUBLIC_JOB = "has_public_job"
    HAS_RUNNING_SERVICE = "has_running_service"
    EXPIRED_JOB = "expired_job"
    WAITING_APPROVAL_JOB = "waiting_approval_job"


class VerifyCodeStatus(str, Enum):
    ACTIVE = 1
    INACTIVE = 0


class VerifyCodeType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"


class CompanyType(str, Enum):
    COMPANY = "company"
    BUSINESS = "household"


class FolderBucket(str, Enum):
    AVATAR = "avatar"
    LOGO = "logo"
    CV = "cv"
    JOB = "job"
    COMPANY = "company"
    CAMPAIGN = "campaign"
    BUSINESS = "business"
    FIELD = "field"
    LABEL_COMPANY = "label_company"


class VerifyType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    COMPANY = "company"
    IDENTIFY = "identify"
