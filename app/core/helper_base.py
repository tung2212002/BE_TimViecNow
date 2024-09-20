from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel

from app.db.base_class import Base
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.core import constant

PaginationType = TypeVar("PaginationType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class HelperBase(Generic[PaginationType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        pagination: Type[PaginationType],
        create: Type[CreateSchemaType],
        update: Type[UpdateSchemaType],
    ):
        self.pagination = pagination
        self.create = create
        self.update = update

    def validate_pagination(
        self,
        data: dict,
    ) -> Optional[PaginationType]:
        if self.pagination:
            try:
                page = self.pagination(**data)
            except Exception as e:
                return custom_response_error(
                    status_code=400,
                    status=constant.ERROR,
                    response=get_message_validation_error(e),
                )
            return page

    def validate_create(
        self,
        data: dict,
    ) -> Optional[CreateSchemaType]:
        if self.create:
            try:
                obj = self.create(**data)
            except Exception as e:
                return custom_response_error(
                    status_code=400,
                    status=constant.ERROR,
                    response=get_message_validation_error(e),
                )
            return obj

    def validate_update(
        self,
        data: dict,
    ) -> Optional[UpdateSchemaType]:
        if self.update:
            try:
                obj = self.update(**data)
            except Exception as e:
                return custom_response_error(
                    status_code=400,
                    status=constant.ERROR,
                    response=get_message_validation_error(e),
                )
            return obj
