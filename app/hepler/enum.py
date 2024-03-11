from enum import Enum


class Role(str, Enum):
    SUPER_USER = "super_user"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


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
