#!/usr/bin/env python3
"""Примечания на полях docx -> таблица замечаний в markdown (формат чек-листа вычитки проекта).

Запуск: python3 zamechaniya_docx.py <файл.docx> [>> briefy/<N>-zamechaniya.md]
Для каждого примечания: заголовок раздела, в котором оно стоит, выделенный фрагмент и текст примечания.
Уровень серьёзности берётся из начала примечания, если автор его поставил: «К:», «С:», «М:».
Нужен только Python 3 (zipfile, xml).
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def tekst(el):
    return "".join(t.text or "" for t in el.iter(W + "t"))


def main(path):
    z = zipfile.ZipFile(path)
    if "word/comments.xml" not in z.namelist():
        print("Примечаний в документе нет.", file=sys.stderr)
        return
    kom = {}
    for c in ET.fromstring(z.read("word/comments.xml")).iter(W + "comment"):
        kom[c.get(W + "id")] = (c.get(W + "author", ""), " ".join(tekst(p) for p in c.iter(W + "p")).strip())

    doc = ET.fromstring(z.read("word/document.xml"))
    razdel, otkryty, fragment, gde = "", set(), {}, {}
    for p in doc.iter(W + "p"):
        stil = p.find(f"{W}pPr/{W}pStyle")
        if stil is not None and re.match(r"(Heading|Заголовок)\s*\d", stil.get(W + "val", ""), re.I):
            razdel = tekst(p).strip()
        for el in p.iter():
            if el.tag == W + "commentRangeStart":
                i = el.get(W + "id")
                otkryty.add(i)
                gde.setdefault(i, razdel)
            elif el.tag == W + "commentRangeEnd":
                otkryty.discard(el.get(W + "id"))
            elif el.tag == W + "t":
                for i in otkryty:
                    fragment[i] = fragment.get(i, "") + (el.text or "")

    print("| № | Где: блок, цитата | Проход | Ур. | Замечание | Предложение | Решение |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for n, (i, (avtor, t)) in enumerate(sorted(kom.items(), key=lambda kv: int(kv[0])), 1):
        ur = ""
        m = re.match(r"\s*([КСМ])\s*[:.)]\s*", t)
        if m:
            ur, t = m.group(1), t[m.end():]
        cit = " ".join(fragment.get(i, "").split())
        cit = cit if len(cit) <= 80 else cit[:77] + "…"
        g = f"«{gde.get(i, '')}», «{cit}»".replace("|", "/")
        print(f"| {n} | {g} |  | {ur} | {t.replace('|', '/')} |  | [ ] |")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
