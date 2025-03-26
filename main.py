# Лабораторная работа №2 (Вариант №8)
# Михайлов Дмитрий Андреевич
# Группа P3206

FILE_IN = "iofiles/input.txt"

def derivative(n, x, f, h=0.00000001):
    """ Найти значение производной функции """
    if n <= 0:
        return None
    elif n == 1:
        return (f(x + h) - f(x)) / h

    return (derivative(n - 1, x + h, f) - derivative(n - 1, x, f)) / h