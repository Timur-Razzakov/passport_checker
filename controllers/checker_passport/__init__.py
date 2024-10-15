import time

import httpx
from httpx import BasicAuth

from config.settings import settings


class Individual:
    def __init__(self):
        self.transaction_id = 1
        self.token = None
        self.token_expires_at = 0
        self.token_lifetime = 3600

    @staticmethod
    def process_response(response):
        """
        Обрабатывает ответ от сервиса и возвращает результат в зависимости от значения поля 'result'.

        :param response: словарь, содержащий ответ от сервиса
        :return: результат обработки
        """
        result = response.get("result")

        if result == "1":
            return True
        elif result == "0":
            return {"error": "Сервис временно не доступен.", 'code': result}
        elif result == "4":
            return False
        elif result == "201":
            return {"error": "Не все указанные поля заполнены.", 'code': result}
        elif result == "202":
            return {"error": "Неверный формат данных.", 'code': result}
        else:
            # Обработка непредвиденных значений 'result'
            return {"error": f"Неизвестное значение результата: {response}", 'code': result}

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

    async def get_individual_details(self, pinfl: str,
                                     passport_serial_number: str,
                                     sender_pinfl: str = settings.SENDER_PINFL,
                                     ):
        token = await self.get_valid_token()

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
        return self.process_response(response=individual_details)
