from dotenv import load_dotenv
import os
import asyncio
import telegram

load_dotenv()
CHATID = os.getenv('CHATID')
BOTAPI = os.getenv('BOTAPI')

async def main(Files: list,ParentDir: str):
    bot = telegram.Bot(token=BOTAPI)
    async with bot:
        #await bot.send_message(chat_id=CHATID, text='Hello, World!')
        for file in Files:
            Resphoto = open(f'{ParentDir}/{file}', 'rb')
            await bot.send_document(chat_id=CHATID,disable_notification=True, document=Resphoto)


if __name__ == '__main__':
    files = os.listdir("Arknights")
    for file in files:
        print(file)
    asyncio.run(main(files, "Arknights"))