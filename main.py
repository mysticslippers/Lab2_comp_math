# Лабораторная работа №2 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

import numpy as np
import matplotlib.pyplot as plt

FILE_PATH = "iofiles/input.txt"

def plot(x, y):
    """Отрисовать график по заданным x и y."""
    plt.gcf().canvas.set_window_title("График функции")

    ax = plt.gca()

    for spine in ['left', 'bottom', 'right', 'top']:
        ax.spines[spine].set_color('none' if spine in ['right', 'top'] else 'black')

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    ax.plot(1, 0, marker=">", ms=5, color='k', transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, marker="^", ms=5, color='k', transform=ax.get_xaxis_transform(), clip_on=False)

    plt.plot(x, y)
    plt.show(block=False)


def get_func(function_num):
    """ Получить выбранную функцию. """
    functions = {
        '1': (np.linspace(-1, 3, 200), lambda x: x ** 3 - 2.92 * (x ** 2) + 1.435 * x + 0.791),
        '2': (np.linspace(-3, 2, 200), lambda x: x ** 3 - x + 4),
        '3': (np.linspace(-20, 20, 200), lambda x: np.sin(x) + 0.1)
    }

    return functions.get(function_num, (None, None))


def check_interval(a, b, function):
    """ Проверить корректность отрезка для функции. """
    if a == b:
        raise ArithmeticError("Границы интервала не могут быть равны!")
    if function(a) * function(b) > 0:
        raise AttributeError("Функция должна менять знак на границах интервала!")


def get_data_file():
    """ Получить данные из файла """
    with open(FILE_PATH, 'rt') as fin:
        try:
            data = {}
            function_data = get_func(fin.readline().strip())
            if function_data is None:
                raise ValueError("Функция не распознана!")
            x, function = function_data
            plot(x, function(x))
            data['function'] = function

            method = fin.readline().strip()
            if method not in {'1', '2', '3'}:
                raise ValueError("Метод должен быть 1, 2 или 3!")
            data["method"] = method

            if method in {'1', '2'}:
                a, b = map(float, fin.readline().strip().split())
                check_interval(a, b, function)
                data['a'], data['b'] = sorted((a, b))

            elif method == '3':
                data['x0'] = float(fin.readline().strip())

            error = float(fin.readline().strip())
            if error < 0:
                raise ArithmeticError("Ошибка должна быть неотрицательной!")
            data['error'] = error

            return data
        except (ValueError, ArithmeticError, AttributeError) as e:
            print(f"Ошибка при получении данных: {e}")
            return None


def select_function():
    """ Выбор функции из списка. """
    print("\nВыберите функцию.")
    print(" 1 - x³ - 2.92x² + 4.435x + 0.791")
    print(" 2 - x³ - x + 4")
    print(" 3 - sin(x) + 0.1")

    while True:
        function_data = get_func(input("Функция: "))
        if function_data is not None:
            return function_data
        print("Выберите функцию из списка.")


def select_method():
    """ Выбор метода решения. """
    print("\nВыберите метод решения.")
    print(" 1 - Метод хорд")
    print(" 2 - Метод секущих")
    print(" 3 - Метод простой итерации")

    while True:
        method = input("Метод решения: ")
        if method in ['1', '2', '3']:
            return method
        print("Выберите метод решения из списка.")


def select_interval(function):
    """ Выбор границ интервала. """
    print("\nВыберите границы интервала.")
    while True:
        try:
            a, b = map(float, input("Границы интервала: ").split())
            if a == b:
                raise ArithmeticError("Границы интервала не могут быть равны.")
            if function(a) * function(b > 0):
                raise AttributeError("Функция должна менять знак на границах интервала.")
            return sorted((a, b))
        except ValueError:
            print("Границы интервала должны быть числами, введенными через пробел!")
        except (ArithmeticError, AttributeError) as e:
            print(e)


def select_initial_approximation():
    while True:
        try:
            x0 = float(input("Начальное приближение: "))
            return x0
        except ValueError:
            print("Начальное приближение должно быть числом!")