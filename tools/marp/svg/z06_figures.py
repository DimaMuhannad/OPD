#!/usr/bin/env python3
"""Рисунки для колоды занятия 6 «Иерархическая структура работ» -> zanyatiya/img/z06_*.svg.

Палитра и хелперы — те же, что для занятия 5 (z05_figures.py): только цвета ГУАП, Arial,
текст 18–24 px при показе 1:1 на слайде 1280x720.

Запуск: python3 tools/marp/svg/z06_figures.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from z05_figures import INK, BLUE, GREEN, RED, W, LIGHT, LINE, text, node, arrow, svg, save  # noqa: E402

# WBS умного горшка: (код, крупный результат, [пакеты]); забывают первыми — 4 и 5
WBS = [
    ("1", "Прототип датчика с индикатором", ["1.1 Компоненты с ценами", "1.2 Схема проверена", "1.3 Программа порога", "1.4 Корпус с индикатором"]),
    ("2", "Испытания", ["2.1 Калибровка датчика", "2.2 Протокол 10 циклов полива"]),
    ("3", "Проверка с пользователями", ["3.1 Три владельца попробовали"]),
    ("4", "Отчёт и защита", ["4.1 Отчёт", "4.2 Презентация"]),
    ("5", "Управление проектом", ["5.1 Паспорт, план, журнал"]),
]
FORGOT = {"4", "5"}


# ── 1. Хук: голосование ────────────────────────────────────────────────────
def hook():
    b = ""
    for i, (tag, t) in enumerate((("А", "Месяц"), ("Б", "Два месяца"), ("В", "До защиты не успеем"))):
        x0 = i * 392
        b += f'<rect x="{x0}" y="0" width="360" height="200" rx="16" fill="{W}"/>'
        b += f'<circle cx="{x0 + 44}" cy="44" r="28" fill="{BLUE}"/>' + text(x0 + 44, 44, [tag], 30, W, True)
        b += text(x0 + 180, 125, [t], 30, INK, True)
    return svg(1144, 200, b)


# ── 2. Целиком срок не назвать — из частей можно ───────────────────────────
def whole():
    b = ""
    n, _ = node(170, 190, 300, "Проект целиком", h=230, fill=LIGHT, fs=26, bold=True)
    b += n + text(170, 265, ["? недель"], 34, RED, True)
    b += arrow(345, 190, 455, 190, BLUE, 4)
    parts = (("Компоненты", "1 нед."), ("Схема", "1 нед."), ("Программа", "1 нед."), ("Корпус", "1 нед."),
             ("Калибровка", "1 нед."), ("10 циклов полива", "2 нед."), ("Пробы у владельцев", "1 нед."), ("Отчёт и питч", "2 нед."))
    for i, (t, d) in enumerate(parts):
        cx, cy = 560 + (i % 2) * 250, 40 + (i // 2) * 92
        b += (f'<rect x="{cx - 112}" y="{cy - 36}" width="224" height="72" rx="10" fill="{W}" '
              f'stroke="{INK}" stroke-width="2.5"/>')
        b += text(cx, cy - 12, [t], 20, INK, True) + text(cx, cy + 16, [d], 20, BLUE, True)
    b += text(685, 405, ["≈ 10 недель — уже можно сравнить с датой защиты"], 22, GREEN, True)
    return svg(1100, 430, b)


# ── 3. Место WBS в планировании ────────────────────────────────────────────
def place():
    b = ""
    steps = ("Дерево целей: что берём", "WBS: что делаем и предъявляем", "Ганта: когда", "Смета и риски")
    for i, t in enumerate(steps):
        cx = 130 + i * 296
        hi = i == 1
        n, _ = node(cx, 70, 250, t, h=110, fill=BLUE if hi else W, stroke=BLUE if hi else INK,
                    tc=W if hi else INK, bold=hi, fs=22)
        b += n
        if i < 3:
            b += arrow(cx + 128, 70, cx + 170, 70, INK, 3)
    b += text(426, 160, ["сегодня"], 22, BLUE, True)
    return svg(1150, 180, b)


# ── 4–6. Дерево WBS горшка по шагам ────────────────────────────────────────
def tree(step):
    b = ""
    CW, X0 = 232, 116
    n, _ = node(X0 + 2 * CW, 42, 520, "Умный горшок: датчик влажности с индикатором", h=66,
                fill=BLUE, stroke=BLUE, tc=W, bold=True, fs=22)
    b += n
    b += f'<line x1="{X0}" y1="98" x2="{X0 + 4 * CW}" y2="98" stroke="{INK}" stroke-width="2.5"/>'
    b += f'<line x1="{X0 + 2 * CW}" y1="76" x2="{X0 + 2 * CW}" y2="98" stroke="{INK}" stroke-width="2.5"/>'
    for i, (code, title, packs) in enumerate(WBS):
        cx = X0 + i * CW
        forgot = code in FORGOT
        ghost = step == 1 and forgot
        if forgot and step >= 2:
            fill, stroke, tc = W, RED, RED
        else:
            fill, stroke, tc = LIGHT, INK, INK
        op = .35 if ghost else 1
        b += f'<line x1="{cx}" y1="98" x2="{cx}" y2="118" stroke="{INK}" stroke-width="2.5" opacity="{op}"/>'
        n, _ = node(cx, 160, 214, f"{code}. {title}", h=84, fill=fill, stroke=stroke, tc=tc, bold=True,
                    fs=20, dash="8 6" if ghost else None, op=op, sw=3 if forgot and step >= 2 else 2.5)
        b += n
        if step >= 3:
            for k, p in enumerate(packs):
                cy = 262 + k * 70
                b += f'<line x1="{cx - 96}" y1="{cy - 70 + (36 if k == 0 else 28)}" x2="{cx - 96}" y2="{cy}" stroke="{LINE}" stroke-width="2.5"/>'
                b += f'<line x1="{cx - 96}" y1="{cy}" x2="{cx - 84}" y2="{cy}" stroke="{LINE}" stroke-width="2.5"/>'
                n, _ = node(cx + 8, cy, 184, p, h=58, fill=W, stroke=BLUE, fs=17, sw=2)
                b += n
    if step == 2:
        b += text(X0 + 3.5 * CW, 232, ["эту работу всё равно придётся сделать"], 20, RED, True)
    return svg(1160, 540 if step >= 3 else 250, b)


# ── 7. Пакет работ: три признака ───────────────────────────────────────────
def package(blank=False):
    b = (f'<rect x="4" y="4" width="560" height="330" rx="14" fill="{W}" stroke="{BLUE}" stroke-width="3"/>'
         f'<rect x="4" y="4" width="560" height="64" rx="14" fill="{BLUE}"/>'
         f'<rect x="4" y="50" width="560" height="18" fill="{BLUE}"/>')
    b += text(284, 36, ["1.2 Схема собрана и проверена"], 24, W, True)
    rows = (("Предъявляем", "фото схемы и показания на 3 образцах почвы"),
            ("Отвечает", "технический эксперт — один человек"),
            ("Займёт", "1 неделя"))
    for i, (k, v) in enumerate(rows):
        y = 118 + i * 82
        b += f'<circle cx="38" cy="{y}" r="16" fill="{GREEN}"/>' + text(38, y, ["✓"], 20, W, True)
        b += text(68, y - 16, [k], 20, BLUE, True, anchor="start")
        b += text(68, y + 14, ["_______________________" if blank and i else v], 20, INK, anchor="start")
    return svg(568, 338, b)


# ── 8. Правило 100 % ───────────────────────────────────────────────────────
def hundred():
    b = ""
    n, _ = node(330, 46, 400, "1. Прототип датчика с индикатором", h=70, fill=LIGHT, bold=True, fs=22)
    b += n
    packs = WBS[0][2]
    for i, p in enumerate(packs):
        cx = 90 + i * 160
        b += f'<line x1="{cx}" y1="150" x2="{330}" y2="82" stroke="{INK}" stroke-width="2"/>'
        n, _ = node(cx, 192, 150, p, h=84, fill=W, stroke=BLUE, fs=18, sw=2)
        b += n
    b += f'<path d="M10,250 Q10,272 40,272 L620,272 Q650,272 650,250" fill="none" stroke="{GREEN}" stroke-width="3"/>'
    b += text(330, 302, ["все пакеты сделаны → прототип готов: 100 %"], 22, GREEN, True)
    b += (f'<rect x="720" y="120" width="300" height="140" rx="12" fill="none" stroke="{RED}" '
          f'stroke-width="3" stroke-dasharray="10 7"/>')
    b += text(870, 170, ["Насос и", "автополив"], 22, RED, True)
    b += text(870, 232, ["за границей — не в WBS"], 20, RED)
    return svg(1030, 320, b)


# ── 9. Лист А4 (альбомный) ─────────────────────────────────────────────────────────────
def sheet():
    b = f'<rect x="16" y="16" width="584" height="414" rx="6" fill="{LINE}" opacity=".6"/>'
    b += f'<rect x="8" y="8" width="584" height="414" rx="6" fill="{W}" stroke="{INK}" stroke-width="3"/>'
    b += text(30, 38, ["А4"], 20, BLUE, True, anchor="start")
    b += (f'<rect x="170" y="30" width="260" height="56" rx="10" fill="{BLUE}" opacity=".12" '
          f'stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 6"/>')
    b += text(300, 58, ["проект"], 22, BLUE, True)
    for i in range(4):
        cx = 92 + i * 138
        b += f'<line x1="{cx}" y1="118" x2="300" y2="88" stroke="{INK}" stroke-width="2"/>'
        b += (f'<rect x="{cx - 60}" y="120" width="120" height="58" rx="8" fill="none" stroke="{INK}" '
              f'stroke-width="3" stroke-dasharray="8 6"/>')
        b += text(cx, 149, ["результат"], 18, INK, True)
        for k in range(3 if i < 2 else 2):
            y = 205 + k * 62
            b += (f'<rect x="{cx - 55}" y="{y}" width="110" height="48" rx="6" fill="none" stroke="{BLUE}" '
                  f'stroke-width="2" stroke-dasharray="6 5"/>')
            b += text(cx, y + 24, ["пакет"], 17, BLUE)
    b += text(300, 402, ["отчёт · управление проектом — тоже результаты"], 18, RED, True)
    return svg(600, 430, b)


if __name__ == "__main__":
    save("z06_hook.svg", hook())
    save("z06_whole.svg", whole())
    save("z06_place.svg", place())
    for s in (1, 2, 3):
        save(f"z06_tree{s}.svg", tree(s))
    save("z06_package.svg", package())
    save("z06_package_blank.svg", package(blank=True))
    save("z06_hundred.svg", hundred())
    save("z06_sheet.svg", sheet())
