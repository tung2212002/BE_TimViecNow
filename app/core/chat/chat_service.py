from redis.asyncio import Redis
from sqlalchemy.orm import Session
from typing import List, Tuple
from redis.asyncio import Redis

from app.model import Account, Conversation, CVApplication, Job
from app.crud import conversation as conversationCRUD, contact as contactCRUD
from app.hepler.enum import TypeAccount
from app.schema.business import BusinessBasicInfoResponse
from app.schema.user import UserBasicResponse
from app.schema.conversation import ConversationResponse
from app.schema.cv_application import CVApplicationGeneralResponse
from app.schema.page import Pagination
from app.core.business.business_helper import business_helper
from app.core.job.job_helper import job_helper
from app.core.user.user_helper import user_helper
from app.core.conversation.conversation_helper import conversation_helper
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.hepler.enum import ConversationType


class ChatService:
    async def get(db: Session, redis: Redis, data: dict, current_user: Account):
        page = Pagination(**data)

        conversations: List[Conversation] = contactCRUD.get_conversations(
            db, account=current_user, **page.model_dump()
        )

        response = []
        for conversation in conversations:
            if conversation.type == ConversationType.PRIVATE:
                response = conversation_helper.get_private_conversation_response(
                    db, conversation, current_user
                )
            else:
                response = conversation_helper.get_group_conversation_response(
                    db, conversation
                )
            response.append(response)

        return CustomResponse(data=response)

    async def get_contactables(
        self, db: Session, redis: Redis, data: dict, current_user: Account
    ):
        page: Pagination = Pagination(**data)

        response = []
        if current_user.type_account == TypeAccount.BUSINESS:
            contactables: List[Tuple[Account, CVApplication]] = (
                contactCRUD.get_list_contactables_for_business(
                    db, account=current_user, **page.model_dump()
                )
            )
            for contactable in contactables:
                account, cv_application = contactable
                response.append(
                    {
                        **user_helper.get_basic_info_by_account(
                            db, account
                        ).model_dump(),
                        "job": job_helper.get_info_general(cv_application.campaign.job),
                    }
                )

        else:
            contactables: List[Tuple[Account, CVApplication]] = (
                contactCRUD.get_list_contactables_for_user(
                    db, account=current_user, **page.model_dump()
                )
            )
            for contactable in contactables:
                account, cv_application = contactable
                response.append(
                    {
                        **business_helper.get_basic_info_by_account(
                            db, account
                        ).model_dump(),
                        "job": job_helper.get_info_general(cv_application.campaign.job),
                    }
                )

        return CustomResponse(data=response)


chat_service = ChatService()
