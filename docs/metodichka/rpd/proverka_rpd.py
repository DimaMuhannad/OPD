#!/usr/bin/env python3
"""Проверка согласованности черновика РПД 2027.

- таблица 3: сумма по разделам = 17 / 34 / 21 (лекции / ПЗ / СР);
- таблица 5: часы практик по разделам совпадают с таблицей 3, всего 34, практическая подготовка 8;
- тон (CLAUDE.md).
Запуск: python3 docs/metodichka/rpd/proverka_rpd.py [файл.md]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TON = r"не получил|не удал|провал|неудач|затруднени|работа встала|передела|для галочки"


def main(path):
    s = open(path, encoding="utf-8").read()
    err = []

    t3 = re.findall(r"^\| \*\*Раздел (\d+)\..*?\| (\d+) \| (\d+) \| (\d+) \|$", s, re.M)
    tot = [sum(int(r[i]) for r in t3) for i in (1, 2, 3)]
    if tot != [17, 34, 21]:
        err.append(f"таблица 3: итог {tot}, нужно [17, 34, 21]")
    pz3 = {r[0]: int(r[2]) for r in t3}

    t5 = re.findall(r"^\| (\d+) \| .*? \| (\d+) \| (—|\d+) \| (\d+) \|$", s, re.M)
    pz5, pp = {}, 0
    for _, h, p, sec in t5:
        pz5[sec] = pz5.get(sec, 0) + int(h)
        pp += 0 if p == "—" else int(p)
    if sum(pz5.values()) != 34:
        err.append(f"таблица 5: всего {sum(pz5.values())} ч, нужно 34")
    if pz5 != pz3:
        err.append(f"часы ПЗ по разделам: таблица 3 {pz3} ≠ таблица 5 {pz5}")
    if pp != 8:
        err.append(f"практическая подготовка {pp} ч, в предложении 8")

    for i, ln in enumerate(s.split("\n"), 1):
        m = re.search(TON, ln, re.I)
        if m and "Fail" not in ln:
            err.append(f"{i}: тон — «{m.group(0)}»")

    for e in err:
        print("ОШИБКА", e)
    print(f"Разделов: {len(t3)}, практик: {len(t5)}. Ошибок: {len(err)}")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "RPD_2027_OPD_1kurs_chernovik.md")))
