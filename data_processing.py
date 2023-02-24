import os
from random import randint


class GameData:

    def __init__(self) -> None:
        self.start = 0  # атребут пртнимает значение 1 при запуске игры и значение 0 при окончании игры
        self.number = 0  # атребут, фиксирующий количества конфет в вазе
        self.opponame = 'noname'  # атребут, фиксирующий имя игрока
        self.total = 0  # атребут, фиксирующий количества конфет в игре
        self.count = 0  # атребут, фиксирующий количество оконченых игр
        self.win = 'None'  # атребут пртнимает значение 1 если победил бот и значение 0 если победил игрок
        self.botbag = 500  # количество конфет в мешке бота
        self.oppobag = 0  # количество конфет в мешке игрока
        self.lot = 0  # количество конфет, которое можно взять из вазы
        self.level = 0  # уровень игры

    # метод конвертирующий объект класса в строку
    def toStr(self):
        return ';'.join(list(map(lambda item: str(item) if not isinstance(item, str) else item, [self.start, self.number, self.opponame, self.total, self.count, self.win, self.botbag, self.oppobag, self.lot, self.level])))

    # метод конвертирующийстроку в объект класса 
    def toCB(self, data:str):
        lst = list(map(lambda item: int(item) if item.isdigit() else item, data))
        self.start = lst[0]
        self.number = lst[1]
        self.opponame = lst[2]
        self.total = lst[3]
        self.count = lst[4]
        self.win = lst[5]
        self.botbag = lst[6]
        self.oppobag = lst[7]
        self.lot = [8]
        self.level = [9]

    # метод, осуществляющий ход бота
    def move(self):
        if self.number < self.lot + 1:
            result = self.number
            self.number = 0
            return result
        elif self.number == self.lot + 1:
            result = randint(1, self.lot)
            self.number -= result
            return result
        elif self.lot < self.number < self.lot * 2 + 1:
            result = self.number - self.lot + 1
            self.number = self.lot + 1
            return result
        else:
            result = randint(1, self.lot)
            self.number -= result
            return result

    # метод, осуществляющий ход игрока
    def opponent(self, oppocandy):
        self.number -= oppocandy

    # метод, осуществляющий ход игрока
    def botContribution(self, handout=0):
        self.start = 1
        self.lot = randint(10, 28)
        if handout:  # если у бота нехватает конфет, и ему одолжил их игрок
            self.total = 50
            self.oppobag -= handout
            self.number = self.total
            self.botbag = 0
        else:
            self.total = randint(50, 100)
            if self.total > self.botbag:
                self.botContribution()
            self.number = self.total
            self.botbag -= self.total


class DataProcessing:

    def __init__(self) -> None:
        self.data = {}

    # метод обновляет переменные для новой игры
    def newGame(self, id, name):
        self.data[id] = self.data.get(id, GameData())
        self.data[id].start = 1
        self.data[id].opponame = name
        self.data[id].lot = randint(10, 28)

    # перезапись файла информацией из переменной
    def overwrite(self):
        if self.data:
            result_data = []
            for key, value in self.data.items():
                result_data.append(str(key) + ';' + value.toStr())
            with open('gamers_data.csv', 'w', encoding='utf-8') as output_file:
                print(*result_data, sep='\n', file=output_file)
            
    # считывание информации из файла
    def read_data(self):
        if os.path.exists('gamers_data.csv'):
            with open('gamers_data.csv', 'r', encoding='utf-8') as input_file:
                data = input_file.readlines()
            for item in data:
                lst = item.rstrip().split(';')
                key = int(lst.pop(0))
                self.data[key] = GameData()
                self.data[key].toCB(lst)
        