#!/usr/bin/env python3
"""Рисунок «WBS умного горшка» в двух профилях — проба стека, не рисунок издания.

Один источник данных (WBS) -> Graphviz dot -> два профиля:
  screen — палитра ГУАП, Arial (веб-версия);
  print  — чёрно-белый, Times New Roman 9 пт, ширина не больше 114 мм (памятка РИЦ).
Выход: wbs_<профиль>.svg и .pdf рядом со скриптом.
Рисунок не масштабируется под ширину: если печатный вариант шире 114 мм, скрипт падает,
иначе кегль молча уменьшился бы ниже 8 пт.

Запуск: python3 docs/metodichka/proba-steka/risunki/wbs_tree.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Те же данные, что в tools/marp/svg/z06_figures.py (сокращённые подписи)
WBS = [
    ("1", "Прототип датчика", ["1.1 Компоненты", "1.2 Схема", "1.3 Программа", "1.4 Корпус"]),
    ("2", "Испытания", ["2.1 Калибровка", "2.2 Протокол"]),
    ("3", "Проверка с пользователями", ["3.1 Три владельца"]),
    ("4", "Отчёт и защита", ["4.1 Отчёт", "4.2 Презентация"]),
    ("5", "Управление проектом", ["5.1 Паспорт, план, журнал"]),
]

PROFILES = {
    # цвета только из BRAND.md: dk2 #002C5F, accent1 #005AAA, белый
    "screen": dict(font="Arial", size=14, ink="#002C5F", line="#005AAA", fill="#FFFFFF",
                   top_fill="#005AAA", top_ink="#FFFFFF", width_in=None),
    # 114 мм = 4,49 дюйма; кегль 9 пт — внутри коридора 8–10 пт
    "print": dict(font="Times New Roman", size=9, ink="#000000", line="#000000", fill="#FFFFFF",
                  top_fill="#D9D9D9", top_ink="#000000", width_in=4.49, compact=True),
}


def wrap(t, n=14):
    """Перенос подписи по словам, строки не длиннее n знаков (для узкого печатного профиля)."""
    out, cur = [], ""
    for w in t.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return "\\n".join(out + [cur])


def dot_source(p):
    lines = [
        "digraph wbs {",
        # печать: дерево слева направо — глубина (3 уровня) по ширине, ветви по высоте
        f'  graph [rankdir={"LR" if p.get("compact") else "TB"}, nodesep=0.08, ranksep=0.2, splines=ortho];',
        f'  node [shape=box, fontname="{p["font"]}", fontsize={p["size"]}, color="{p["line"]}",'
        f' fontcolor="{p["ink"]}", style=filled, fillcolor="{p["fill"]}", margin="0.06,0.03"];',
        f'  edge [color="{p["line"]}", arrowhead=none];',
        f'  root [label="Умный горшок", fillcolor="{p["top_fill"]}", fontcolor="{p["top_ink"]}"];',
    ]
    for code, name, packs in WBS:
        if p.get("compact"):
            # результат — в две строки, его пакеты — одной рамкой со списком
            lines.append(f'  n{code} [label="{wrap(code + " " + name, 16)}"]; root -> n{code};')
            lst = "".join(wrap(pk, 20).replace("\\n", "\\l   ") + "\\l" for pk in packs)
            lines.append(f'  k{code} [label="{lst}"]; n{code} -> k{code};')
            continue
        lines.append(f'  n{code} [label="{code} {name}"]; root -> n{code};')
        prev = f"n{code}"
        for k, pk in enumerate(packs):
            nid = f'p{pk.split()[0].replace(".", "_")}'
            lines.append(f'  {nid} [label="{pk}"]; {prev} -> {nid};')
            prev = nid  # пакеты столбиком под результатом — узко, влезает в 114 мм
    lines.append("}")
    return "\n".join(lines)


if __name__ == "__main__":
    for name, p in PROFILES.items():
        src = dot_source(p)
        if p["width_in"]:
            svg_txt = subprocess.run(["dot", "-Tsvg"], input=src.encode(), capture_output=True, check=True).stdout.decode()
            w_pt = float(svg_txt.split('width="', 1)[1].split("pt", 1)[0])
            limit = p["width_in"] * 72
            if w_pt > limit:
                sys.exit(f"{name}: ширина {w_pt:.0f} pt > {limit:.0f} pt (114 мм) — упростить рисунок")
            print(f"{name}: ширина {w_pt:.0f} pt из {limit:.0f} pt, кегль {p['size']} пт без масштабирования")
        for fmt in ("svg", "pdf"):
            out = os.path.join(HERE, f"wbs_{name}.{fmt}")
            subprocess.run(["dot", f"-T{fmt}", "-o", out], input=src.encode(), check=True)
            print(out)
