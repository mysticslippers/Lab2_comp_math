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

def iteration_method(x0, f, e, maxitr=100):
    """ Метод простой итерации """
    log = [['x0', 'f(x0)', 'x', 'g(x0)', '|x - x0|']]

    def g(g_x):
        return g_x + (-1 / derivative(1, g_x, f)) * f(g_x)

    x = g(x0)
    log.append([x0, f(x0), x, g(x0), abs(x - x0)])

    itr = 0
    while abs(x - x0) > e and itr < maxitr:
        if derivative(1, x, g) >= 1:
            return None
        x0, x = x, g(x)
        log.append([x0, f(x0), x, g(x0), abs(x - x0)])
        itr += 1

    return x, f(x), itr, log

def chord_method(a, b, f, e, maxitr=100):
    """ Метод хорд """
    log = [['a', 'b', 'x', 'f(a)', 'f(b)', 'f(x)', '|x - x0|']]

    if f(a) * derivative(2, a, f) < 0:
        x = a
        fix_x = b
    elif f(b) * derivative(2, a, f) < 0:
        x = b
        fix_x = a
    else:
        x = a - (b - a) / (f(b) - f(a)) * f(a)
        fix_x = None

    x0 = x + 2 * e
    log.append([a, b, x, f(a), f(b), f(x), abs(x - x0)])

    itr = 0
    while abs(x - x0) > e and itr < maxitr:
        if fix_x is None:
            if f(a) * f(x) < 0:
                b = x
            else:
                a = x
            x, x0 = a - (b - a) / (f(b) - f(a)) * f(a), x
            log.append([a, b, x, f(a), f(b), f(x), abs(x - x0)])
        else:
            x, x0 = x - (fix_x - x) / (f(fix_x) - f(x)) * f(x), x
            if fix_x == a:
                log.append([fix_x, x, x, f(fix_x), f(x), f(x), abs(x - x0)])
            else:
                log.append([x, fix_x, x, f(x), f(fix_x), f(x), abs(x - x0)])
        itr += 1

    return x, f(x), itr, log