from loader import dp
from aiogram.types import Message
from data_processing import DataProcessing
from os import getenv

games = DataProcessing()
games.read_data()

# функция позволяет правильно выводить слово "конфеты" на экран, в зависимости от количества конфет
def change_word(word: str, number: int):
    number = str(number)
    if word in ('мешке', 'приз'):
        if number[-1] in ('2', '3', '4') and number not in ('12', '13', '14'):
            return f'{word} {number} конфеты'
        elif number[-1] == '1' and number != '11':
            return f'{word} {number} конфета'
        else:
            return f'{word} {number} конфет'
    else:
        if number[-1] == '1' and number != '11':
            return f'{word} {number} конфеты'
        else:
            return f'{word} {number} конфет'

# запуск бота
@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    if message.from_id == int(getenv('ADMIN_ID')):  # если пишет администратор
        await message.answer(f'Привет, {message.from_user.first_name}!\nДоступные команды:\n/game - начать игру.\n/view - показать информацию о пользователях')
    elif message.from_id in games.data:
        await message.answer(f'Привет, {message.from_user.first_name}!\nПродолжим игру?\nНапоминаю:\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag)}.')
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
            if games.data[message.from_id].count:  # если сыграли хотябы одну игру
                if games.data[message.from_id].win and games.data[message.from_id].oppobag > 49:  # если в прошлой игре победил бот и у человека в мешке больше 49 конфет
                    games.newGame(message.from_id, message.from_user.first_name)
                    await message.answer(f'Жаждешь реванша? Я не против.\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag)}.\nБрать можно не {change_word("больше", games.data[message.from_id].lot)}.\nСколько конфет кладёшь в вазу?')
                elif games.data[message.from_id].win and games.data[message.from_id].oppobag < 50:  # если в прошлой игре победил бот и у человека в мешке меньше 50 конфет
                    games.data[message.from_id].botContribution()
                    await message.answer(f'Жаждешь реванша? Я не против.\nУ меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}, у тебя в {change_word("мешке", games.data[message.from_id].oppobag)}. Этого не достаточно.\nТак уж и быть, положу в вазу {change_word(games.data[message.from_id].total)}.\nБрать можно не {change_word("больше", games.data[message.from_id].lot)}.\nСколько конфет забераешь?')
                elif games.data[message.from_id].botbag < 50:  # если у бота в мешке меньше 50 конфет
                    await message.answer(f'У меня в {change_word("мешке", games.data[message.from_id].botbag)}. Этого недостаточно, чтобы продолжить игру.\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}.\n Если хочешь продолжить игру, можешь добавить мне {change_word(50 - games.data[message.from_id].botbag)}, и продолжим игру. Если согласен введи {50 - games.data[message.from_id].botbag}.')
                else:
                    games.data[message.from_id].botContribution()
                    await message.answer(f'В этот раз я своего не упущу!!\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}. Я кладу в вазу {change_word(games.data[message.from_id].total)}.\nБрать можно не {change_word("больше", games.data[message.from_id].lot)}.\nСколько конфет забераешь?')
            else:
                games.newGame(message.from_id, message.from_user.first_name)
                await message.answer(f'Продолжим!!!\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}. Я кладу в вазу {change_word(games.data[message.from_id].total)}.\nБрать можно не {change_word("больше", games.data[message.from_id].lot)}.\nСколько конфет забераешь?')
        else:
            await message.answer('Уже играем, делай свой ход')
    else:
        games.newGame(message.from_id, message.from_user.first_name)
        games.data[message.from_id].botContribution()
        await message.answer(
            f'Отлично!!!\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}. Я кладу в вазу {change_word(games.data[message.from_id].total)}.\nБрать можно не {change_word("больше", games.data[message.from_id].lot)}.\nСколько конфет забераешь?')


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
                await message.answer(f'Ты положил в вазу {change_word(games.data[message.from_id].total)}. Я забираю {change_word(botnum)}. В вазе осталось {change_word(games.data[message.from_id].number)}. Сколько конфет забераешь?')
            elif int(num) > games.data[message.from_id].oppobag:
                await message.answer('У тебя нет столько конфет')
            elif int(num) > 100:
                await message.answer('Много, надо меньше.')
            else:
                await message.answer('Мало, надо больше.')
        elif num.isdigit() and int(num) > games.data[message.from_id].lot:
            await message.answer(f'Не жадничей. Не больше {games.data[message.from_id].lot} конфет, помни об этом.')
        elif num.isdigit() and int(num) <= games.data[message.from_id].number and 0 < int(num) < games.data[message.from_id].lot + 1:
            games.data[message.from_id].opponent(int(num))
            if games.data[message.from_id].number == 0:
                games.data[message.from_id].start = 0
                games.data[message.from_id].count += 1
                games.data[message.from_id].win = 0
                games.data[message.from_id].oppobag += games.data[message.from_id].total
                games.overwrite()
                await message.answer(f'Победа!! Твой приз {change_word("приз", games.data[message.from_id].total)}!!!\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}.\nЖелаешь повторить триумф - Жми /game')
            else:
                botnum = games.data[message.from_id].move()
                if games.data[message.from_id].number == 0:
                    games.data[message.from_id].start = 0
                    games.data[message.from_id].count += 1
                    games.data[message.from_id].win = 1
                    games.data[message.from_id].botbag += games.data[message.from_id].total
                    games.overwrite()
                    await message.answer(f'Я забрал {change_word(botnum)} и победил!!! Мой {change_word("приз", games.data[message.from_id].total)}!!!\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}.\nЖелаешь реванша - жми /game')
                else:
                    await message.answer(f'Я забрал {change_word(botnum)}. Осталось {change_word(games.data[message.from_id].number)}. Сколько конфет забераешь?')
        elif num.isdigit() and int(num) > games.data[message.from_id].number:
            await message.answer('Столько конфет нет. Возьми поменьше.')
        else:
            await message.answer('Мы играть будем, или ерунду друг другу писать?')
    elif not games.data[message.from_id].count:  # если игра ещё не начата и не одной игры не сыграно
        await message.answer('Хорошь болтать, давай играть.\nЖми /game и погнали')
    elif not games.data[message.from_id].start and num.isdigit() and int(num) == 50 - games.data[message.from_id].botbag:  # если игра не начата и введёное число равно недостающему боту количеству конфет
        games.data[message.from_id].botContribution(handout=int(num))
        await message.answer(
            f'Благодарю!!!\nУ тебя в {change_word("мешке", games.data[message.from_id].oppobag)}, у меня в {change_word("мешке", games.data[message.from_id].botbag + games.data[message.from_id].total)}. Я кладу в вазу {change_word(games.data[message.from_id].total)}.\nБрать можно не {change_word("больше", games.data[message.from_id].lot)}.\nСколько конфет забераешь?')

    else:
        await message.answer('Сыграем ешё разок? Жми /game , если согласен.')
        