from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.orm import Session

from app.core.email_config import conf


class EmailService:
    async def send_email_background(
        self,
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
