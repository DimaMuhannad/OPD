#!/usr/bin/env python3
"""Проверка CSL под ГОСТ Р 7.0.100–2018 и соглашений bib-файла книги.

1. Тестовые записи primery.bib рендерятся стилем и сравниваются с etalon.txt (строка в строку).
2. В kniga/istochniki.bib проверяются соглашения, без которых стиль ошибётся:
   - четыре автора и больше — keywords = {bez-zagolovka} (описание с заглавия), меньше — без него;
   - заглавие латиницей — langid = {english}; кириллицей — без langid;
   - организация (автор в двойных скобках) — не автор, а издатель: описание начинается с заглавия;
   - иностранный источник с пятью авторами и больше — предупреждение: стиль поставит «[и др.]», а не «[et al.]».
Запуск: python3 shablony/test-csl/proverka_csl.py   (код выхода 1 — есть ошибки)
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KNIGA = os.path.dirname(os.path.dirname(HERE))
CSL = os.path.join(KNIGA, "shablony", "gost-r-7-0-100-2018-numeric.csl")


def render():
    out = subprocess.run(["quarto", "pandoc", os.path.join(HERE, "primery.md"), "--citeproc",
                          "--bibliography", os.path.join(HERE, "primery.bib"), "--csl", CSL,
                          "-t", "plain", "--wrap=none"], capture_output=True, text=True, check=True).stdout
    return [ln for ln in out.split("\n") if ln.strip()]


def zapisi(path):
    """Записи bib: ключ -> {поле: значение} (простой разбор, хватает для нашего файла)."""
    text = open(path, encoding="utf-8").read()
    res = {}
    for m in re.finditer(r"@(\w+)\{([^,]+),(.*?)\n\}", text, re.S):
        polya = {}
        for f in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\s*$", m.group(3), re.M):
            polya[f.group(1).lower()] = f.group(2)
        polya["_tip"] = m.group(1).lower()
        polya["_syroe"] = m.group(3)
        res[m.group(2).strip()] = polya
    return res


def soglasheniya(path):
    err, warn = [], []
    for kl, p in zapisi(path).items():
        avtory = [a for a in re.split(r"\s+and\s+", p.get("author", "")) if a.strip()]
        flag = "bez-zagolovka" in p.get("keywords", "")
        if len(avtory) >= 4 and not flag:
            err.append(f"{kl}: {len(avtory)} авторов — нужно keywords = {{bez-zagolovka}} (описание с заглавия)")
        if len(avtory) < 4 and flag:
            err.append(f"{kl}: bez-zagolovka при {len(avtory)} авторах — убрать")
        title = p.get("title", "")
        latin, kiril = re.search(r"[A-Za-z]", title), re.search(r"[А-Яа-яЁё]", title)
        eng = p.get("langid", "").lower() in ("english", "american", "british")
        if latin and not kiril and not eng:
            err.append(f"{kl}: заглавие латиницей — нужно langid = {{english}}")
        if kiril and eng:
            err.append(f"{kl}: заглавие кириллицей при langid = english — убрать langid")
        if re.search(r"author\s*=\s*\{\{", p["_syroe"]):
            err.append(f"{kl}: организация как автор — перенести в publisher (описание с заглавия)")
        if eng and len(avtory) >= 5:
            warn.append(f"{kl}: иностранный источник, {len(avtory)} авторов — стиль напишет «[и др.]»; "
                        "проверить вручную (по ГОСТу — «[et al.]»)")
    return err, warn


def main():
    err = []
    got, want = render(), [ln for ln in open(os.path.join(HERE, "etalon.txt"), encoding="utf-8").read().split("\n") if ln.strip()]
    for i, (g, w) in enumerate(zip(got, want), 1):
        if g != w:
            err.append(f"эталон, строка {i}:\n  ждали:   {w}\n  вышло:   {g}")
    if len(got) != len(want):
        err.append(f"эталон: строк {len(want)}, вышло {len(got)}")
    e2, warn = soglasheniya(os.path.join(KNIGA, "istochniki.bib"))
    err += [f"istochniki.bib: {e}" for e in e2]
    for w in warn:
        print(f"предупреждение istochniki.bib: {w}")
    for e in err:
        print(f"ОШИБКА {e}")
    print(f"CSL ГОСТ Р 7.0.100–2018: эталон {len(want)} строк, ошибок: {len(err)}")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
