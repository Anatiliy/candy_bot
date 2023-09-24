import os
from random import randint


class GameData:

    def __init__(self) -> None:
        self.data = {'start': 0,  # атребут принимает значение 1 при запуске игры и значение 0 при окончании игры
                     'number': 0,  # атребут, фиксирующий количества конфет в вазе
                     'opponame': 'noname',  # атребут, фиксирующий имя игрока
                     'total': 0,  # атребут, фиксирующий количества конфет в игре
                     'count': 0,  # атребут, фиксирующий количество оконченых игр
                     'win': 'None',  # атребут пртнимает значение 1 если победил бот и значение 0 если победил игрок
                     'botbag': 300,  # количество конфет в мешке бота
                     'oppobag': 0,  # количество конфет в мешке игрока
                     'lot': 0,  # количество конфет, которое можно взять из вазы
                     'level': 0}  # уровень игры


    def __getitem__(self, item: str):
        if item in self.data:
            return self.data[item]


    def __len__(self):
        return len(self.data)

    def __setitem__(self, key: str, value):
        self.data[key] = value

    # метод конвертирующий объект класса в строку
    def toStr(self):
        return ';'.join(list(map(lambda item: str(item) if not isinstance(item, str) else item, self.data.values())))

    # метод конвертирующий строку в объект класса
    def toCB(self, data: str):
        lst = list(map(lambda item: int(item) if item.isdigit() else item, data))
        index = 0
        for key in self.data:
            self.data[key] = lst[index]
            index += 1


    # метод, осуществляющий ход бота
    def move(self):
        if self.data['number'] <= self.data['lot']:
            result = self.data['number']
            self.data['number'] = 0
            return result
        elif self.data['level'] and self.data['lot'] + 1 < self.data['number'] <= self.data['lot'] * 2 + 1:
            result = self.data['number'] - self.data['lot'] + 1
            self.data['number'] = self.data['lot'] + 1
            return result
        elif self.data['level'] > 1 and self.data['number'] <= self.data['lot'] * 3 + 2:
            result = self.data['number'] - self.data['lot'] * 2 + 2
            self.data['number'] = self.data['lot'] * 2 + 2
            return result
        else:
            result = randint(1, self.data['lot'])
            self.data['number'] -= result
            return result

    # метод, осуществляющий ход игрока
    def opponent(self, oppocandy):
        self.data['number'] -= oppocandy

    # метод, осуществляющий ход игрока
    def botContribution(self, handout=0):
        self.data['start'] = 1
        self.data['lot'] = randint(10, 28)
        if handout:  # если у бота нехватает конфет, и ему одолжил их игрок
            self.data['total'] = 50
            self.data['oppobag'] -= handout
            self.data['number'] = self.data['total']
            self.data['botbag'] = 0
        else:
            self.data['total'] = randint(50, 100)
            if self.data['total'] > self.data['botbag']:
                self.botContribution()
            self.data['number'] = self.data['total']
            self.data['botbag'] -= self.data['total']


class DataProcessing:

    def __init__(self) -> None:
        self.data = {}


    def __getitem__(self, item: int):
        if item in self.data:
            return self.data[item]


    def __len__(self):
        return len(self.data)

    def __setitem__(self, key: int, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]


    # метод обновляет переменные для новой игры
    def newGame(self, id, name):
        self.data[id] = self.data.get(id, GameData())
        self.data[id]['start'] = 1
        self.data[id]['opponame'] = name
        self.data[id]['lot'] = randint(10, 28)

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