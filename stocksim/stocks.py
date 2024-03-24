import math
import random
import sys
from typing import List, Dict, Tuple

import numpy

LOW = (1, 70)
MED = (70, 150)
HIGH = (150, 250)

unbiased_distribution = [0.05, 0.1, 0.25, 0.2, 0.25, 0.1, 0.05]
biased_good_distribution = [0.05, 0.1, 0.15, 0.3, 0.25, 0.1, 0.05]


def get_lifetime(trend: int):
    t = abs(trend)
    return random.randint(1, int(10 / (t + 1)))


def wrndm(old_trends=None):
    if old_trends is None:
        old_trends = [0]
    return random.choices(
        population=[-3, -2, -1, 0, 1, 2, 3],
        weights=create_hotspot_distribution(biased_good_distribution, old_trends),
        k=1
    )[0]


def create_hotspot_distribution(distribution, indices: List[int]):
    index = indices[len(indices) - 1]
    dec = len(str(distribution[0]).split(".")[1])
    n = len(distribution)
    if n % 2 == 0 or index < -n // 2 or index > n // 2:
        raise ValueError("Invalid distribution length or index")

    hotspot_distribution = [0] * n
    deviations = [abs(x - index) for x in indices]
    bump = 0.75 * numpy.clip(sum(deviations) / len(deviations), 0, 10)
    decay_factor = 0.6

    for i in range(n):
        distance = abs((i - math.floor(n / 2)) - index)
        if distance == 0:
            hotspot_distribution[i] = round(distribution[i] * decay_factor, dec)
        else:
            hotspot_distribution[i] = round(distribution[i] + (bump / distance), dec)
    total = sum(hotspot_distribution)
    return [round(x / total, dec) for x in hotspot_distribution]


class Stocks:
    def __init__(self):
        self.stocks: Dict[str, Dict[str, str | int | List[int]]] = {
            'AAPL': {
                'name': 'Apple',
                'price': 1000,
                'last_price': 1000,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'GOOG': {
                'name': 'Google',
                'price': 400,
                'last_price': 400,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'MSFT': {
                'name': 'Microsoft',
                'price': 1200,
                'last_price': 1200,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'AMZN': {
                'name': 'Amazon',
                'price': 800,
                'last_price': 800,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'TSLA': {
                'name': 'Tesla',
                'price': 100,
                'last_price': 100,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'NVDA': {
                'name': 'Nvidia',
                'price': 1400,
                'last_price': 1400,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'SHEL': {
                'name': 'Shell Oil',
                'price': 10,
                'last_price': 10,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'MCD': {
                'name': 'McDonalds',
                'price': 20,
                'last_price': 20,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            },
            'NFLX': {
                'name': 'Netflix',
                'price': 50,
                'last_price': 50,
                'trends': [wrndm()],
                'lifetime': random.randint(1, 7)
            }
        }

        for ticker, stock in self.stocks.items():
            self.stocks[ticker]['last_price'] = stock['price']
            self.stocks[ticker]['trend'] = stock['trends'][0]

        self.my_stocks: Dict[str, Dict[str, int | List[List[int]]]] = {
            'AAPL': {'amount': 0, 'buying_prices': []},
            'GOOG': {'amount': 0, 'buying_prices': []},
            'MSFT': {'amount': 0, 'buying_prices': []},
            'AMZN': {'amount': 0, 'buying_prices': []},
            'TSLA': {'amount': 0, 'buying_prices': []},
            'NVDA': {'amount': 0, 'buying_prices': []},
            'SHEL': {'amount': 0, 'buying_prices': []},
            'MCD': {'amount': 0, 'buying_prices': []},
            'NFLX': {'amount': 0, 'buying_prices': []}
        }

        self.my_cash = 100

    def get_my_stock(self, ticker: str):
        return self.my_stocks[ticker]

    def get_stock(self, ticker: str):
        return self.stocks[ticker]

    def calculate_buying_price(self, ticker: str):
        my_stock = self.get_my_stock(ticker)
        buying_prices: int = 0
        amount = 0
        for items in my_stock['buying_prices']:
            buying_prices += items[0] * items[1]
            amount += items[0]
        return round(buying_prices / amount, 2)

    def buy_stock(self, ticker: str, amount: int):
        cost = self.stocks[ticker]['price'] * amount
        if self.my_cash >= cost:
            self.my_cash -= cost
            self.my_stocks[ticker]['amount'] += amount
            self.my_stocks[ticker]['buying_prices'].append([amount, self.stocks[ticker]['price']])

            print(self.stocks[ticker]['price'])
            print(self.calculate_buying_price(ticker))
            return True
        else:
            return False

    def has_stock(self, ticker: str, amount: int):
        return self.my_stocks[ticker]['amount'] >= amount

    def sell_stock(self, ticker: str, amount: int):
        if self.has_stock(ticker, amount):
            self.my_cash += self.stocks[ticker]['price'] * amount
            self.my_stocks[ticker]['amount'] -= amount
            # print(self.my_stocks[ticker]['buying_prices'])
            for t in range(amount, 0, -1):
                first = self.my_stocks[ticker]['buying_prices'][0]
                self.my_stocks[ticker]['buying_prices'][0][0] -= 1
                if first[0] == 0:
                    self.my_stocks[ticker]['buying_prices'].pop(0)
            # print(self.my_stocks[ticker]['buying_prices'])
            return True
        else:
            return False

    def set_trend(self, ticker: str, trends: List[int]):
        new_trend = wrndm(trends)
        if len(self.stocks[ticker]['trends']) > 3:
            self.stocks[ticker]['trends'].pop(0)
        self.stocks[ticker]['trends'].append(new_trend)
        self.stocks[ticker]['trend'] = new_trend

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
                self.set_trend(ticker, self.stocks[ticker]['trends'])
                self.stocks[ticker]['lifetime'] = get_lifetime(self.stocks[ticker]['trend'])
            else:
                self.stocks[ticker]['lifetime'] -= 1

            d: float

            if self.stocks[ticker]['trend'] == -3:
                d = self.stocks[ticker]['price'] * -(random.randint(HIGH[0], HIGH[1]) / 1000)
            elif self.stocks[ticker]['trend'] == -2:
                d = self.stocks[ticker]['price'] * -(random.randint(MED[0], MED[1]) / 1000)
            elif self.stocks[ticker]['trend'] == -1:
                d = self.stocks[ticker]['price'] * -(random.randint(LOW[0], LOW[1]) / 1000)
            elif self.stocks[ticker]['trend'] == 0:
                d = 0
            elif self.stocks[ticker]['trend'] == 1:
                d = self.stocks[ticker]['price'] * (random.randint(LOW[0], LOW[1]) / 1000)
            elif self.stocks[ticker]['trend'] == 2:
                d = self.stocks[ticker]['price'] * (random.randint(MED[0], MED[1]) / 1000)
            elif self.stocks[ticker]['trend'] == 3:
                d = self.stocks[ticker]['price'] * (random.randint(HIGH[0], HIGH[1]) / 1000)
            else:
                raise Exception(f"Invalid trend: {self.stocks[ticker]['trend']}")

            self.stocks[ticker]['last_price'] = self.stocks[ticker]['price']
            self.stocks[ticker]['price'] += d
            self.stocks[ticker]['price'] = numpy.clip(self.stocks[ticker]['price'], 0, 10000)

            #  Source: https://stackoverflow.com/a/30926930/18007885
            def get_change(current, previous):
                if current == previous:
                    return 0
                try:
                    return ((current - previous) / previous) * 100.0
                except ZeroDivisionError:
                    return 0

            self.stocks[ticker]['change'] = round(
                get_change(self.stocks[ticker]['price'], self.stocks[ticker]['last_price']), 2)  # changes[ticker]

            # sys.exit()

        return changes
