# -*- coding: utf-8 -*-
"""Односвязный список на функциях высшего порядка. Задания 2.1–2.15.

Пустой список — None. Узел — замыкание, хранящее голову и хвост.
Встроенные контейнеры не используются для хранения узлов.
"""


def pair(head, tail):
    """2.1. Создать узел без ветвлений и встроенных контейнеров."""
    return lambda selector: selector(head, tail)


def head(lst):
    """2.1. Вернуть голову непустого списка."""
    if lst is None:
        raise ValueError("У пустого списка нет головы")
    return lst(lambda first, rest: first)


def tail(lst):
    """2.1. Вернуть хвост непустого списка."""
    if lst is None:
        raise ValueError("У пустого списка нет хвоста")
    return lst(lambda first, rest: rest)


def make_list(*args):
    """2.2. Создать функциональный список из аргументов по порядку.

    Python сам упаковывает *args в кортеж; узлы хранятся в замыканиях.
    """
    result = None
    for value in reversed(args):
        result = pair(value, result)
    return result


def list_to_string(lst):
    """2.3. Представить элементы строкой вида [1, 2, 3]."""
    def append_text(acc, value):
        return acc + (", " if acc else "") + repr(value)

    return "[" + foldl(append_text, lst, "") + "]"


def list_range(low, high):
    """2.4. Создать список целых чисел от low до high включительно."""
    result = None
    for value in range(high, low - 1, -1):
        result = pair(value, result)
    return result


def foldl(func, lst, acc):
    """2.5. Левая свёртка: func(func(acc, x1), x2), ..."""
    while lst is not None:
        acc = func(acc, head(lst))
        lst = tail(lst)
    return acc


def list_sum(lst):
    """2.6. Вычислить сумму с помощью foldl."""
    return foldl(lambda acc, value: acc + value, lst, 0)


def fact(n):
    """2.7. Вычислить факториал с помощью foldl и list_range."""
    if not isinstance(n, int):
        raise TypeError("Аргумент факториала должен быть целым числом")
    if n < 0:
        raise ValueError("Факториал отрицательного числа не определён")
    return foldl(lambda acc, value: acc * value, list_range(1, n), 1)


def list_to_py(lst):
    """2.8. Преобразовать список в обычный список Python через foldl.

    Встроенный список создаётся только как результат преобразования.
    """
    return foldl(lambda acc, value: acc + [value], lst, [])


def list_reverse(lst):
    """2.9. Построить развёрнутый список с помощью foldl."""
    return foldl(lambda acc, value: pair(value, acc), lst, None)


def foldr(func, lst, acc):
    """2.10. Правая свёртка: func(x1, func(x2, ... acc))."""
    return foldl(
        lambda result, value: func(value, result), list_reverse(lst), acc
    )


def list_map(func, lst):
    """2.11. Применить функцию к элементам с помощью foldr."""
    return foldr(lambda value, acc: pair(func(value), acc), lst, None)


def list_filter(pred, lst):
    """2.12. Отобрать элементы с помощью foldr, сохраняя порядок."""
    return foldr(
        lambda value, acc: pair(value, acc) if pred(value) else acc,
        lst,
        None,
    )


def sum_odd_squares(lst):
    """2.13. Сумма квадратов нечётных через filter, map и sum."""
    return list_sum(list_map(
        lambda value: value * value,
        list_filter(lambda value: value % 2 != 0, lst),
    ))


def list_concat(lst1, lst2):
    """2.14. Соединить списки без изменения исходных узлов."""
    return foldr(lambda value, acc: pair(value, acc), lst1, lst2)


def list_replace(lst, index, value):
    """2.15. Вернуть список с заменой по индексу, начиная с нуля."""
    if not isinstance(index, int):
        raise TypeError("Индекс должен быть целым числом")
    if index < 0:
        raise IndexError("Индекс вне границ списка")

    prefix = None
    current = lst
    for _ in range(index):
        if current is None:
            raise IndexError("Индекс вне границ списка")
        prefix = pair(head(current), prefix)
        current = tail(current)
    if current is None:
        raise IndexError("Индекс вне границ списка")

    replaced = pair(value, tail(current))
    return foldl(lambda acc, item: pair(item, acc), prefix, replaced)


if __name__ == "__main__":
    numbers = make_list(1, 2, 3, 4, 5)
    print("Список:", list_to_string(numbers))
    print("Голова:", head(numbers))
    print("Хвост:", list_to_string(tail(numbers)))
    print("Диапазон 2–6:", list_to_string(list_range(2, 6)))
    print("Сумма:", list_sum(numbers))
    print("Факториал 5:", fact(5))
    print("Список Python:", list_to_py(numbers))
    print("Разворот:", list_to_string(list_reverse(numbers)))
    print("Свёртка справа:", foldr(lambda x, acc: x - acc, numbers, 0))
    print("Квадраты:", list_to_string(list_map(lambda x: x * x, numbers)))
    print("Нечётные:", list_to_string(list_filter(lambda x: x % 2, numbers)))
    print("Сумма квадратов нечётных:", sum_odd_squares(numbers))
    print("Соединение:", list_to_string(list_concat(numbers, make_list(6, 7))))
    print("Замена по индексу 2:", list_to_string(list_replace(numbers, 2, 99)))
