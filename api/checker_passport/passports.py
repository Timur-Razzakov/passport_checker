from fastapi import APIRouter
from fastapi import Request

from controllers.checker_passport.passports import CheckPassport, GetAllInfoAboutUser
from schemas.checker_passport.passports import IndividualAccount, SuccessResponse, GetInfoAboutUser

router = APIRouter(
    prefix="/api/v1/passport",
    tags=["passport"],
)


@router.post(
    "/is_correct",
    response_model=SuccessResponse,
)
async def passport_checker(request: Request, individual: IndividualAccount):
    return await CheckPassport(request).call(individual)


@router.post(
    "/get_info"
)
async def info_about_user(request: Request, individual: GetInfoAboutUser):
    return await GetAllInfoAboutUser(request).call(individual)
