from loader import dp
from aiogram.types import Message
from data_processing import DataProcessing
from os import getenv

games = DataProcessing()
games.read_data()

# запуск бота
@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    if message.from_id == int(getenv('ADMIN_ID')): # если пишет администратор
        await message.answer(f'Привет, {message.from_user.first_name}!\nДоступные команды:\n/game - начать игру.\n/view - показать информацию о пользователях')
    else:
        await message.answer(f'Привет, {message.from_user.first_name}! В "конфеты" играть будем?\nУсловия игры:\nВ вазе лежит заданное количество конфет. Играют два игрока делая ход друг после друга. За один ход можно забрать не более чем 28 конфет. Все конфеты оппонента достаются сделавшему последний ход.\nЖми /game , если согласен.')

# пресылает админостратору сообщение о количестве пользователей бота
@dp.message_handler(commands=['view'])
async def mes_menu(message: Message):
    if message.from_id == int(getenv('ADMIN_ID')):
        await message.answer(f'количество пользователей - {len(games.data)}')



# запуск игры
@dp.message_handler(commands=['game'])
async def mes_game(message: Message):
    games.newGame(message.from_id, message.from_user.first_name)
    if games.data[message.from_id].count: # если сыграли хотябы одну игру
        if games.data[message.from_id].win: # если в прошлой игре победил бот
            await message.answer('Жаждешь реванша? Я не против. Сколько конфет положить в вазу?')      
        else:
            await message.answer('В этот раз я своего не упущу!! Сколько конфет положить в вазу?')
    else:
        await message.answer('Отлично!!! Сколько конфет положить в вазу?')

# основная логика игры
@dp.message_handler()
async def mes_all(message: Message):
    num = message.text
    if games.data[message.from_id].start: # если игра начата
        if num.isdigit() and not games.data[message.from_id].number: # если в вазе нет конфет
            if int(num) > 28:
                games.data[message.from_id].total = int(num)
                games.data[message.from_id].number = int(num)
                await message.answer(f'В вазе {num} конфет. Сколько конфет забераешь?')
            else:
                await message.answer(f'Мало, надо больше')
        elif num.isdigit() and int(num) > 28:
            await message.answer(f'Не жадничей. Не больше 28 конфет, помни об этом.')
        elif num.isdigit() and int(num) <= games.data[message.from_id].number and int(num) < 29:
            games.data[message.from_id].opponent(int(num))
            if games.data[message.from_id].number == 0:
                games.data[message.from_id].start = 0
                games.data[message.from_id].count += 1
                games.data[message.from_id].win = 0
                games.overwrite()
                await message.answer(f'Ты победил!! Твой приз {games.data[message.from_id].total} конфет!!! Желаешь повторить триумф - Жми /game')
            else:
                botnum = games.data[message.from_id].move()
                if games.data[message.from_id].number == 0:
                    games.data[message.from_id].start = 0
                    games.data[message.from_id].count += 1
                    games.data[message.from_id].win = 1
                    games.overwrite()
                    await message.answer(f'Я забрал {botnum} конфет и победил!!! Мой приз {games.data[message.from_id].total} конфет!!! Желаешь реванша - жми /game')
                else:
                    await message.answer(f'Я забрал {botnum} конфет. Осталось {games.data[message.from_id].number} конфет. Сколько конфет забераешь?')
        elif num.isdigit() and int(num) > games.data[message.from_id].number:
            await message.answer('Столько конфет нет. Возьми поменьше.')
        else:
            await message.answer('Мы играть будем, или ерунду друг другу писать?')
    elif not games.data[message.from_id].count: # если игра ещё не начата и не одной игры не сыграно
        await message.answer('Хорошь болтать, давай играть.\nЖми /game и погнали')
    else:
        await message.answer('Сыграем ешё разок? Жми /game , если согласен.')
        