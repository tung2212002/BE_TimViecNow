from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import exists, select

from app.model import Account, CVApplication, Campaign, Conversation, ConversationMember
from app.hepler.enum import Role


class CRUDContact:
    def get_list_contactables_for_business(
        self, db: Session, account: Account, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Account]:
        query = (
            db.query(Account)
            .filter(
                Account.role == Role.USER,
                db.query(CVApplication)
                .join(Campaign, Campaign.id == CVApplication.campaign_id)
                .filter(
                    Campaign.business_id == account.id,
                    CVApplication.user_id == Account.id,
                )
                .exists(),
            )
            .limit(limit)
            .offset(skip)
        )

        return query.all()

    def get_list_contactables_for_user(
        self, db: Session, account: Account, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Account]:
        query = (
            db.query(Account)
            .filter(
                Account.role == Role.BUSINESS,
                db.query(CVApplication)
                .join(Campaign, Campaign.id == CVApplication.campaign_id)
                .filter(
                    Campaign.business_id == Account.id,
                    CVApplication.user_id == account.id,
                )
                .exists(),
            )
            .limit(limit)
            .offset(skip)
        )

        return query.all()

    def check_business_can_contact(
        self, db: Session, account_ids: List[int], account: Account
    ) -> bool:
        query = (
            db.query(CVApplication.user_id)
            .join(Campaign, CVApplication.campaign_id == Campaign.id)
            .filter(
                CVApplication.user_id.in_(account_ids),
                Campaign.business_id == account.id,
            )
            .distinct(CVApplication.user_id)
        )

        return query.count() == len(account_ids)

    def check_can_contact(
        self, db: Session, candidate_id: int, business_id: int
    ) -> bool:
        subquery = select(Campaign.id).where(Campaign.business_id == business_id)

        query = select(
            exists().where(
                CVApplication.user_id == candidate_id,
                CVApplication.campaign_id.in_(subquery),
            )
        )

        return db.execute(query).scalar()

        # SELECT EXISTS (
        # SELECT 1
        # FROM c_v_application
        # WHERE c_v_application.user_id = :candidate_id
        # AND c_v_application.campaign_id IN (
        #     SELECT campaign.id
        #     FROM campaign
        #     WHERE campaign.business_id = :business_id
        # )
        # ) AS exists_result;

    def get_conversations(
        db: Session, account: Account, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Conversation]:
        return (
            db.query(Conversation)
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Conversation.id,
            )
            .filter(ConversationMember.account_id == account.id)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(skip)
            .all()
        )


contact = CRUDContact()
