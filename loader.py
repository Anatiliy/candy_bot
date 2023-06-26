from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from os import getenv

load_dotenv()  # загружаем переменные из файла ".env" в виртуальное окружение
bot = Bot(getenv('TOKEN'))
dp = Dispatcher(bot)