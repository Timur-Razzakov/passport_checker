import time

import httpx
from fastapi import HTTPException
from httpx import BasicAuth

from config.settings import settings
from schemas.checker_passport.passports import ErrorResponse


class Individual:
    def __init__(self):
        self.transaction_id = 1
        self.token = None
        self.token_expires_at = 0
        self.token_lifetime = 3600

    @staticmethod
    def process_result(result, response):
        error_messages = {
            "1": {"result": True, "error": "", "code": 1},
            "0": {"result": False, "error": "Сервис временно не доступен.", 'code': 0},
            "4": {"result": False, "error": "Данные не найдены в системе", 'code': 4},
            "201": {"result": False, "error": "Не все указанные поля заполнены.", 'code': 201},
            "202": {"result": False, "error": "Неверный формат данных.", 'code': 202},
        }
        if result in error_messages:
            return error_messages[result]

        return {"result": False, "error": f"Неизвестное значение результата: {response}", 'code': result}

    def process_response(self, response):
        """Метод для обработки полученного ответа"""
        result = response.get("result")
        return self.process_result(result, response)

    @staticmethod
    async def get_details(params, url, headers=None, auth=None, is_data=False):
        async with httpx.AsyncClient() as client:
            if is_data:
                response = await client.post(
                    url,
                    headers=headers,
                    data=params,  # Передача данных в формате form-data
                    auth=auth
                )
            else:
                response = await client.post(
                    url,
                    headers=headers,
                    json=params,
                    auth=auth
                )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get details. Status code: {response.status_code}",
                        "response": response.text}

    async def get_oauth_token(self, consumer_key: str,
                              consumer_secret: str,
                              username: str,
                              password: str):
        url = "https://rmp-iskm.egov.uz:9444/oauth2/token"
        data = {
            "grant_type": 'password',
            "username": username,
            "password": password,
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        auth = BasicAuth(username=consumer_key, password=consumer_secret)
        response = await self.get_details(params=data, url=url, auth=auth, headers=headers, is_data=True)
        print(234234234234, response)
        print(234234234234, response.text)
        self.token = response.get('access_token')
        self.token_expires_at = time.time() + self.token_lifetime
        return self.token

    async def get_valid_token(self):
        if self.token and time.time() < self.token_expires_at:
            return self.token
        return await self.get_oauth_token(
            consumer_key=settings.CONSUMER_KEY,
            consumer_secret=settings.CONSUMER_SECRET,
            password=settings.PASSWORD,
            username=settings.USERNAME
        )

    async def get_all_info_about_user(self, pinfl: str,
                                      passport_serial_number: str,
                                      sender_pinfl: str = settings.SENDER_PINFL,
                                      ):
        try:
            token = await self.get_valid_token()
        except Exception as e:
            raise HTTPException(status_code=500, detail=ErrorResponse(
                result=False,
                error=f'Ошибка при получении токена: {e}',
                code=500
            ).model_dump())
        url = "https://rmp-apimgw.egov.uz:8243/gcp/docrest/v1"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        params = {
            "transaction_id": self.transaction_id,
            "is_consent": "Y",
            "sender_pinfl": sender_pinfl,
            "langId": 1,
            "document": passport_serial_number,
            "pinpp": pinfl,
            "is_photo": "Y",
            "Sender": "P"
        }
        self.transaction_id += 1
        individual_details = await self.get_details(params=params, url=url, headers=headers)
        return individual_details

    async def get_individual_details(self, pinfl: str,
                                     passport_serial_number: str,
                                     ):
        individual_details = await self.get_all_info_about_user(pinfl=pinfl,
                                                                passport_serial_number=passport_serial_number,
                                                                )
        return self.process_response(response=individual_details)
