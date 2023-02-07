from loader import dp
from aiogram import types
from candybot import CandyBot

game = CandyBot()

# запуск бота
@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}! В "конфеты" играть будем?\nУсловия игры:\nВ вазе лежит заданное количество конфет. Играют два игрока делая ход друг после друга. За один ход можно забрать не более чем 28 конфет. Все конфеты оппонента достаются сделавшему последний ход.\nЖми /game , если согласен.')

# запуск игры
@dp.message_handler(commands=['game'])
async def mes_game(message: types.Message):
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
                await message.answer(f'Ты победил!! Твой приз {game.total} конфет!!! Желаешь повторить триумф - Жми /game')
            else:
                botnum = game.move()
                if game.number == 0:
                    game.start = False
                    game.count += 1
                    game.win = 1
                    await message.answer(f'Я забрал {botnum} конфет и победил!!! Мой приз {game.total} конфет!!! Желаешь реванша - жми /game')
                else:
                    await message.answer(f'Я забрал {botnum} конфет. Осталось {game.number} конфет. Сколько конфет забераешь?')
        elif num.isdigit() and int(num) > game.number:
            await message.answer('Столько конфет нет. Возьми поменьше.')
        else:
            await message.answer('Мы играть будем, или ерунду друг другу писать?')
    elif not game.count: # если игра ещё не начата и не одной игры не сыграно
        await message.answer('Хорошь болтать, давай играть.\nЖми /game и погнали')
    else:
        await message.answer('Сыграем ешё разок? Жми /game , если согласен.')
        