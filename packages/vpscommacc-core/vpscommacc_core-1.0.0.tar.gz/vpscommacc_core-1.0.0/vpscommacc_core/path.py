# -*- coding: utf-8 -*-
import os
import glob


def listdir(directory, deep=False, mask='**/*'):
    """
    Получить все файлы из директории (рекурсивно или нет)

    :param directory: целевая директория
    :type directory: str
    :param deep: рекурсивно или нет
    :type deep: bool
    :param mask: маска поиска ('**/*', '**/*.txt', etc)
    :type mask: str

    :rtype: list
    :return: Список файлов с полным путем
    """
    result = []
    pattern = os.sep.join([directory, mask])
    for filename in glob.iglob(pattern, recursive=deep):
        result.append(filename)
    return result


def listdir_os(directory, ext='*', full_path=False):
    """
    Получить все файлы из директории (с полным путем или без)

    :param directory: целевая директория
    :type directory: str
    :param ext: все или с определенным разрешением
    :type ext: str
    :param full_path: с полным путем или нет
    :type full_path: bool

    :rtype: list
    :return: Список файлов (с полным путем или без)
    """
    result = os.listdir(directory)
    if full_path:
        result = []
        for file in os.listdir(directory):
            f_path = ''.join([directory, file])
            result.append(f_path)
    if ext != '*':
        result = list(filter(lambda x: x.endswith(ext), result))
    return result


def dir_get(cur_dir, *args):
    """
    Получить директорию относительно текущей

    :param cur_dir: текущая директория
    :type cur_dir: str
    :param args: набор директорий через запятую
    :type args: str

    :rtype: str
    :return: Полный путь к директории
    """
    cur_dir = cur_dir[:-1]
    return os.sep.join([cur_dir, *args])


def dir_cur(current_file):
    """
    Получить текущую директорию

    :param current_file: __file__
    :type current_file: str

    :rtype: str
    :return: Полный путь к текущей директории
    """
    abs_path = os.path.abspath(current_file)
    f_name = os.path.basename(current_file)
    return abs_path.replace(f_name, '')
