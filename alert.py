import os
import json
import time
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from prettytable import PrettyTable
from colorama import Fore, init
from datetime import datetime, timedelta
from playsound import playsound

# PrettyTable Colors
R = "\033[0;31;40m"  # RED
G = "\033[0;32;40m"  # GREEN
N = "\033[0m"  # RESET

DEFAULT_TICKER = 'BTC'
DEFAULT_CONVERT = 'USDT'
DEFAULT_DELTA_TRIGGER = 0.01
DEFAULT_SOUNDFILE = 'alert.wav'
DEFAULT_DELTA_REFRESH_SECONDS = 30
MAX_ROWS_DISPLAYED = 10


class BitcoinAlert():
    endpoint = 'https://api.binance.com/api/v3/avgPrice'

    @staticmethod
    def __getPercent(price, prev):
        return ((price - prev) * 100 / price)

    @staticmethod
    def __getLogo():
        os.system('cls' if os.name == 'nt' else 'clear')
        return Fore.YELLOW + """\
            """ + Fore.RESET

    def __init__(self, ticker, convert, delta, sound_file, delta_refresh_seconds):
        self.ticker = ticker
        self.convert = convert
        self.delta = delta
        self.sound_file = sound_file
        self.delta_refresh_seconds = delta_refresh_seconds

    def start(self):
        try:
            init()  # colorama init
            table = PrettyTable(['Asset', 'Previous Value (' + self.convert + ')',
                                 'New Value (' + self.convert + ')', 'Last Updated', 'Percentage (%)'], )
            previous = 0.0
            n_prev = 0
            offset = 0

            while True:
                response = requests.get(
                    f'{self.endpoint}?symbol={self.ticker}{self.convert}').json()
                price = eval(response['price'])
                percent = self.__getPercent(price, previous)
                table.add_row([f'{self.ticker}', f'{round(previous, 2):,}',
                               f'{round(price, 2):,}', datetime.now().strftime("%H:%M:%S"),
                               G+f'+{round(percent, 3)}'+N if percent > 0 else R+f'{round(percent, 3)}'+N])

                n_prev += 1
                if n_prev >= MAX_ROWS_DISPLAYED:
                    offset += 1

                next_update = (datetime.now() + timedelta(seconds=self.delta_refresh_seconds)).strftime("%H:%M:%S")
                print(f'{self.__getLogo()}\n{table.get_string(start=offset, end=MAX_ROWS_DISPLAYED + offset)}\
                    \n\nAPI refreshes every {self.delta_refresh_seconds} seconds (next update at {next_update})')

                if (abs(percent) > self.delta):
                    playsound(self.sound_file)
                previous = price
                time.sleep(self.delta_refresh_seconds)

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)


if __name__ == "__main__":
    BitcoinAlert(DEFAULT_TICKER, DEFAULT_CONVERT, DEFAULT_DELTA_TRIGGER,
                 DEFAULT_SOUNDFILE, DEFAULT_DELTA_REFRESH_SECONDS).start()
