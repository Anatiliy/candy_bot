import os
from random import randint


class GameData:

    def __init__(self) -> None:
        self.start = 0 # атребут пртнимает значение 1 при запуске игры и значение 0 при окончании игры
        self.number = 0 # атребут, фиксирующий количества конфет в вазе
        self.opponame = 'noname' # атребут, фиксирующий имя игрока
        self.total = 0  # атребут, фиксирующий количества конфет в игре
        self.count = 0 # атребут, фиксирующий количество оконченых игр
        self.win = 'None' # атребут пртнимает значение 1 если победил бот и значение 0 если победил игрок
        self.botbag = 500 # количество конфет в мешке бота (в данный момент в программе не задействован)
        self.oppobag = 0 # количество конфет в мешке игрока (в данный момент в программе не задействован)

    # метод конвертирующий объект класса в строку
    def toStr(self):
        return ';'.join(list(map(lambda item: str(item) if not isinstance(item, str) else item, [self.start, self.number, self.opponame, self.total, self.count, self.win, self.botbag, self.oppobag])))

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


class DataProcessing:

    def __init__(self) -> None:
        self.data = {}

    # метод обновляет переменные для новой игры
    def newGame(self, id, name):
        self.data[id] = self.data.get(id, GameData())
        self.data[id].start = 1
        self.data[id].opponame = name

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
        