from typing import Union
import requests
from loguru import logger


def send_message_in_bot(chat_id: Union[int, str], token: str, message: str) -> None:
    """
    Обновляем ценники и уведомляем по тг
    """
    base_url = 'https://api.telegram.org/bot{token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
    }
    try:
        resp = requests.get(
            url=base_url.format(token=token),
            params=params
        )
        if not resp.status_code == 200:
            logger.error(f'Ошибка в боте: {resp.text}')
    except Exception as Ex:
        logger.error(f'При отправке сообщения в тг-бот возникла ошибка: {Ex}')
