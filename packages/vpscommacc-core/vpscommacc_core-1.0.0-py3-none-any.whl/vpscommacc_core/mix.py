# -*- coding: utf-8 -*-
import csv


def diff(list_one, list_two):
    """
    Вычесть из первого списка элементы второго списка

    :param list_one:
    :type list_one: list
    :param list_two:
    :type list_two: list

    :rtype list
    :return: Элементы 1-го списка, которых нет во 2-м списке
    """
    return list(set(list_one) - set(list_two))


def intersect(list_one, list_two):
    """
    Найти элементы присутствующие в обоих списках

    :param list_one:
    :type list_one: list
    :param list_two:
    :type list_two: list

    :rtype list
    :return: Общие для двух списков элементы
    """
    return [x for x in list_one if x in list_two]
