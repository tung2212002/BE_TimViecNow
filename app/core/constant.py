import os

FAIL = "fail"
ERROR = "error"
WARNING = "warning"
SUCCESS = "success"
MYSQL_SERVER = os.getenv("MYSQL_SERVER")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
REGEX_EMAIL = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$"
REGEX_PHONE_NUMBER = r"(84|0[3|5|7|8|9])+([0-9]{8})\b"
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/svg+xml"]
MAX_IMAGE_SIZE = 2 * 1024 * 1024
BUCKET_URL = "https://tvnow-bucket.s3.amazonaws.com/"
