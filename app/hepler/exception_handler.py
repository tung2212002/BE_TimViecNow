from app.core import constant


def get_message_validation_error(e):
    loc = e.errors()[0]["loc"][0]
    error = e.errors()[0]["msg"]
    return loc + ": " + error
