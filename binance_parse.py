
import json
import time
from datetime import datetime
from http import HTTPStatus

import requests

import exceptions

RETRY_TIME = 10
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
    except requests.exceptions.RequestException as error_message:
        raise exceptions.UnexpectedError(
            f'Запрос c параметрами {ENDPOINT}',
            f'завершился ошибкой({error_message})'
        )
    except json.JSONDecodeError as value_error:
        raise exceptions.DecodeError(
            'Декодирование данных JSON',
            f'завершилось ошибкой {value_error}'
        )
    return price_eth_usdt


def main():
    """Основная логика работы."""
    print('==================Начало работы==================')
    print('№---------------Date--------------Price----------')
    price_history = []
    while True:
        try:
            price = get_latest_price()
            date = datetime.now()
            price_history.append(float(price))

            print(len(price_history), date, price, sep=' || ')
            if len(price_history) ==2:
                if price_history[-1] < max(price_history) * 0.99:
                    diff = (abs(max(price_history) - price_history[-1]) / price_history[-1]) * 100.0
                    print(
                    f'Цена упала на {diff}% от максимальной цены за час',
                    f'макс. цена {max(price_history)}, текущая -- {price_history[-1]}', 
                    )
                    price_history = []
                elif price_history[-1] > max(price_history) * 1.01:
                    diff = (abs(max(price_history) - price_history[-1]) / price_history[-1]) * 100.0
                    print(
                    f'Цена увеличилась на {diff}% от максимальной цены за час',
                    f'макс. цена {max(price_history)}, текущая -- {price_history[-1]}',
                    )
                    price_history = []
                else:
                    diff = (abs(max(price_history) - price_history[-1]) / price_history[-1]) * 100.0
                    print(
                        f'Максимальная цена за последний час {max(price_history)} ',
                        f'текущая -- {price_history[-1]} '
                        f'разница {round(diff, 3)}%'
                    )
                    price_history = []
        except Exception as error:
                message = f'Сбой в работе программы: {error}'
                print(message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Принудительное завершение программы')