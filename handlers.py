from random import randint
from loader import dp
from aiogram import types
from candybot import CandyBot

game = CandyBot()

# запуск игры
@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    game.start = True
    if game.count: # если сыграли хотябы одну игру
        if game.win: # если в прошлой игре победил бот
            await message.answer('Жаждешь реванша? Я не против. Сколько конфет положить в вазу?')      
        else:
            await message.answer('В этот раз я своего не упущу!! Сколько конфет положить в вазу?')
    else:
        await message.answer('Отлично!!! Сколько конфет положить в вазу?')

# основная логика игры
@dp.message_handler()
async def mes_all(message: types.Message):
    num = message.text
    if game.start: # если игра начата
        if num.isdigit() and not game.number: # если в вазе нет конфет
            if int(num) > 28:
                game.total = int(num)
                game.number = int(num)
                await message.answer(f'В вазе {num} конфет. Сколько конфет забераешь?')
            else:
                await message.answer(f'Мало, надо больше')
        elif num.isdigit() and int(num) > 28:
            await message.answer(f'Не жадничей. Не больше 28 конфет, помни об этом.')
        elif num.isdigit() and int(num) <= game.number and int(num) < 29:
            game.opponent(int(num))
            if game.number == 0:
                game.start = False
                game.count += 1
                game.win = 0
                await message.answer(f'Ты победил!! Твой приз {game.total} конфет!!! Желаешь повторить триумф - Жми /start')
            else:
                botnum = game.move()
                if game.number == 0:
                    game.start = False
                    game.count += 1
                    game.win = 1
                    await message.answer(f'Я забрал {botnum} конфет и победил!!! Мой приз {game.total} конфет!!! Желаешь реванша - жми /start')
                else:
                    await message.answer(f'Я забрал {botnum} конфет. Осталось {game.number} конфет. Сколько конфет забераешь?')
        elif num.isdigit() and int(num) > game.number:
            await message.answer('Столько конфет нет. Возьми поменьше.')
        else:
            await message.answer('Мы играть будем, или ерунду друг другу писать?')
    elif not game.count: # если игра ещё не начата и не одной игры не сыграно
        if not game.hello: # если приветствия не было
            game.hello = True
            await message.answer(f'Привет, {message.from_user.first_name}! В "конфеты" играть будем? Жми /start , если согласен.')
        else:
            await message.answer('Хорошь болтать, давай играть.\nЖми /start и погнали')
    else:
        await message.answer('Сыграем ешё разок? Жми /start , если согласен.')
        