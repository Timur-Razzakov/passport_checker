import re

from pydantic import BaseModel, field_validator


class SuccessResponse(BaseModel):
    result: bool


class ErrorResponse(BaseModel):
    error: str
    code: int


class IndividualAccount(BaseModel):
    passport_serial_number: str
    pinfl: str

    @field_validator("passport_serial_number")
    def validate_passport(cls, value):
        if not re.match(r"^[A-Z]{2}\d{7}$", value):
            raise ValueError("Passport must start with 2 letters followed by 7 digits")
        return value
