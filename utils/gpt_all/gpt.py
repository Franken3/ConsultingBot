import asyncio
import os

import aiohttp
from aiohttp_proxy import ProxyConnector
from dotenv import load_dotenv

from utils.db_api.db_comands import get_user_dialog_history, save_user_and_assist_msg, save_continue_answ

load_dotenv()
gpt_api_key = str(os.getenv("GPT_API_KEY"))
proxy = str(os.getenv("PROXY"))


class ChatGPT:
    def __init__(self):
        self.api_key = gpt_api_key
        self.connector = ProxyConnector.from_url('socks5://bot:alexSMX2121@185.104.112.43:1080')
        self.session = aiohttp.ClientSession(connector=self.connector)

    async def async_openai_request(self, messages: list):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        data = {"model": "gpt-4",
                "messages": messages,
                "temperature": 1,
                "max_tokens": 700,
                "top_p": 1,
                "frequency_penalty": 0, "presence_penalty": 0}




        async with self.session.post(url, json=data, headers=headers, ssl=False) as response:
            info = await response.json()
            return info

    async def handle_user_message(self, tg_id: int, prompt: str, msg_id: int, is_continued: bool, section: str= None, user_prompt: str= None, ):
        # Получаем историю диалога пользователя из базы данных
        user_dialogs = await get_user_dialog_history(tg_id)

        # Добавляем новое сообщение пользователя в историю
        user_dialogs.append({"role": "user", "content": prompt})

        # Получаем ответ от GPT-4
        response = await self.async_openai_request(user_dialogs)

        # Обрабатываем ответ и добавляем его в базу данных
        if response and "choices" in response and len(response["choices"]) > 0:
            assistant_message = response["choices"][0]["message"]["content"]

            # Мне пиздец как не нравится тут же сохранять в бд, но я не хочу тащить это в
            # основной код и там уже сохранять
            if not is_continued:
                await save_user_and_assist_msg(tg_id=tg_id,
                                               section=section,
                                               user_prompt=user_prompt,
                                               msg_id=msg_id,
                                               user_message=prompt,
                                               assistant_message=assistant_message)
            else:
                await save_continue_answ(tg_id=tg_id, msg_id=msg_id, assistant_message=assistant_message)
        else:
            assistant_message = 'Увы, ошибка :('
            print('Ошибка!')
            print(response)
        return assistant_message
