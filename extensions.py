import requests
import json
from config import keys, access_key


class ConvertionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'http://api.currencylayer.com/live?access_key={access_key}&currencies={base_ticker},{quote_ticker}&format=1')

        usd = json.loads(r.content).get('quotes')

        total_base = round(((usd.get(f'USD{quote_ticker}') / usd.get(f'USD{base_ticker}')) * amount), 4)

        return total_base
