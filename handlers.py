from loader import dp
from aiogram.types import Message
from data_processing import DataProcessing, GameData
from random import randint
from os import getenv

games = DataProcessing()
games.read_data()

# запуск бота
@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    if message.from_id == int(getenv('ADMIN_ID')): # если пишет администратор
        await message.answer(f'Привет, {message.from_user.first_name}!\nДоступные команды:\n/game - начать игру.\n/view - показать информацию о пользователях')
    elif games.data[message.from_id].count:
        await message.answer(f'Привет, {message.from_user.first_name}!\nПродолжим игру?\nНапоминаю:\nУ тебя в мешке {games.data[message.from_id].oppobag} конфет, у меня в мешке {games.data[message.from_id].botbag} конфет.')
    else:
        await message.answer(f'Привет, {message.from_user.first_name}! В "конфеты" играть будем?\nУсловия игры:\nУ меня есть мешок, в котором лежит 500 конфет.\nОдин из нас кладёт из своего мешка в вазу от 50 до 100 конфет.\nВ начале игры я кладу конфеты в вазу. так как у тебя мешок пустой. В следующих раундах в вазу кладёт конфеты проигравший в прошлом раунде игрок. Ходить будем друг после друга, превый ход в раунде делает победитель прошлого раунда. За один ход можно забрать определённое количество конфет, в каждом раунде оно меняется. Все конфеты оппонента достаются сделавшему последний ход.\nТы победишь, если у меня не останется ни одной конфеты в мешке.\nЖми /game , если согласен.')

# пресылает админостратору сообщение о количестве пользователей бота
@dp.message_handler(commands=['view'])
async def mes_menu(message: Message):
    if message.from_id == int(getenv('ADMIN_ID')):
        await message.answer(f'количество пользователей - {len(games.data)}')



# запуск игры
@dp.message_handler(commands=['game'])
async def mes_game(message: Message):
    if message.from_id in games.data:
        if not games.data[message.from_id].start:
            games.newGame(message.from_id, message.from_user.first_name)
        else:
            await message.answer('Уже играем, делай свой ход')
    else:
        games.newGame(message.from_id, message.from_user.first_name)
    if games.data[message.from_id].count: # если сыграли хотябы одну игру
        if games.data[message.from_id].win and games.data[message.from_id].oppobag > 49: # если в прошлой игре победил бот и у человека в мешке больше 49 конфет
            await message.answer(f'Жаждешь реванша? Я не против.\nУ тебя в мешке {games.data[message.from_id].oppobag} конфет, у меня в мешке {games.data[message.from_id].botbag} конфет.\nБрать можно не больше {games.data[message.from_id].lot} конфет.\nСколько конфет кладёшь в вазу?')
        elif games.data[message.from_id].win and games.data[message.from_id].oppobag < 50:  # если в прошлой игре победил бот и у человека в мешке меньше 50 конфет
            bot_contribution = randint(50, 100)
            games.data[message.from_id].total = bot_contribution
            games.data[message.from_id].number = bot_contribution
            games.data[message.from_id].botbag -= bot_contribution
            await message.answer(f'Жаждешь реванша? Я не против.\nУ меня в мешке {games.data[message.from_id].botbag + bot_contribution} конфет, у тебя в мешке {games.data[message.from_id].oppobag} конфет. Этого не достаточно.\nТак уж и быть, положу в вазу {bot_contribution} конфет.\nБрать можно не больше {games.data[message.from_id].lot} конфет.\nСколько конфет забераешь?')
        else:
            bot_contribution = randint(50, 100)
            games.data[message.from_id].total = bot_contribution
            games.data[message.from_id].number = bot_contribution
            games.data[message.from_id].botbag -= bot_contribution
            await message.answer(f'В этот раз я своего не упущу!!\nУ тебя в мешке {games.data[message.from_id].oppobag} конфет, у меня в мешке {games.data[message.from_id].botbag + bot_contribution} конфет. Я кладу в вазу {bot_contribution} конфет.\nБрать можно не больше {games.data[message.from_id].lot} конфет.\nСколько конфет забераешь?')
    else:
        bot_contribution = randint(50, 100)
        games.data[message.from_id].total = bot_contribution
        games.data[message.from_id].number = bot_contribution
        games.data[message.from_id].botbag -= bot_contribution
        await message.answer(f'Отлично!!!\nУ тебя в мешке {games.data[message.from_id].oppobag} конфет, у меня в мешке {games.data[message.from_id].botbag + bot_contribution} конфет. Я кладу в вазу {bot_contribution} конфет.\nБрать можно не больше {games.data[message.from_id].lot} конфет.\nСколько конфет забераешь?')

# основная логика игры
@dp.message_handler()
async def mes_all(message: Message):
    num = message.text
    if games.data[message.from_id].start: # если игра начата
        if num.isdigit() and not games.data[message.from_id].number and games.data[message.from_id].win and games.data[message.from_id].oppobag: # если в вазе нет конфет и в прошлом раунде победил бот
            if 50 <= int(num) <= 100 and int(num) <= games.data[message.from_id].oppobag:
                games.data[message.from_id].total = int(num)
                games.data[message.from_id].number = int(num)
                games.data[message.from_id].oppobag -= int(num)
                botnum = games.data[message.from_id].move()
                await message.answer(f'Ты положил в вазу {games.data[message.from_id].total} конфет. Я забираю {botnum} конфет. В вазе осталось {games.data[message.from_id].number} конфет. Сколько конфет забераешь?')
            elif int(num) > games.data[message.from_id].oppobag:
                await message.answer('У тебя нет столько конфет')
            elif int(num) > 100:
                await message.answer('Много, надо меньше.')
            else:
                await message.answer('Мало, надо больше.')
        elif num.isdigit() and int(num) > games.data[message.from_id].lot:
            await message.answer(f'Не жадничей. Не больше {games.data[message.from_id].lot} конфет, помни об этом.')
        elif num.isdigit() and int(num) <= games.data[message.from_id].number and int(num) < games.data[message.from_id].lot + 1:
            games.data[message.from_id].opponent(int(num))
            if games.data[message.from_id].number == 0:
                games.data[message.from_id].start = 0
                games.data[message.from_id].count += 1
                games.data[message.from_id].win = 0
                games.data[message.from_id].oppobag += games.data[message.from_id].total
                games.overwrite()
                await message.answer(f'Ты победил!! Твой приз {games.data[message.from_id].total} конфет!!! Желаешь повторить триумф - Жми /game')
            else:
                botnum = games.data[message.from_id].move()
                if games.data[message.from_id].number == 0:
                    games.data[message.from_id].start = 0
                    games.data[message.from_id].count += 1
                    games.data[message.from_id].win = 1
                    games.data[message.from_id].botbag += games.data[message.from_id].total
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
        