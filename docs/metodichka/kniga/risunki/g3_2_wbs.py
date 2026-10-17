#!/usr/bin/env python3
"""Рисунки главы 3.2 «Иерархическая структура работ» в двух профилях (экран, печать).

Данные умного горшка — те же, что в методических указаниях занятия 6
(zanyatiya/Zanyatie_06_WBS_Konspekt.md) и в tools/marp/svg/z06_figures.py.
Запуск: python3 docs/metodichka/kniga/risunki/g3_2_wbs.py  -> risunki/out/*.svg, *.pdf
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from profil import accent, head, render, wrap  # noqa: E402

WBS = [
    ("1", "Прототип датчика с индикатором", ["1.1 Компоненты", "1.2 Схема", "1.3 Программа", "1.4 Корпус"]),
    ("2", "Испытания", ["2.1 Калибровка", "2.2 Протокол 10 циклов полива"]),
    ("3", "Проверка с пользователями", ["3.1 Три владельца попробовали"]),
    ("4", "Отчёт и защита", ["4.1 Отчёт", "4.2 Презентация"]),
    ("5", "Управление проектом", ["5.1 Паспорт, план, журнал"]),
]


def mesto(p):
    """Где структура работ в цепочке планирования: выход предыдущего шага — вход следующего."""
    steps = ["Паспорт", "Дерево целей: что берём", "Структура работ: что делаем", "Диаграмма Ганта: когда", "Смета и риски"]
    b = head(p, rankdir="LR", nodesep=0.1, ranksep=0.12)
    for i, s in enumerate(steps):
        extra = accent(p) if i == 2 else ""
        b += f'n{i} [label="{wrap(s, 9)}", {extra}];\n'
        if i:
            b += f"n{i - 1} -> n{i} [arrowsize=0.6];\n"
    return b


def derevo(p):
    """Структура работ горшка: проект — крупные результаты — пакеты (слева направо, чтобы уложиться в 114 мм)."""
    b = head(p, rankdir="LR", nodesep=0.03, ranksep=0.22)
    b += 'node [margin="0.05,0.015"];\n'  # плотнее по вертикали: пример и таблица — на одной странице разворота
    b += f'root [label="{wrap("Умный горшок: датчик влажности с индикатором", 12)}", {accent(p)}];\n'
    for code, name, packs in WBS:
        b += f'n{code} [label="{wrap(code + " " + name, 16)}"]; root -> n{code} [arrowhead=none];\n'
        lst = "".join(wrap(pk, 22).replace("\\n", "\\l     ") + "\\l" for pk in packs)
        b += f'k{code} [label="{lst}"]; n{code} -> k{code} [arrowhead=none];\n'
    return b


def sto(p):
    """Правило 100 %: пакеты в сумме дают результат; то, что за границей, в структуру работ не входит."""
    b = head(p, rankdir="TB", nodesep=0.12, ranksep=0.3)
    b += f'r [label="1 Прототип датчика с индикатором", {accent(p)}];\n'
    for pk in WBS[0][2]:
        k = pk.split()[0].replace(".", "_")
        b += f'p{k} [label="{wrap(pk, 11)}"]; r -> p{k} [arrowhead=none];\n'
    b += (f'g [label="{wrap("Насос и автополив — за границей, в структуре работ их нет", 30)}", style="dashed", '
          f'color="{p["warn"]}", fontcolor="{p["warn"]}"];\n')
    b += "p1_2 -> g [style=invis];\n"  # граница — строкой ниже пакетов
    return b


def list_a4(p):
    """Схема листа «Структура работ» А4: лицевая сторона — дерево, оборот — таблица пакетов."""
    b = head(p, rankdir="TB", nodesep=0.12, ranksep=0.22)
    b += f'pr [label="Проект: результат из паспорта", {accent(p)}];\n'
    for i in range(1, 4):
        b += f'r{i} [label="{i} Крупный\\nрезультат"]; pr -> r{i} [arrowhead=none];\n'
        b += f'k{i} [label="{i}.1 Пакет\\l{i}.2 Пакет\\l", style="dashed"]; r{i} -> k{i} [arrowhead=none];\n'
    b += (f'ob [label="Оборот листа — таблица пакетов:\\lкод · пакет · что предъявляем ·\\lответственный · длительность · зависит от\\l", '
          f'shape=note];\n')
    b += "k2 -> ob [style=invis];\n"
    return b


if __name__ == "__main__":
    render("g3_2_mesto", mesto)
    render("g3_2_derevo", derevo)
    render("g3_2_sto", sto)
    render("g3_2_list", list_a4)
