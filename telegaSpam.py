from dotenv import load_dotenv
import os
import asyncio
import telegram

load_dotenv()
CHATID = os.getenv('CHATID')
BOTAPI = os.getenv('BOTAPI')
bot = telegram.Bot(token=BOTAPI)

async def SendAfterParse(ParentDir: str):
    files = os.listdir(ParentDir)
    async with bot:
        for file in files:
            Resphoto = open(f'{ParentDir}/{file}', 'rb')
            await bot.send_document(chat_id=CHATID,disable_notification=True, document=Resphoto)
