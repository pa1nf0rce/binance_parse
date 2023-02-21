class HTTPStatusNotOK(Exception):
    """Статус ответа не 200."""


class SendMessageError(Exception):
    """Отправка сообщения завершилась ошибкой."""


class DecodeError(Exception):
    """Ошибка декодироваия данных JSON."""


class UnexpectedError(Exception):
    """Непредвиденная ошибка."""


class ReturnedCryptoPriceIsEmpty(Exception):
    """Пустое значение 'price'."""
