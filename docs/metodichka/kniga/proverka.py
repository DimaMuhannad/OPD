#!/usr/bin/env python3
"""Проверка глав книги по памятке РИЦ ГУАП и правилам курса (CLAUDE.md).

Запуск: python3 proverka.py [glavy/*.qmd]   — ноль ошибок перед показом РИЦ.
Ошибки (код выхода 1) и предупреждения печатаются с номером строки.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Тон (CLAUDE.md): слово -> чем заменить
TON = {
    r"не получил": "встретились со сложностями", r"не удал": "встретились со сложностями",
    r"провал": "встретились со сложностями", r"неудач": "общий результат / сложности",
    r"затруднени": "сложности", r"работа встала": "где было сложно",
    r"передела": "ещё один подход, вторая версия листа", r"исправ\w* лист": "вторая версия листа",
    r"для галочки": "появилось уже после того, как решение сложилось",
}
# Книга не привязана к семестру и не показывает РПД
ZAPRET = {
    # «ДД.ММ»: коды пакетов WBS (1.1, 2.3) под шаблон не попадают
    r"\b([0-2]\d|3[01])\.(0[1-9]|1[0-2])(\.\d{2,4})?\b": "дата — в книге недели от начала семестра, без дат",
    r"\bРПД\b|рабочая программа": "РПД студентам не показывается",
    r"\bна паре\b|\bзанятии? \d": "книга не привязана к расписанию занятий",
}


def strip_code(lines):
    """Строки вне блоков кода и HTML-комментариев (номер, текст)."""
    out, code, comment = [], False, False
    for i, ln in enumerate(lines, 1):
        if ln.startswith("```"):
            code = not code
            continue
        if "<!--" in ln:
            comment = True
        if not code and not comment:
            out.append((i, ln))
        if "-->" in ln:
            comment = False
    return out


def check_qmd(path):
    err, warn = [], []
    lines = open(path, encoding="utf-8").read().split("\n")
    body = strip_code(lines)
    text = "\n".join(ln for _, ln in body)

    for i, ln in body:
        if ln.startswith("---") or ln.startswith("#|"):
            continue
        plain = re.sub(r"\{[^}]*\}|\(\.\./[^)]*\)|\[-?@[^\]]*\]|@\w[\w-]*", "", ln)
        for pat, fix in TON.items():
            if re.search(pat, plain, re.I):
                err.append(f"{i}: тон — «{re.search(pat, plain, re.I).group(0)}» → {fix}")
        for pat, why in ZAPRET.items():
            if not ln.startswith(("|", ":")) and re.search(pat, plain):
                err.append(f"{i}: {why}: «{re.search(pat, plain).group(0)}»")
        if re.match(r"#{4,} ", ln):
            err.append(f"{i}: рубрикация глубже трёх уровней")
        m = re.match(r"(#{1,3}) (.+?)\s*(\{.*\})?$", ln)
        if m and m.group(2).rstrip().endswith("."):
            err.append(f"{i}: точка в конце заголовка")
        if re.search(r"<u>|\[[^\]]+\]\{\.underline\}", ln):
            err.append(f"{i}: подчёркивание (памятка: выделение курсивом или полужирным)")
        # подписи рисунков и таблиц: без точки в конце
        m = re.match(r"!\[(.+?)\]\(", ln) or re.match(r": (.+?) \{#tbl-", ln)
        if m and m.group(1).rstrip().endswith("."):
            err.append(f"{i}: точка в конце подписи")

    # каждый рисунок и таблица: есть ссылка в тексте, и она раньше самого объекта
    for kind in ("fig", "tbl"):
        for m in re.finditer(r"\{#(" + kind + r"-[\w-]+)", text):
            lab = m.group(1)
            ref = re.search(r"@" + re.escape(lab) + r"\b", text)
            if not ref:
                err.append(f"{lab}: нет ссылки в тексте")
            elif ref.start() > m.start():
                warn.append(f"{lab}: первая ссылка стоит после объекта")

    # если раздел делится — подразделов не меньше двух
    heads = [(i, len(m.group(1))) for i, ln in body if (m := re.match(r"(#{1,3}) ", ln))
             and "{.unnumbered}" not in ln]
    for k, (i, lvl) in enumerate(heads):
        kids = 0
        for _, l2 in heads[k + 1:]:
            if l2 <= lvl:
                break
            if l2 == lvl + 1:
                kids += 1
        if kids == 1:
            warn.append(f"{i}: раздел делится на один подраздел (памятка: минимум два)")

    # глава не кончается рисунком или таблицей: последний значимый блок перед списком литературы
    tail = text.split("Библиографический список")[0].rstrip().split("\n")
    last = next((ln for ln in reversed(tail) if ln.strip() and not ln.startswith(":::")), "")
    if last.startswith(("!", "|", ": ")):
        err.append("глава заканчивается рисунком или таблицей — нужен обобщающий абзац")
    return err, warn


def check_figures():
    err = []
    for f in sorted(glob.glob(os.path.join(HERE, "risunki", "out", "*_pechat.svg"))):
        svg = open(f, encoding="utf-8").read()
        w = float(re.search(r'width="([\d.]+)pt"', svg).group(1))
        name = os.path.basename(f)
        if w > 114 / 25.4 * 72 + 0.5:
            err.append(f"{name}: ширина {w * 25.4 / 72:.0f} мм > 114 мм")
        sizes = {float(s) for s in re.findall(r'font-size="([\d.]+)"', svg)}
        if sizes and (min(sizes) < 8 or max(sizes) > 10):
            err.append(f"{name}: кегль {sorted(sizes)} вне 8–10 пт")
        fams = set(re.findall(r'font-family="([^"]+)"', svg)) - {"Times New Roman"}
        if fams:
            err.append(f"{name}: шрифт {fams} вместо Times New Roman")
    return err


def main(paths):
    total = 0
    for p in paths:
        err, warn = check_qmd(p)
        for e in err:
            print(f"ОШИБКА {os.path.relpath(p, HERE)}:{e}")
        for w in warn:
            print(f"предупреждение {os.path.relpath(p, HERE)}:{w}")
        total += len(err)
    for e in check_figures():
        print(f"ОШИБКА рисунок {e}")
        total += 1
    print(f"Ошибок: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "glavy", "*.qmd")))))
