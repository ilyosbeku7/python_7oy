import requests
import asyncio
from telegram import Bot

async def get_chat_id(bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['result']:
            chat_id = data['result'][0]['message']['chat']['id']
            return chat_id
        else:
            print("No updates found. Make sure you've started a conversation with your bot.")
    else:
        print(f"Failed to fetch updates. Status code: {response.status_code}")

async def send_message(bot_token, chat_id, text):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=text)

bot_token = '6822713325:AAFnZhE3rMa9QbRuqRIZi1E46YkB37Loh6E'

async def main(text):
    chat_id = await get_chat_id(bot_token)
    if chat_id:
        await send_message(bot_token, chat_id, text)
    else:
        print("No chat ID found.")
