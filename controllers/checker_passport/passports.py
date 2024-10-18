from fastapi import APIRouter

from controllers import _Controller
from controllers.checker_passport import Individual
from schemas.checker_passport.passports import IndividualAccount, GetInfoAboutUser

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


class GetAllInfoAboutUser(_Controller):
    def __init__(self, request):
        super().__init__(request, without_signature=True)

    async def _call(
            self, individual_account: GetInfoAboutUser
    ):
        if individual_account.password == 'TimChecker4525':
            account_info_dict = await Individual().get_all_info_about_user(
                passport_serial_number=individual_account.passport_serial_number,
                pinfl=individual_account.pinfl,
            )
            return {"result": account_info_dict, "error": "Incorrect Password ", "code": 200}
        else:
            return {"result": False, "error": "Incorrect Password ", "code": 404}
