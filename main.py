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
