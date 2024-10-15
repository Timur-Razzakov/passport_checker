from fastapi import APIRouter
from fastapi import Request

from controllers.checker_passport.passports import CheckPassport
from schemas.checker_passport.passports import IndividualAccount

router = APIRouter(
    prefix="/api/v1/passport",
    tags=["passport"],
)


@router.post(
    "/is_correct",
    response_model=dict | bool,
)
async def passport_checker(request: Request, individual: IndividualAccount):
    return await CheckPassport(request).call(individual)
