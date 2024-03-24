from app.core import constant


def get_message_validation_error(e):
    error = e.errors()[0]["msg"]
    return error
