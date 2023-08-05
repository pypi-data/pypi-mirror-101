# -*- coding: utf-8 -*-
import csv


def csv_sort(reader, column_id, desc=True):
    """
    Отсортировать csv-файл по определенной колонке

    :param reader:
    :param column_id:
    :param desc:

    :return:
    """
    return sorted(reader, key=lambda row: row[column_id], reverse=desc)


def csv_write(f_name, row, mode='a'):
    """
    Записать одну строку в csv-файл

    :param f_name: Путь к файлу
    :type f_name: str
    :param row: Список
    :type row: list
    :param mode: Режим работы с файлом
    :type mode: str

    :rtype None
    :return: Запись в файл
    """
    with open(f_name, mode, newline='', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(row)


def csv_write_rows(f_name, rows, mode='a'):
    """
    Записать несколько строк в csv-файл

    :param f_name: Путь к файлу
    :type f_name: str
    :param rows: Список списков
    :type rows: list
    :param mode: Режим работы с файлом
    :type mode: str

    :rtype None
    :return: Запись в файл
    """
    with open(f_name, mode, newline='', encoding="utf8") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(rows)
