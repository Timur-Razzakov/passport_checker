from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Get info about passport
    CONSUMER_KEY: str
    CONSUMER_SECRET: str
    USERNAME: str
    PASSWORD: str
    SENDER_PINFL: str

    SECRET_KEY: str
    ALGORITHMS: str

    class Config:
        env_file = ".env"


settings = Settings()
description = """
API AI

## Описание проекта

Проект предназначен для проверки паспортных данных

Возможные результаты:
{"result": True, "error": "", "code": 1},
{"result": False, "error": "Сервис временно не доступен.", 'code': 0},
{"result": False, "error": "Данные не найдены в системе", 'code': 4},
{"result": False, "error": "Не все указанные поля заполнены.", 'code': 201},
{"result": False, "error": "Неверный формат данных.", 'code': 202},
        
"""
