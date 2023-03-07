
import json
import time
from datetime import datetime, timedelta
from http import HTTPStatus

import requests

import exceptions

RETRY_TIME = 5
ENDPOINT = 'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'


def get_latest_price():
    """Получение данных с АПИ Binance о цене ETHUSDT."""
    try:
        response = requests.get(ENDPOINT)
        if response.status_code != HTTPStatus.OK:
            error_message = (
                f'Эндпоинт {ENDPOINT} не доступен,'
                f'http-статус: {response.status_code}'
            )
            raise exceptions.HTTPStatusNotOK(error_message)
        price_eth_usdt = response.json()['price']
    except json.JSONDecodeError as value_error:
        raise exceptions.DecodeError(
            'Декодирование данных JSON',
            f'завершилось ошибкой {value_error}'
        )
    return price_eth_usdt


def main():
    """Основная логика работы."""
    print('==================Начало работы==================')
    print('№---------------Date----------------Price----------')
    price_history = []
    start_date = datetime.now()
    delta = timedelta(minutes=1)
    while True:
        try:
            price = get_latest_price()
            date = datetime.now()
            price_history.append(float(price))
            print(len(price_history), date, price, sep=" || ")
            if date - start_date >= delta:
                max_price = max(price_history)
                if price_history[-1] <= max_price * 0.99:
                    diff = (
                        abs(max_price - price_history[-1]) / price_history[-1]
                    ) * 100.0
                    print(
                    f'Цена упала на {diff}% от максимальной цены за час',
                    f'макс. цена {max_price}, текущая - {price_history[-1]}', 
                    )
                    start_date = datetime.now()
                    price_history = []
                elif price_history[-1] >= max_price * 1.01:
                    diff = (abs(max_price - price_history[-1]) / price_history[-1]) * 100.0
                    print(
                    f'Цена увеличилась на {diff}% от максимальной цены за час',
                    f'макс. цена {max_price}, текущая -- {price_history[-1]}',
                    )
                    start_date = datetime.now()
                    price_history = []
                else:
                    diff = (abs(max_price - price_history[-1]) / price_history[-1]) * 100.0
                    print(
                        f'Максимальная цена за последний час {max_price} ',
                        f'текущая -- {price_history[-1]} '
                        f'разница {round(diff, 3)}%'
                    )
                    start_date = datetime.now()
                    price_history = []
        except Exception as error:
                print(f'Сбой в работе программы: {error}')
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Принудительное завершение программы')