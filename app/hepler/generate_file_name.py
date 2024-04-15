import uuid


def generate_file_name(key: str = "", file_name: str = "") -> str:
    return (
        f"{key}/{uuid.uuid4()}.{file_name.split('.')[-1]}"
        if key
        else f"{uuid.uuid4()}.{file_name.split('.')[-1]}"
    )
