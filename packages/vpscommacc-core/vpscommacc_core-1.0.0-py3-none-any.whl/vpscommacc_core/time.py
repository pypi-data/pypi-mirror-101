# -*- coding: utf-8 -*-
import datetime
import time


def day_week():
    """
    Получить порядковый номер дня недели

    :rtype int
    :return: Число 1, 2, 3, 4, 5, 6, 7
    """
    return datetime.datetime.today().isoweekday()


def now_eng(hms=False):
    """
    Дата и время в английском формате

    :rtype: str
    :return: Образец: 03.01.2021 11:32:47
    """
    pattern = "%Y-%m-%d %H:%M:%S" if hms else "%Y-%m-%d"
    return now().strftime(pattern)


def now_rus(hms=False):
    """
    Дата и время в русском формате

    :rtype: str
    :return: Образец: 03.01.2021 11:32:47
    """
    pattern = "%d.%m.%Y %H:%M:%S" if hms else "%d.%m.%Y"
    return now().strftime(pattern)


def now():
    """
    Получить текущие дату и время

    :rtype: datetime.datetime
    :return: Образец: 2021-01-03 11:22:25.248840
    """
    return datetime.datetime.now()


def unix():
    """
    Получить UNIX-метку

    :rtype: int
    :return: Количество секунд, прошедших с 1 января 1970 года
    """
    return int(time.time())
