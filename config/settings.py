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

"""
