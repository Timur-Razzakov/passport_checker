import logging

from fastapi.security import HTTPBearer

from config.settings import settings
from controllers.signature import Signature
from schemas.checker_passport.passports import ErrorResponse

security = HTTPBearer()


class _Controller:
    def __init__(self, request, without_signature: bool = False):
        self.log = logging.LoggerAdapter(
            logging.getLogger("app"), {"clsName": self.__class__.__name__}
        )
        self.request = request
        self.without_signature = without_signature

    async def _call(self, *args, **kwds):
        raise NotImplementedError("%s._call" % self.__class__.__name__)

    async def call(self, *args, **kwds):
        try:
            if not self.without_signature:
                await Signature(request=self.request,
                                secret_key=settings.SECRET_KEY).verify_request_signature()
            data = await self._call(*args, **kwds)
            if isinstance(data, (list, dict)):
                response = data
            else:
                response = data.dict()

        except Exception as ex:
            self.log.exception(f"{self.__class__.__name__} finished with error: {str(ex)}")
            response = ErrorResponse(
                result=False,
                error=ex.detail['error'] if isinstance(ex.detail, dict) else str(ex.detail),
                code=400
            ).model_dump()
        return response
