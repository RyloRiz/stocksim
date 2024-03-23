import math
import random
import sys
import numpy


LOW = (1, 7)
MED = (7, 15)
HIGH = (15, 30)


def wrndm():
    return random.choices(
        population=[-3, -2, -1, 0, 1, 2, 3],
        weights=[0.05, 0.1, 0.25, 0.2, 0.25, 0.1, 0.05],
        k=1
    )[0]


class Stocks:
    def __init__(self):
        self.stocks = {
            'AAPL': {
                'name': 'Apple',
                'price': 1000,
                'last_price': 1000,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'GOOG': {
                'name': 'Google',
                'price': 400,
                'last_price': 400,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'MSFT': {
                'name': 'Microsoft',
                'price': 1200,
                'last_price': 1200,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'AMZN': {
                'name': 'Amazon',
                'price': 800,
                'last_price': 800,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'TSLA': {
                'name': 'Tesla',
                'price': 100,
                'last_price': 100,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'NVDA': {
                'name': 'Nvidia',
                'price': 1400,
                'last_price': 1400,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'FOMOCO': {
                'name': 'Ford Motor Co',
                'price': 10,
                'last_price': 10,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'MCD': {
                'name': 'McDonalds',
                'price': 20,
                'last_price': 20,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            },
            'NFLX': {
                'name': 'Netflix',
                'price': 50,
                'last_price': 50,
                'trend': wrndm(),
                'lifetime': random.randint(1, 7)
            }
        }

        self.my_stocks = {
            'AAPL': 0,
            'GOOG': 0,
            'MSFT': 0,
            'AMZN': 0,
            'TSLA': 0,
            'NVDA': 0,
            'FOMOCO': 0,
            'MCD': 0,
            'NFLX': 0
        }

        self.my_cash = 100

    def get_stock(self, ticker: str):
        return self.stocks[ticker]

    def buy_stock(self, ticker: str, amount: int):
        self.my_cash -= self.stocks[ticker]['price'] * amount
        self.my_stocks[ticker] += amount

    def has_stock(self, ticker: str, amount: int):
        return self.my_stocks[ticker] >= amount

    def sell_stock(self, ticker: str, amount: int):
        self.my_cash += self.stocks[ticker]['price'] * amount
        self.my_stocks[ticker] -= amount

    def run_game_loop(self):
        changes = {}

        for ticker in self.stocks:
            # d = self.stocks[ticker]['price'] * random.randint(1, 10) / 100
            # self.stocks[ticker]['last_price'] = self.stocks[ticker]['price']
            # d2 = random.uniform(round(-d), round(d))
            # self.stocks[ticker]['price'] += d2
            # self.stocks[ticker]['price'] = numpy.clip(self.stocks[ticker]['price'], 0, 10000)

            # changes[ticker] = round((self.stocks[ticker]['price'] / self.stocks[ticker]['last_price']) * 100, 2)

            if self.stocks[ticker]['lifetime'] == 1:
                self.stocks[ticker]['trend'] = wrndm()
                self.stocks[ticker]['lifetime'] = random.randint(1, 7)
            else:
                self.stocks[ticker]['lifetime'] -= 1

            d: int

            if self.stocks[ticker]['trend'] == -3:
                d = self.stocks[ticker]['price'] * -(random.randint(HIGH[0], HIGH[1]) / 100)
            elif self.stocks[ticker]['trend'] == -2:
                d = self.stocks[ticker]['price'] * -(random.randint(MED[0], MED[1]) / 100)
            elif self.stocks[ticker]['trend'] == -1:
                d = self.stocks[ticker]['price'] * -(random.randint(LOW[0], LOW[1]) / 100)
            elif self.stocks[ticker]['trend'] == 0:
                d = 0
            elif self.stocks[ticker]['trend'] == 1:
                d = self.stocks[ticker]['price'] * (random.randint(LOW[0], LOW[1]) / 100)
            elif self.stocks[ticker]['trend'] == 2:
                d = self.stocks[ticker]['price'] * (random.randint(MED[0], MED[1]) / 100)
            elif self.stocks[ticker]['trend'] == 3:
                d = self.stocks[ticker]['price'] * (random.randint(HIGH[0], HIGH[1]) / 100)
            else:
                raise Exception(f"Invalid trend: {self.stocks[ticker]['trend']}")

            self.stocks[ticker]['last_price'] = self.stocks[ticker]['price']
            self.stocks[ticker]['price'] += d
            self.stocks[ticker]['price'] = numpy.clip(self.stocks[ticker]['price'], 0, 10000)

            def get_change(current, previous):
                if current == previous:
                    return 0
                try:
                    return ((current - previous) / previous) * 100.0
                except ZeroDivisionError:
                    return 0

            changes[ticker] = round(get_change(self.stocks[ticker]['price'], self.stocks[ticker]['last_price']), 2)
            self.stocks[ticker]['last_change'] = changes[ticker]

            # sys.exit()

        return changes
