import logging

from fastapi.security import HTTPBearer
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
            if isinstance(data, bool):
                response = {"result": data}
            elif isinstance(data, (list, dict)):
                response = data
            else:
                response = data.dict()
        except Exception as ex:
            self.log.exception(f"{self.__class__.__name__} finished with error: {str(ex)}")
            response = {
                "result": False,
                "message": f"Service error: {str(ex)}",
                "error_code": 'SERVICE_ERROR',
            }
        return response
