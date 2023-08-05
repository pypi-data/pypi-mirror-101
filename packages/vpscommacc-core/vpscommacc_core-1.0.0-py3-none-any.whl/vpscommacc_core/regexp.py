# -*- coding: utf-8 -*-
import re


def clear_html(html):
    """
    Очистить строку от всех html-тегов

    :param html:
    :type html: str

    :rtype str
    :return: Строка без html
    """
    regex = re.compile(r'<.*?>', re.DOTALL)
    return regex.sub('', html)


def all_chars(txt, ru=True):
    """
    Получить все символы из текста (кириллица или латиница)

    :param txt: строка
    :type txt: str

    :rtype: list
    :return: Список: ['йцу', 'фыв', 'ячс'] / ['qwe', 'asd', 'zxc']
    """
    regex_char = re.compile('[а-яА-яёЁ]+') if ru else re.compile('[a-zA-Z]+')
    return regex_char.findall(txt)


def all_num(txt):
    """
    Получить все цифры из текста

    :param txt: строка
    :type txt: str

    :rtype: list
    :return: Список: ['123', '456', '789']
    """
    regex_num = re.compile('\d+')
    return regex_num.findall(txt)
