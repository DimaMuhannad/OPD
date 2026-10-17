#!/usr/bin/env python3
"""
Автопроверка материалов курса перед сдачей и публикацией.
Ловит ошибки, которые преподаватель уже находил вручную (правила — CLAUDE.md).

    python3 tools/check/lint.py 05            # всё по занятию 5: колода, речь, конспект, посты
    python3 tools/check/lint.py <файл> ...    # отдельные файлы

ОШИБКА — исправить до отправки. ВНИМАНИЕ — посмотреть глазами, может быть допустимо.
Код выхода 1, если есть хотя бы одна ОШИБКА.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
issues = []


def add(level, path, line, msg, text=""):
    issues.append((level, path, line, msg, text.strip()[:110]))


# Словарь тона (CLAUDE.md, «Тон — вторая правка того же дня»)
TONE = [
    (r"не получилось|не удалось|провал", "тон: «встретились со сложностями»"),
    (r"затруднени", "тон: «сложности» (кроме термина productive failure)"),
    (r"работа встала", "тон: «где было сложно»"),
    (r"неудач", "тон: «общий результат, а не чья-то недоработка»"),
    (r"переделать|исправить лист", "тон: «ещё один подход, вторая версия листа»"),
    (r"для галочки", "тон: «появилось уже после того, как решение сложилось»"),
]
# Ссылки по номеру вместо смысла (CLAUDE.md, замечание 02.10)
BY_NUMBER = r"\b(слайд[а-я]*|раздел[а-я]*|пункт[а-я]*|практик[а-я]*|учебн[а-я]+ вопрос[а-я]*)\s+№?\s*\d+"
DATE = r"\b\d{1,2}\.\d{2}(\.\d{4})?\b"


def lines(p):
    return p.read_text(encoding="utf-8").split("\n")


def check_common(p, L, tone=True, numbers=True):
    for i, s in enumerate(L, 1):
        low = s.lower()
        if re.search(r"\b[АA]3\b", s):
            add("ОШИБКА", p, i, "формат А3 — принтера и бумаги А3 нет, только А4 (17.10)", s)
        if tone:
            for rx, msg in TONE:
                if re.search(rx, low) and "productive failure" not in low:
                    add("ВНИМАНИЕ", p, i, msg, s)
        if numbers and re.search(BY_NUMBER, low) and not re.search(r"\(\s*(слайд|раздел|пункт)", low):
            add("ВНИМАНИЕ", p, i, "ссылка по номеру — назвать по смыслу, номер только в скобках", s)


def check_deck(p):
    L = lines(p)
    text = "\n".join(L)
    check_common(p, L)
    for i, s in enumerate(L, 1):
        low = s.lower()
        if "рабочая программа" in low:
            add("ОШИБКА", p, i, "строка «Рабочая программа…» на слайде не показывается", s)
        if re.search(r"учебный вопрос\s*\d|\d+\s*мин\b.*·|·\s*\d+\s*мин", low) and "stop-work" not in s:
            add("ОШИБКА", p, i, "служебная строка над заголовком (учебный вопрос / минуты)", s)
        if "style=" in s:
            add("ОШИБКА", p, i, "style= вырезается санитайзером Marp — нужен класс в theme.css", s)
        if s.startswith("# ") and re.search(r"\bне [^,]{2,40}, а\b", low):
            add("ВНИМАНИЕ", p, i, "афоризм «не А, а Б» в заголовке", s)
        if s.startswith("# ") and len(s) > 95:
            add("ВНИМАНИЕ", p, i, f"длинный заголовок ({len(s) - 2} знаков) — проверить перенос", s)
    for m in re.finditer(r"[^\n]\n---\n", text):
        ln = text[: m.start()].count("\n") + 2
        if ln > 8:
            add("ОШИБКА", p, ln, "перед --- нет пустой строки — слайды слипнутся")
    for m in re.finditer(r'src="([^"]+)"', text):
        if not (p.parent / m.group(1)).resolve().exists():
            add("ОШИБКА", p, text[: m.start()].count("\n") + 1, f"нет файла картинки {m.group(1)}")


def deck_heads(p):
    text = p.read_text(encoding="utf-8")
    parts = re.split(r"\n\s*\n---\s*\n", text)
    heads = []
    for part in parts[1:]:  # parts[0] — фронтматтер
        m = re.search(r"^#{1,2} (.+)$", part, re.M)
        heads.append(m.group(1).strip() if m else "")
    return heads


def check_speech(p, deck):
    L = lines(p)
    check_common(p, L, numbers=False)  # номера слайдов в речи — для преподавателя, допустимы
    heads = [(i, re.match(r"## СЛАЙД (\d+)\s*·\s*(.*)", s)) for i, s in enumerate(L, 1)]
    heads = [(i, int(m.group(1)), m.group(2).strip()) for i, m in heads if m]
    if not deck:
        return
    dh = deck_heads(deck)
    if len(heads) != len(dh):
        add("ОШИБКА", p, 0, f"в речи {len(heads)} слайдов, в колоде {len(dh)} — речь не соответствует колоде")
    for k, (i, n, title) in enumerate(heads):
        if n != k + 1:
            add("ОШИБКА", p, i, f"нумерация сбита: ожидался слайд {k + 1}, стоит {n}")
        if k < len(dh) and k > 1 and dh[k] and title and title.lower()[:25] != dh[k].lower()[:25]:
            add("ВНИМАНИЕ", p, i, f"заголовок расходится с колодой: «{dh[k][:60]}»", title)


def check_konspekt(p):
    L = lines(p)
    check_common(p, L)
    for i, s in enumerate(L, 1):
        low = s.lower()
        if "рабочая программа" in low or re.search(r"\bрпд\b", low):
            add("ОШИБКА", p, i, "метаконтекст РПД в методических указаниях", s)
        if re.search(r"\(\s*\d+\s*мин|\d+\s*минут\)|хронометраж", low):
            add("ОШИБКА", p, i, "время на этап — живёт в речи, не в указаниях", s)


def check_post(p):
    L = lines(p)
    check_common(p, L, numbers=False)
    for i, s in enumerate(L, 1):
        if i == 1:
            continue  # в первой строке дата прошедшего занятия допустима
        for m in re.finditer(DATE, s):
            add("ОШИБКА", p, i, f"дата {m.group(0)} в посте — писать «на следующем занятии» "
                "(даты дальних событий согласовать с преподавателем)", s)
        if re.search(r"рабочая программа|\bрпд\b", s.lower()):
            add("ОШИБКА", p, i, "РПД в посте студентам", s)
    if p.name.endswith(".files"):
        for i, s in enumerate(L, 1):
            if s.strip() and not s.startswith("#") and not (ROOT / s.strip()).exists():
                add("ОШИБКА", p, i, f"нет файла вложения {s.strip()}")


def check_file(p, deck=None):
    n = p.name
    if p.suffix == ".md" and "marp-src" in str(p):
        check_deck(p)
    elif "Rech_po_slaydam" in n and p.suffix == ".md":
        check_speech(p, deck or guess_deck(p))
    elif "Konspekt" in n and p.suffix == ".md":
        check_konspekt(p)
    elif "telegram/posts" in str(p) and p.suffix in (".txt", ".files"):
        check_post(p)


def guess_deck(p):
    num = re.match(r"Zanyatie_(\d+)", p.name)
    if not num:
        return None
    c = sorted((ROOT / "zanyatiya/marp-src").glob(f"Zanyatie_{num.group(1)}_*Slaydy.md"))
    return c[0] if len(c) == 1 else None


def files_for(num):
    num = num.zfill(2)
    out = sorted((ROOT / "zanyatiya/marp-src").glob(f"Zanyatie_{num}_*.md"))
    out += sorted((ROOT / "zanyatiya").glob(f"Zanyatie_{num}_*.md"))
    # посты: комплект, где вложения или текст ссылаются на это занятие
    for kit in sorted((ROOT / "tools/telegram/posts").glob("*/")):
        blob = " ".join(f.read_text(encoding="utf-8") for f in kit.glob("*") if f.is_file())
        if f"Zanyatie_{num}_" in blob or f"Занятие {int(num)} " in blob:
            out += sorted(f for f in kit.glob("*") if f.suffix in (".txt", ".files"))
    return out


def main(args):
    if not args:
        print(__doc__)
        return 2
    targets = []
    for a in args:
        targets += files_for(a) if re.fullmatch(r"\d{1,2}", a) else [Path(a).resolve()]
    for t in targets:
        check_file(t)
    for lvl, p, ln, msg, txt in sorted(issues, key=lambda x: (x[0] != "ОШИБКА", str(x[1]), x[2])):
        rel = Path(p).resolve().relative_to(ROOT) if str(p).startswith(str(ROOT)) else p
        print(f"{lvl:9} {rel}:{ln}  {msg}" + (f"\n          › {txt}" if txt else ""))
    err = sum(1 for x in issues if x[0] == "ОШИБКА")
    print(f"\nПроверено файлов: {len(targets)}. Ошибок: {err}, внимание: {len(issues) - err}.")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
