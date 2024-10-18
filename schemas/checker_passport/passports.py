import re
from typing import Any

from pydantic import BaseModel, field_validator
from typing_extensions import Self


class SuccessResponse(BaseModel):
    result: bool
    error: str
    code: int


class ErrorResponse(SuccessResponse):
    pass


class IndividualAccount(BaseModel):
    passport_serial_number: str
    pinfl: str

    @field_validator("passport_serial_number")
    def validate_passport(cls, value):
        if not re.match(r"^[A-Z]{2}\d{7}$", value):
            raise ValueError("Passport must start with 2 letters followed by 7 digits")
        return value

    @field_validator("pinfl")
    def validate_pinfl(cls, value: Any) -> Self:
        if not re.match(r"^\d{14}$", value):
            raise ValueError("PINFL must be 14 digits")
        return value


class GetInfoAboutUser(IndividualAccount):
    password: str
