import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import ValidationError
from starlette.responses import JSONResponse

from api.routers import all_routers
from config.settings import description
from exceptions import ServiceException

app = FastAPI(
    title="AI API",
    description=description,
    version="1.0.1",
)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://185.196.213.130/8081",
]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    formatted_errors = {}

    for error in errors:
        field_name = error["loc"][-1]
        message = error["msg"]
        formatted_errors[field_name] = message

    return JSONResponse(status_code=422, content=formatted_errors)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
for router in all_routers:
    app.include_router(router)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    # Преобразуем сообщение об ошибке в ваш собственный формат
    return JSONResponse(
        status_code=422,
        content={
            "result": False,
            "data": None,
            "message": exc.errors()[0]["msg"],  # Первое сообщение об ошибке
        },
    )


# Настройка Swagger UI для использования авторизации
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
if __name__ == "__main__":
    uvicorn.run(app="main:app", host="185.196.213.130", port=8081, reload=True)
