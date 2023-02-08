from handlers import dp
from aiogram import executor
from os import getenv

async def on_start(_):
    print('Бот запущен')
    await dp.bot.send_message(getenv('ADMIN_ID'), 'Бот запущен.\n/start') # отправляем сообшение администратору

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
