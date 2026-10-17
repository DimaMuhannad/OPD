"""Общие профили рисунков книги: экран (веб) и печать (рукопись РИЦ, PDF А5).

Рисунок описывается один раз как граф Graphviz; профиль задаёт шрифт, кегль и цвета.
Печатный профиль не масштабируется: если рисунок шире поля набора (114 мм), сборка
останавливается — иначе кегль надписей молча упал бы ниже 8 пт (памятка РИЦ: 8–10 пт).
"""
import os
import subprocess
import sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")

PROFILES = {
    # цвета только из tools/marp/guap-brand/BRAND.md
    "ekran": dict(font="Arial", size=14, ink="#002C5F", line="#005AAA", fill="#FFFFFF",
                  accent_fill="#005AAA", accent_ink="#FFFFFF", mute="#00BEF3", warn="#E70F47"),
    # ч/б: акцент — серая заливка и полужирный, «за границей» — пунктир
    "pechat": dict(font="Times New Roman", size=9, ink="#000000", line="#000000", fill="#FFFFFF",
                   accent_fill="#D9D9D9", accent_ink="#000000", mute="#000000", warn="#000000"),
}
MAX_W_PT = 114 / 25.4 * 72   # 323 pt — ширина поля набора А5
MAX_H_PT = 165 / 25.4 * 72   # 468 pt — высота поля набора


SHORT = {"в", "во", "с", "со", "к", "ко", "и", "а", "о", "у", "на", "по", "за", "из", "от", "до", "не"}


def wrap(t, n):
    """Перенос подписи по словам: строки не длиннее n знаков, разделитель Graphviz \\n.
    Короткий предлог или союз не остаётся в конце строки — склеивается со следующим словом."""
    words, glued = t.split(), []
    for w in words:
        if glued and glued[-1].lower() in SHORT:
            glued[-1] += "\u00a0" + w
        else:
            glued.append(w)
    out, cur = [], ""
    for w in glued:
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return "\\n".join(out + [cur])


def pango(p, style=""):
    """Имя шрифта для Graphviz в синтаксисе pango: «Семейство,Начертание».
    Без запятой pango читает «Roman» в «Times New Roman» как начертание, ищет семейство «Times New»
    и молча подставляет другой шрифт (в этой среде — Inter)."""
    return f'{p["font"]},{style}'


def head(p, rankdir="TB", nodesep=0.1, ranksep=0.25):
    f = pango(p)
    return (
        f'graph [rankdir={rankdir}, nodesep={nodesep}, ranksep={ranksep}, splines=ortho, '
        f'fontname="{f}", fontsize={p["size"]}];\n'
        f'node [shape=box, fontname="{f}", fontsize={p["size"]}, color="{p["line"]}", '
        f'fontcolor="{p["ink"]}", style=filled, fillcolor="{p["fill"]}", margin="0.07,0.04"];\n'
        f'edge [color="{p["line"]}", fontname="{f}", fontsize={p["size"]}];\n'
    )


def accent(p):
    """Атрибуты выделенного узла."""
    return f'fillcolor="{p["accent_fill"]}", fontcolor="{p["accent_ink"]}", fontname="{pango(p, "Bold")}"'


def render(name, build):
    """build(p) -> тело графа. Пишет out/<name>_<профиль>.svg и .pdf, проверяет печатный размер."""
    os.makedirs(OUT, exist_ok=True)
    for prof, p in PROFILES.items():
        src = "digraph g {\n" + build(p) + "}\n"
        svg = subprocess.run(["dot", "-Tsvg"], input=src.encode(), capture_output=True, check=True).stdout.decode()
        w = float(svg.split('width="', 1)[1].split("pt", 1)[0])
        h = float(svg.split('height="', 1)[1].split("pt", 1)[0])
        if prof == "pechat":
            if w > MAX_W_PT or h > MAX_H_PT:
                sys.exit(f"{name}: {w:.0f}×{h:.0f} pt не помещается в 114×165 мм "
                         f"({MAX_W_PT:.0f}×{MAX_H_PT:.0f} pt) — переделать раскладку")
            print(f"{name}: {w * 25.4 / 72:.0f}×{h * 25.4 / 72:.0f} мм, кегль {p['size']} пт")
        # в SVG имя pango («Семейство,Bold») браузер прочтёт как список семейств — переводим в CSS
        svg = svg.replace(f'font-family="{pango(p, "Bold")}"', f'font-family="{p["font"]}" font-weight="bold"')
        svg = svg.replace(f'font-family="{pango(p)}"', f'font-family="{p["font"]}"')
        with open(os.path.join(OUT, f"{name}_{prof}.svg"), "w") as f:
            f.write(svg)
        pdf = os.path.join(OUT, f"{name}_{prof}.pdf")
        subprocess.run(["dot", "-Tpdf", "-o", pdf], input=src.encode(), check=True)
        if prof == "pechat":
            fonts = subprocess.run(["pdffonts", pdf], capture_output=True, text=True, check=True).stdout
            alien = [ln.split()[0] for ln in fonts.splitlines()[2:] if "TimesNewRoman" not in ln]
            if alien:
                sys.exit(f"{name}: в печатном PDF чужие шрифты {alien} — проверить имя шрифта")
