import math
import random

import numpy


class Stocks:
    def __init__(self):
        self.stocks = {
            'AAPL': {
                'name': 'Apple',
                'price': 1000,
                'last_price': 1000,
            },
            'GOOG': {
                'name': 'Google',
                'price': 400,
                'last_price': 400,
            },
            'MSFT': {
                'name': 'Microsoft',
                'price': 1200,
                'last_price': 1200,
            },
            'AMZN': {
                'name': 'Amazon',
                'price': 800,
                'last_price': 800,
            },
            'TSLA': {
                'name': 'Tesla',
                'price': 100,
                'last_price': 100,
            },
            'NVDA': {
                'name': 'Nvidia',
                'price': 1400,
                'last_price': 1400,
            },
            'FOMOCO': {
                'name': 'Ford Motor Co',
                'price': 10,
                'last_price': 10,
            },
            'MCD': {
                'name': 'McDonalds',
                'price': 20,
                'last_price': 20,
            },
            'NFLX': {
                'name': 'Netflix',
                'price': 50,
                'last_price': 50,
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
            d = self.stocks[ticker].price * random.randint(1, 10) / 100

            self.stocks[ticker]['last_price'] = self.stocks[ticker]['price']
            self.stocks[ticker]['price'] += random.randint(round(-d), round(d))
            self.stocks[ticker]['price'] = numpy.clip(self.stocks[ticker]['price'], 0, 10000)

            changes[ticker] = round((self.stocks[ticker]['price'] / self.stocks[ticker]['last_price']) * 100, 2)

        return changes
