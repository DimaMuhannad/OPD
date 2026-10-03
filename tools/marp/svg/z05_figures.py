#!/usr/bin/env python3
"""Рисунки для колоды занятия 5 «Содержание проекта» -> zanyatiya/img/z05_*.svg.

Палитра — только ГУАП (BRAND.md): dk2 #002C5F, accent1 #005AAA, accent2 #E70F47,
accent6 #009A49, dk1 #242834, белый; светлые подложки — те же цвета с прозрачностью.
Шрифт Arial. Размер текста в рисунках 20–24 px: рисунок показывается 1:1 на слайде
1280x720, 1 pt = 1.333 px, то есть 15–18 pt.

Запуск: python3 tools/marp/svg/z05_figures.py
"""
import os
import textwrap

INK, BLUE, GREEN, RED, DK1 = "#002C5F", "#005AAA", "#009A49", "#E70F47", "#242834"
W, LIGHT, LINE = "#FFFFFF", "#F4F7FA", "#C9D3DE"
FS = 24
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "..", "zanyatiya", "img")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def wrap(text, w, fs):
    n = max(6, int((w - 28) / (fs * 0.56)))
    return textwrap.wrap(text, n)


def text(cx, cy, lines, fs=FS, fill=INK, bold=False, anchor="middle", italic=False, op=1):
    out = []
    n = len(lines)
    for i, ln in enumerate(lines):
        y = cy + (i - (n - 1) / 2) * fs * 1.25
        out.append(
            f'<text x="{cx}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="central" '
            f'font-family="Arial, Helvetica, sans-serif" font-size="{fs}" fill="{fill}" '
            f'font-weight="{"700" if bold else "400"}" font-style="{"italic" if italic else "normal"}" '
            f'opacity="{op}">{esc(ln)}</text>'
        )
    return "".join(out)


def node(cx, cy, w, label, h=None, fill=W, stroke=INK, tc=INK, sw=2.5, dash=None,
         fs=FS, bold=False, op=1, rx=12):
    lines = wrap(label, w, fs)
    need = len(lines) * fs * 1.25 + 24
    h = max(h or 0, need)
    d = f' stroke-dasharray="{dash}"' if dash else ""
    r = (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w}" height="{h:.1f}" rx="{rx}" '
         f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d} opacity="{op}"/>')
    return r + text(cx, cy, lines, fs, tc, bold, op=op), h


def arrow(x1, y1, x2, y2, color=INK, sw=3, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    mid = {INK: "ai", BLUE: "ab", RED: "ar", GREEN: "ag", W: "aw", DK1: "ad"}[color]
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} '
            f'marker-end="url(#{mid})"/>')


def svg(w, h, body):
    marks = "".join(
        f'<marker id="{i}" markerWidth="12" markerHeight="10" refX="11" refY="5" orient="auto">'
        f'<path d="M0,0 L12,5 L0,10 z" fill="{c}"/></marker>'
        for i, c in (("ai", INK), ("ab", BLUE), ("ar", RED), ("ag", GREEN), ("aw", W), ("ad", DK1)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{marks}</defs>{body}</svg>')


def save(name, s):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)
    print("OK", name)


# ── 1. Хук: два дерева, одно из них — дерево решений ───────────────────────
def hook():
    b = ""
    panels = (
        (0, "А", "Растение болеет или гибнет", "Владельцы поливают неправильно",
         ("Полив на глаз", "Влажность не видна", "При отъезде полива нет")),
        (624, "Б", "Нет готового устройства", "Нет приложения для учёта полива",
         ("Нет датчика", "Нет программы", "Нет корпуса")),
    )
    for x0, tag, top, mid, roots in panels:
        b += f'<rect x="{x0}" y="0" width="560" height="440" rx="16" fill="{W}"/>'
        b += f'<circle cx="{x0 + 40}" cy="40" r="26" fill="{BLUE}"/>' + text(x0 + 40, 40, [tag], 30, W, True)
        n, _ = node(x0 + 280, 100, 400, top, fill=LIGHT, fs=22)
        b += n
        n, _ = node(x0 + 280, 225, 470, mid, fill=BLUE, stroke=BLUE, tc=W, bold=True, fs=22)
        b += n
        b += arrow(x0 + 280, 190, x0 + 280, 138, INK)
        for i, r in enumerate(roots):
            cx = x0 + 100 + i * 180
            n, _ = node(cx, 370, 166, r, fill=LIGHT, fs=20, h=88)
            b += n
            b += arrow(cx, 326, x0 + 280 + (i - 1) * 60, 262, INK, 2.5)
    return svg(1184, 440, b)


# ── 2. Айсберг: продукт и работа проекта ───────────────────────────────────
def iceberg():
    b = f'<rect x="0" y="175" width="620" height="285" fill="{BLUE}" opacity=".12"/>'
    b += f'<line x1="0" y1="175" x2="620" y2="175" stroke="{BLUE}" stroke-width="3"/>'
    b += (f'<polygon points="330,25 250,175 410,175" fill="{W}" stroke="{INK}" stroke-width="3" '
          f'stroke-linejoin="round"/>')
    b += (f'<polygon points="230,175 430,175 560,250 520,370 350,440 190,385 110,270" fill="{BLUE}" '
          f'opacity=".30" stroke="{BLUE}" stroke-width="3" stroke-linejoin="round"/>')
    b += text(430, 62, ["ПРОДУКТ"], 24, BLUE, True, anchor="start")
    b += text(430, 118, ["датчик,", "индикатор,", "корпус"], 22, INK, anchor="start")
    b += text(325, 230, ["РАБОТА ПРОЕКТА"], 24, INK, True)
    b += text(325, 300, ["подобрать датчик", "собрать схему", "10 циклов полива", "написать отчёт"], 22, INK)
    b += text(14, 152, ["видно всем"], 20, BLUE, True, anchor="start")
    b += text(14, 205, ["видит команда"], 20, BLUE, True, anchor="start")
    return svg(620, 460, b)


# ── 3. Расползание: граница, которую раздвигают «а ещё…» ───────────────────
def creep():
    b = f'<rect x="85" y="75" width="450" height="285" rx="14" fill="{RED}" opacity=".07" stroke="{RED}" stroke-width="3" stroke-dasharray="10 7"/>'
    b += f'<rect x="195" y="140" width="230" height="150" rx="12" fill="{LIGHT}" stroke="{BLUE}" stroke-width="3.5" stroke-dasharray="10 7"/>'
    b += text(310, 190, ["содержание", "на старте"], 24, BLUE, True)
    b += text(310, 250, ["датчик, индикатор"], 20, INK)
    notes = ((10, 12, 210, 54, "а ещё приложение", 160, 76),
             (400, 12, 210, 54, "а ещё автополив", 460, 76),
             (8, 380, 270, 54, "а ещё чат-бот", 100, 358),
             (400, 380, 210, 54, "а ещё доставка", 470, 358))
    for x, y, w, h, t, ax, ay in notes:
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{W}" stroke="{RED}" stroke-width="2.5"/>'
        b += text(x + w / 2, y + h / 2, [t], 20, RED, True)
    b += arrow(110, 66, 150, 100, RED, 3)
    b += arrow(500, 66, 460, 100, RED, 3)
    b += arrow(130, 380, 150, 340, RED, 3)
    b += arrow(490, 380, 470, 340, RED, 3)
    b += text(310, 100, ["граница после «а ещё…»"], 20, RED, True)
    b += text(310, 452, ["срок, стоимость и ресурсы остались прежними"], 20, INK, True)
    return svg(620, 480, b)


# ── 4. Несколько причин, проект закрывает не все ───────────────────────────
def causes():
    ys = (50, 150, 250, 350)
    labels = ("Влажность на глубине корней не видна", "Готовые датчики дороги",
              "Полив по расписанию, а не по почве", "При отъезде полива нет")
    b = (f'<rect x="8" y="6" width="500" height="196" rx="16" fill="{BLUE}" opacity=".08" '
         f'stroke="{BLUE}" stroke-width="3.5" stroke-dasharray="10 7"/>')
    for i, (y, t) in enumerate(zip(ys, labels)):
        inside = i < 2
        n, _ = node(258, y, 460, t, fill=W, stroke=BLUE if inside else DK1, sw=3 if inside else 2,
                    dash=None if inside else "7 6", op=1 if inside else .6, h=70)
        b += n
        b += arrow(490, y, 730, 200 + (y - 200) * .35, BLUE if inside else DK1, 3, None if inside else "7 6")
    n, _ = node(950, 200, 380, "Растения поливают неправильно", fill=BLUE, stroke=BLUE, tc=W, bold=True, h=110)
    b += n
    b += text(525, 26, ["проект берёт эти"], 22, BLUE, True, anchor="start")
    b += text(525, 382, ["остальное проект не закрывает"], 22, DK1, anchor="start", op=.8)
    return svg(1184, 400, b)


# ── 5–7. Дерево проблем, растёт по шагам ───────────────────────────────────
def tree(step):
    b = ""
    cx = 592
    if step >= 3:
        b += (f'<ellipse cx="592" cy="95" rx="570" ry="92" fill="{GREEN}" opacity=".10" '
              f'stroke="{GREEN}" stroke-width="2.5"/>')
        b += text(14, 20, ["СЛЕДСТВИЯ"], 20, GREEN, True, anchor="start")
        for dx, t in ((-340, "Растение болеет или гибнет"), (0, "Труд и деньги пропадают"),
                      (340, "Человек отказывается от растений")):
            n, _ = node(cx + dx, 95, 310, t, fill=W, stroke=GREEN, sw=3, h=78)
            b += n
            b += arrow(cx + dx * .55, 194, cx + dx * .85, 136, GREEN, 3)
    if step < 3:   # бледные заготовки ещё не построенных ветвей
        b += (f'<ellipse cx="592" cy="95" rx="570" ry="92" fill="none" stroke="{GREEN}" '
              f'stroke-width="2.5" stroke-dasharray="9 8" opacity=".55"/>')
        b += text(592, 95, ["следствия: к чему это приводит?"], 24, GREEN, True, op=.8)
    if step < 2:
        b += (f'<rect x="42" y="346" width="1100" height="78" rx="12" fill="none" stroke="{INK}" '
              f'stroke-width="2.5" stroke-dasharray="9 8" opacity=".5"/>')
        b += text(592, 385, ["причины: почему это происходит?"], 24, INK, True, op=.75)
    if step >= 2:
        b += text(14, 200, ["ПРОБЛЕМА"], 20, BLUE, True, anchor="start")
    n, _ = node(cx, 235, 600, "Владельцы поливают неправильно, и это заметно слишком поздно",
                fill=BLUE, stroke=BLUE, tc=W, bold=True, h=78)
    b += n
    if step >= 2:
        b += text(14, 322, ["ПРИЧИНЫ"], 20, INK, True, anchor="start")
        for dx, t in ((-380, "Полив на глаз, а не по почве"), (0, "Влажность на глубине корней не видна"),
                      (380, "При отъезде полива нет")):
            n, _ = node(cx + dx, 385, 340, t, fill=W, stroke=INK, sw=3, h=78)
            b += n
            b += arrow(cx + dx * .8, 346, cx + dx * .3, 277, INK, 3)
    return svg(1184, 440, b)


# ── 8. Макет листа А4 ──────────────────────────────────────────────────────
def sheet():
    b = f'<rect x="16" y="16" width="584" height="414" rx="6" fill="{LINE}" opacity=".6"/>'
    b += f'<rect x="8" y="8" width="584" height="414" rx="6" fill="{W}" stroke="{INK}" stroke-width="3"/>'
    for dx, t in ((-150, "следствие"), (150, "следствие")):
        b += (f'<rect x="{300 + dx - 120}" y="30" width="240" height="64" rx="10" fill="none" '
              f'stroke="{GREEN}" stroke-width="3" stroke-dasharray="8 6"/>')
        b += text(300 + dx, 62, [t], 22, GREEN, True)
        b += arrow(300 + dx * .5, 170, 300 + dx * .8, 98, GREEN, 3)
    b += (f'<rect x="90" y="172" width="420" height="76" rx="10" fill="{BLUE}" opacity=".12" '
          f'stroke="{BLUE}" stroke-width="3" stroke-dasharray="8 6"/>')
    b += text(300, 210, ["центральная проблема"], 24, BLUE, True)
    for i, dx in enumerate((-190, 0, 190)):
        b += (f'<rect x="{300 + dx - 85}" y="328" width="170" height="68" rx="10" fill="none" '
              f'stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>')
        b += text(300 + dx, 362, ["причина"], 22, INK, True)
        b += arrow(300 + dx * .7, 324, 300 + dx * .4, 252, INK, 3)
    b += text(14, 118, ["≥ 2"], 20, GREEN, True, anchor="start")
    b += text(14, 304, ["≥ 3"], 20, INK, True, anchor="start")
    return svg(600, 430, b)


# ── 9. Инверсия: дерево проблем → дерево целей ─────────────────────────────
def invert():
    rows = (("Владельцы поливают неправильно", "Владелец поливает по состоянию почвы"),
            ("Влажность на глубине корней не видна", "Влажность на глубине корней видна"),
            ("Готовые датчики дороги", "Датчик доступен по цене"),
            ("При отъезде полива нет", "Полив идёт и без хозяина"))
    b = text(272, 24, ["ДЕРЕВО ПРОБЛЕМ"], 22, INK, True) + text(912, 24, ["ДЕРЕВО ЦЕЛЕЙ"], 22, BLUE, True)
    for i, (l, r) in enumerate(rows):
        y = 84 + i * 80
        n, _ = node(272, y, 520, l, fill=W, stroke=INK, sw=3, h=60)
        b += n
        n, _ = node(912, y, 520, r, fill=BLUE, stroke=BLUE, tc=W, bold=True, h=60)
        b += n
        b += arrow(542, y, 640, y, BLUE, 3.5)
    return svg(1184, 360, b)


# ── 10. Выбор ветвей: содержание и граница ─────────────────────────────────
def choice():
    b = ""
    n, _ = node(592, 50, 620, "Владелец поливает по состоянию почвы", fill=BLUE, stroke=BLUE, tc=W, bold=True, h=72)
    b += n
    b += f'<line x1="772" y1="130" x2="772" y2="415" stroke="{DK1}" stroke-width="3.5" stroke-dasharray="10 8"/>'
    b += text(392, 335, ["СОДЕРЖАНИЕ ПРОЕКТА"], 24, BLUE, True)
    b += text(972, 335, ["ГРАНИЦА"], 24, DK1, True)
    subs = ((232, "Влажность на глубине корней видна", True), (592, "Датчик доступен по цене", True),
            (952, "Полив идёт и без хозяина", False))
    for x, t, taken in subs:
        n, _ = node(x, 262, 340, t, h=100, fill=W, stroke=BLUE if taken else DK1, sw=4 if taken else 2.5,
                    dash=None if taken else "8 7", op=1 if taken else .65)
        b += n
        b += arrow(x + (592 - x) * .12, 212, 592 + (x - 592) * .35, 90, BLUE if taken else DK1, 3,
                   None if taken else "7 6")
    b += text(972, 372, ["записываем как отказ:"], 20, DK1, anchor="middle")
    b += text(972, 398, ["«автополив не делаем»"], 20, DK1, True, anchor="middle")
    return svg(1184, 425, b)


# ── 11. Домашнее задание: три цитаты ───────────────────────────────────────
def quotes():
    b = ""
    for i in range(3):
        x = 20 + i * 390
        b += (f'<path d="M{x + 20},10 h310 a20,20 0 0 1 20,20 v120 a20,20 0 0 1 -20,20 h-190 l-45,45 v-45 '
              f'h-75 a20,20 0 0 1 -20,-20 v-120 a20,20 0 0 1 20,-20 z" fill="{LIGHT}" stroke="{BLUE}" stroke-width="3"/>')
        b += text(x + 60, 60, ["«"], 64, BLUE, True)
        for k in range(3):
            b += (f'<line x1="{x + 56}" y1="{98 + k * 26}" x2="{x + 330}" y2="{98 + k * 26}" '
                  f'stroke="{LINE}" stroke-width="3"/>')
        b += text(x + 185, 232, [f"цитата {i + 1}"], 22, BLUE, True)
    return svg(1184, 256, b)


if __name__ == "__main__":
    save("z05_hook.svg", hook())
    save("z05_iceberg.svg", iceberg())
    save("z05_creep.svg", creep())
    save("z05_causes.svg", causes())
    for s in (1, 2, 3):
        save(f"z05_tree{s}.svg", tree(s))
    save("z05_sheet.svg", sheet())
    save("z05_invert.svg", invert())
    save("z05_choice.svg", choice())
    save("z05_quotes.svg", quotes())
