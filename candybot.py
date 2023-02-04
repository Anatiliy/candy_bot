from random import randint

class CandyBot:

    def __init__(self) -> None:
        self.start = False # атребут пртнимает значение True при запуске игры и значение False при окончании игры
        self.number = None # атребут, фиксирующий количества конфет в вазе
        self.opponame = 'noname' # атребут, фиксирующий имя игрока
        self.total = None  # атребут, фиксирующий количества конфет в игре
        self.count = 0 # атребут, фиксирующий количество оконченых игр
        self.win = None # атребут пртнимает значение 1 если победил бот и значение 0 если победил игрок
        self.hello = False # атребут пртнимает значение True при приветствии игрока и False если бот ещё не приветствовал игрока

    # метод, осуществляющий ход бота
    def move(self):
        if self.number < 29:
            result = self.number
            self.number = 0
            return result
        elif self.number == 29:
            result = randint(1, 28)
            self.number -= result
            return result
        elif 28 < self.number < 57:
            result = self.number - 29
            self.number = 29
            return result
        else:
            result = randint(1, 28)
            self.number -= result
            return result

    # метод, осуществляющий ход игрока
    def opponent(self, oppocandy):
        self.number -= oppocandy

