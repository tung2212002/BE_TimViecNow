from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session
from pathlib import Path

from app.core.email_config import conf


class EmailService:
    async def send_email_background(
        db: Session,
        background_tasks: BackgroundTasks,
        subject: str,
        email_to: str,
        body: str,
    ):
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[email_to],
                body=body,
                subtype="html",
            )

            fm = FastMail(conf)

            background_tasks.add_task(fm.send_message, message)

            return True
        except Exception as e:
            print(e)
            return False


email_service = EmailService()

# async def send_email_background(
#     db: Session,
#     background_tasks: BackgroundTasks,
#     subject: str,
#     email_to: str,
#     body: str,
# ):
#     try:
#         message = MessageSchema(
#             subject=subject,
#             recipients=[email_to],
#             body=body,
#             subtype="html",
#         )

#         fm = FastMail(conf)

#         background_tasks.add_task(fm.send_message, message)

#         return True
#     except Exception as e:
#         return False


# def fill_template(template: str, **kwargs) -> str:
#     for key, value in kwargs.items():
#         template = template.replace("{{ " + key + " }}", value)
#     return template


# async def read_email_templates(file_path: Path) -> str:
#     html_file_template = Path(__file__).parent / "templates" / file_path
#     return html_file_template.read_text(encoding="utf-8")
