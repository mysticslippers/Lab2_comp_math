# Лабораторная работа №2 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

import numpy as np
import matplotlib.pyplot as plt

FILE_PATH = "iofiles/input.txt"


def get_derivative(n, x, f, h=1e-10, cache={}):
    """ Найти значение производной функции с использованием кэширования """
    if n <= 0:
        return None
    elif (n, x) in cache:
        return cache[(n, x)]
    elif n == 1:
        result = (f(x + h) - f(x)) / h
    else:
        result = (get_derivative(n - 1, x + h, f, h, cache) - get_derivative(n - 1, x, f, h, cache)) / h

    cache[(n, x)] = result
    return result


def iteration_method(x0, f, e, maxitr=100):
    """ Метод простой итерации с оптимизациями """
    log = [['x0', 'f(x0)', 'x', 'g(x0)', '|x - x0|']]

    def g(g_x):
        derivative = get_derivative(1, g_x, f)
        if derivative == 0:
            return None
        return g_x + (-1 / derivative) * f(g_x)

    x = g(x0)
    if x is None:
        return None
    log.append([x0, f(x0), x, g(x0), abs(x - x0)])

    itr = 0
    while abs(x - x0) > e and itr < maxitr:
        x0, x_new = x, g(x)
        if x_new is None:
            return None

        log.append([x0, f(x0), x_new, g(x0), abs(x_new - x0)])
        if get_derivative(1, x, g) is None or get_derivative(1, x, g) >= 1:
            return None
        x = x_new
        itr += 1

    return x, f(x), itr, log


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


def select_error_tolerance():
    while True:
        try:
            error = float(input("Погрешность вычисления: "))
            if error <= 0:
                raise ArithmeticError("Погрешность вычисления должна быть положительным числом!")
            return error
        except (ValueError, ArithmeticError) as e:
            print(e)


def get_data_console():
    data = {}
    function = select_function()
    data['function'] = function

    method = select_method()
    data['method'] = method

    if method in ['1', '2']:
        a, b = select_interval(function)
        data['a'] = a
        data['b'] = b
    elif method == '3':
        x0 = select_initial_approximation()
        data['x0'] = x0

    error = select_error_tolerance()
    data['error'] = error

    return data


def main():
    print("\t\tЛабораторная работа #2 (19)")
    print("Численное решение нелинейных уравнений")

    print("\nВзять исходные данные из файла (+) или ввести с клавиатуры (-)?")
    input_choice = input("Режим ввода: ")

    while input_choice not in ('+', '-'):
        print("Введите '+' или '-' для выбора способа ввода.")
        input_choice = input("Режим ввода: ")

    if input_choice == '+':
        data = get_data_file()
        if data is None:
            print("\nПри считывании данных из файла произошла ошибка!")
            print("Режим ввода переключен на ручной!")
            data = get_data_console()
    else:
        data = get_data_console()

    try:
        method_switch = {
            '1': chord_method,
            '2': secant_method,
            '3': iteration_method
        }

        method = method_switch.get(data['method'])

        if method is None:
            print("Недопустимый метод!")
            return

        answer = method(data['a'], data['b'], data['function'], data['error'])

        if answer is None:
            if data['method'] == '2':
                print("Знаки функций и вторых производных не равны ни в 'a', ни в 'b'!")
            elif data['method'] == '3':
                print("Не выполняется условие сходимости!")
            raise ValueError

        print(f"\nКорень уравнения: {answer[0]}")
        print(f"Значение функции в корне: {answer[1]}")
        print(f"Число итераций: {answer[2]}")

        log = input("\nВывести таблицу трассировки? (+ / -)\nТаблица трассировки: ")

        while log not in ('+', '-'):
            print("Введите '+' или '-' для выбора, выводить ли таблицу трассировки.")
            log = input("Таблица трассировки: ")

        if log == '+':
            for row in answer[3]:
                print(' '.join(f'{value:12.3f}' for value in row))

    except ValueError:
        print("Произошла ошибка при вычислении корня уравнения. Проверьте входные данные!")

    input("\n\nНажмите Enter, чтобы выйти.")


main()