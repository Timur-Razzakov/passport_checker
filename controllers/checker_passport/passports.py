from fastapi import APIRouter

from controllers import _Controller
from controllers.checker_passport import Individual
from schemas.checker_passport.passports import IndividualAccount

router = APIRouter(
    prefix="/api/v1/passport",
    tags=["passport"],
)


class CheckPassport(_Controller):
    def __init__(self, request):
        super().__init__(request)

    async def _call(
            self, individual_account: IndividualAccount
    ):
        account_info_dict = await Individual().get_individual_details(
            passport_serial_number=individual_account.passport_serial_number,
            pinfl=individual_account.pinfl,
        )
        return account_info_dict
