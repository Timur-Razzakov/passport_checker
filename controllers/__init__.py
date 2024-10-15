import logging

from fastapi.security import HTTPBearer
from starlette.responses import JSONResponse

from exceptions import ServiceException
from schemas import ControllerResult

security = HTTPBearer()


class _Controller:
    def __init__(self, request):
        self.log = logging.LoggerAdapter(
            logging.getLogger("app"), {"clsName": self.__class__.__name__}
        )
        self.request = request

    async def _call(self, *args, **kwds):
        raise NotImplementedError("%s._call" % self.__class__.__name__)

    async def call(self, *args, **kwds):
        try:
            data = await self._call(*args, **kwds)
            if not isinstance(data, (list, dict)):
                data = data.dict()
            response = ControllerResult(data=data)
        except ServiceException as ex:
            ex_message = str(ex)
            self.log.warning(ex_message)
            response = ControllerResult(
                result=False,
                message=ex.response_message or ex_message,
                error_code=ex.error_code,
                error_key=ex.error_key,
            )
            return JSONResponse(content=response.model_dump(), status_code=500)
        except Exception as ex:
            self.log.exception("%s finished with error" % self.__class__.__name__)
            response = ControllerResult(
                result=False,
                message=f"Service error: {str(ex)}",
                error_code='SERVICE_ERROR',
            )
            return JSONResponse(content=response.model_dump(), status_code=500)
        else:
            return JSONResponse(content=response.model_dump())
