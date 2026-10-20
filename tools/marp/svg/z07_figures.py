#!/usr/bin/env python3
"""Рисунки для колоды занятия 7 «Диаграмма Ганта и критический путь» -> zanyatiya/img/z07_*.svg.

Палитра и хелперы — те же, что для занятия 5 (z05_figures.py): только цвета ГУАП, Arial,
текст 17–24 px при показе 1:1 на слайде 1280x720. Расписание умного горшка — то же, что в
конспекте занятия 7 и в примере таблицы WBS (занятие 6).

Запуск: python3 tools/marp/svg/z07_figures.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from z05_figures import INK, BLUE, GREEN, RED, W, LIGHT, LINE, text, node, arrow, svg, save  # noqa: E402

# (код, подпись, старт (неделя от 0), длительность, критический, ответственный)
TASKS = [
    ("1.1", "Компоненты куплены", 0, 1, True, "аналитик"),
    ("1.2", "Схема проверена", 1, 1, True, "технический эксперт"),
    ("1.3", "Программа порога", 2, 1, True, "технический эксперт"),
    ("1.4", "Корпус с индикатором", 1, 1, False, "лидер"),
    ("2.1", "Калибровка датчика", 2, 1, True, "технический эксперт"),
    ("2.2", "10 циклов полива", 3, 2, True, "аналитик"),
    ("3.1", "Проба у владельцев", 5, 1, True, "коммуникатор"),
    ("4.1", "Отчёт", 6, 1, True, "аналитик"),
    ("4.2", "Презентация и питч", 7, 1, True, "коммуникатор"),
]
LABEL_W, CW, ROW, HEAD = 330, 88, 38, 40


def grid(tasks, weeks, label_w=LABEL_W, cw=CW, row=ROW, head=HEAD, title="неделя"):
    b = text(8, head / 2, [title], 18, BLUE, True, anchor="start")
    for w in range(weeks):
        x = label_w + w * cw
        b += text(x + cw / 2, head / 2, [str(w + 1)], 20, INK, True)
    for i, t in enumerate(tasks):
        y = head + i * row
        if i % 2 == 0:
            b += f'<rect x="0" y="{y}" width="{label_w + weeks * cw}" height="{row}" fill="{LIGHT}"/>'
        b += text(8, y + row / 2, [f"{t[0]} {t[1]}"], 18, INK, anchor="start")
    for w in range(weeks + 1):
        x = label_w + w * cw
        b += f'<line x1="{x}" y1="{head}" x2="{x}" y2="{head + len(tasks) * row}" stroke="{LINE}" stroke-width="1.5"/>'
    return b


def bar(x, y, w, color, h=26, dash=False, fill=None):
    if dash:
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill or "none"}" '
                f'stroke="{color}" stroke-width="2.5" stroke-dasharray="7 5"/>')
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{color}"/>'


def gantt(mode):
    n = len(TASKS)
    b = grid(TASKS, 8)
    for i, (code, _, s, d, crit, _) in enumerate(TASKS):
        y = HEAD + i * ROW + (ROW - 26) / 2
        x = LABEL_W + s * CW + 3
        color = RED if (mode in ("crit", "miles") and crit) else BLUE
        b += bar(x, y, d * CW - 6, color)
        if mode in ("crit", "miles") and not crit:
            b += bar(x + CW, y, CW - 6, BLUE, dash=True)
            b += text(x + CW + (CW - 6) / 2, y + 13, ["запас"], 17, BLUE, True)
    h = HEAD + n * ROW
    if mode == "crit":
        b += bar(10, h + 14, 36, RED, h=22)
        b += text(56, h + 25, ["критический путь: срок проекта — 8 недель"], 19, INK, anchor="start")
        b += bar(560, h + 14, 36, BLUE, h=22)
        b += text(606, h + 25, ["есть запас: можно сдвинуть"], 19, INK, anchor="start")
        return svg(LABEL_W + 8 * CW, h + 50, b)
    if mode == "miles":
        marks = ((3, "конец 3-й недели: прототип собран и откалиброван"),
                 (5, "конец 5-й недели: испытания закончены"),
                 (8, "конец 8-й недели: отчёт сдан, питч готов"))
        for k, (wk, label) in enumerate(marks):
            x = LABEL_W + wk * CW
            b += f'<line x1="{x}" y1="{HEAD - 6}" x2="{x}" y2="{h}" stroke="{GREEN}" stroke-width="3" stroke-dasharray="8 5"/>'
            b += f'<rect x="{x - 10}" y="{HEAD - 14}" width="20" height="20" fill="{GREEN}" transform="rotate(45 {x} {HEAD - 4})"/>'
            b += f'<rect x="12" y="{h + 14 + k * 30}" width="18" height="18" fill="{GREEN}" transform="rotate(45 21 {h + 23 + k * 30})"/>'
            b += text(46, h + 23 + k * 30, [label], 19, INK, anchor="start")
        return svg(LABEL_W + 8 * CW + 24, h + 100, b)
    return svg(LABEL_W + 8 * CW, h + 6, b)


# ── 1. Хук: график с ошибкой ───────────────────────────────────────────────
def hook():
    tasks = [("1.2", "Схема проверена", 0, 1, 0, ""), ("2.1", "Калибровка датчика", 0, 1, 0, ""),
             ("1.3", "Программа порога", 1, 1, 0, ""), ("2.2", "10 циклов полива", 0, 2, 0, "")]
    b = f'<rect x="0" y="0" width="{LABEL_W + 4 * CW}" height="{HEAD + 4 * ROW + 6}" rx="12" fill="{W}"/>'
    b += grid(tasks, 4)
    for i, (_, _, s, d, _, _) in enumerate(tasks):
        b += bar(LABEL_W + s * CW + 3, HEAD + i * ROW + (ROW - 26) / 2, d * CW - 6, BLUE)
    return svg(LABEL_W + 4 * CW, HEAD + 4 * ROW + 6, b)


# ── 2. Место Ганта в планировании ──────────────────────────────────────────
def place():
    b = ""
    steps = ("Дерево целей: что берём", "WBS: что делаем и предъявляем", "Ганта: когда", "Смета и риски")
    for i, t in enumerate(steps):
        cx = 130 + i * 296
        hi = i == 2
        n, _ = node(cx, 70, 250, t, h=110, fill=BLUE if hi else W, stroke=BLUE if hi else INK,
                    tc=W if hi else INK, bold=hi, fs=22)
        b += n
        if i < 3:
            b += arrow(cx + 128, 70, cx + 170, 70, INK, 3)
    b += text(722, 160, ["сегодня"], 22, BLUE, True)
    return svg(1150, 180, b)


# ── 3. Зависимость «окончание → начало» ────────────────────────────────────
def dep():
    b = ""
    n, _ = node(200, 60, 300, "1.1 Компоненты куплены", h=72, fill=LIGHT, bold=True, fs=22)
    b += n
    n, _ = node(640, 60, 300, "1.2 Схема собрана", h=72, fill=W, stroke=BLUE, bold=True, fs=22)
    b += n
    b += arrow(352, 60, 488, 60, BLUE, 4)
    b += text(420, 24, ["ждёт"], 20, BLUE, True)
    b += text(200, 115, ["предшественник"], 20, INK)
    b += text(640, 115, ["зависит от 1.1"], 20, BLUE, True)
    b += bar(160, 160, 200, INK)
    b += bar(360, 200, 200, BLUE)
    b += f'<line x1="360" y1="150" x2="360" y2="236" stroke="{RED}" stroke-width="3" stroke-dasharray="6 5"/>'
    b += text(560, 173, ["1.1 закончилась"], 19, INK, anchor="start")
    b += text(570, 213, ["только теперь можно начать 1.2"], 19, BLUE, True, anchor="start")
    return svg(940, 250, b)


# ── 4. Нагрузка по людям ───────────────────────────────────────────────────
def people():
    lanes = ["аналитик", "технический эксперт", "лидер", "коммуникатор"]
    tasks = [(p, "", 0, 0, 0, 0) for p in lanes]
    b = grid([(p, "", 0, 0, 0, 0) for p in lanes], 8, label_w=240, cw=100, row=64)
    LW, C, R = 240, 100, 64
    # убираем код из подписи: grid пишет «код подпись» — перерисуем чище
    b = grid([("", p, 0, 0, 0, 0) for p in lanes], 8, label_w=LW, cw=C, row=R)
    for ti, t in enumerate(TASKS):
        code, _, s, d, _, who = t
        lane = lanes.index(who)
        y = HEAD + lane * R
        x = LW + s * C + 3
        conflict = code in ("1.3", "2.1")
        if conflict:
            yy = y + 6 + (0 if code == "1.3" else 26)
            b += bar(x, yy, C - 6, RED, h=24)
            b += text(x + (C - 6) / 2, yy + 12, [code], 18, W, True)
        else:
            yy = y + (R - 30) / 2
            b += bar(x, yy, d * C - 6, BLUE, h=30)
            b += text(x + (d * C - 6) / 2, yy + 15, [code], 18, W, True)
    cx = LW + 2 * C
    b += (f'<rect x="{cx - 1}" y="{HEAD + R + 2}" width="{C + 2}" height="{R - 4}" rx="8" fill="none" '
          f'stroke="{RED}" stroke-width="3" stroke-dasharray="8 5"/>')
    b += text(cx + C + 14, HEAD + R + R / 2, ["3-я неделя: две работы у одного человека"], 20, RED, True, anchor="start")
    return svg(LW + 8 * C, HEAD + 4 * R + 6, b)


# ── 5. Буфер: один, в конце критического пути ──────────────────────────────
def buffer():
    seq = [("1.1", 1), ("1.2", 1), ("1.3", 1), ("2.2", 1), ("3.1", 1), ("4.1", 1), ("4.2", 1)]
    CWb, X0, Y = 120, 24, 100
    b = text(X0, 40, ["критический путь, пакет 2.2 сокращён до одной недели"], 20, INK, True, anchor="start")
    for i, (code, d) in enumerate(seq):
        b += bar(X0 + i * CWb + 3, Y, CWb - 6, RED, h=52)
        b += text(X0 + i * CWb + CWb / 2, Y + 26, [code], 22, W, True)
    xb = X0 + 7 * CWb
    b += bar(xb + 3, Y, CWb - 6, GREEN, h=52, dash=True)
    b += text(xb + CWb / 2, Y + 26, ["буфер"], 22, GREEN, True)
    xe = xb + CWb
    b += f'<line x1="{xe}" y1="{Y - 30}" x2="{xe}" y2="{Y + 90}" stroke="{INK}" stroke-width="4"/>'
    b += text(xe - 6, Y + 112, ["защита 26.12"], 22, INK, True, anchor="end")
    b += text(X0 + 3.5 * CWb, Y + 112, ["7 недель работы"], 20, RED, True)
    b += text(xb + CWb / 2, Y + 150, ["1 неделя"], 20, GREEN, True)
    return svg(X0 + 8 * CWb + 24, Y + 180, b)


# ── 6. Лист для Ганта (пустой) ─────────────────────────────────────────────
def sheet():
    LW, C, R = 160, 50, 40
    b = f'<rect x="16" y="16" width="584" height="414" rx="6" fill="{LINE}" opacity=".6"/>'
    b += f'<rect x="8" y="8" width="584" height="414" rx="6" fill="{W}" stroke="{INK}" stroke-width="3"/>'
    b += text(30, 36, ["А4"], 20, BLUE, True, anchor="start")
    for w in range(8):
        b += text(LW + 20 + w * C + C / 2, 36, [str(w + 1)], 17, INK, True)
    for i in range(7):
        y = 56 + i * R
        b += f'<line x1="24" y1="{y}" x2="576" y2="{y}" stroke="{LINE}" stroke-width="2"/>'
        b += text(30, y + R / 2, ["пакет"], 17, BLUE, anchor="start")
    for w in range(9):
        x = LW + 20 + w * C
        b += f'<line x1="{x}" y1="56" x2="{x}" y2="{56 + 7 * R}" stroke="{LINE}" stroke-width="1.5"/>'
    b += ('<defs><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" '
          f'patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="{INK}" stroke-width="3"/></pattern></defs>')
    b += bar(LW + 20 + 2 * C + 3, 56 + R + 7, 2 * C - 6, INK, h=26, dash=True, fill="url(#hatch)")
    b += text(300, 408, ["штриховкой — критический путь"], 18, INK, True)
    return svg(600, 430, b)


if __name__ == "__main__":
    save("z07_hook.svg", hook())
    save("z07_place.svg", place())
    save("z07_dep.svg", dep())
    save("z07_gantt1.svg", gantt("plain"))
    save("z07_gantt2.svg", gantt("crit"))
    save("z07_gantt3.svg", gantt("miles"))
    save("z07_people.svg", people())
    save("z07_buffer.svg", buffer())
    save("z07_sheet.svg", sheet())
