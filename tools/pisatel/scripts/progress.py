#!/usr/bin/env python3
"""Прогресс проекта по файлу progress.toml — аналог /gsd:progress для книг и документов.

Показывает: готовность разделов (полоса и счётчики по статусам), что ждёт человека, вехи со сроками
(сколько дней осталось, что просрочено), расхождения файла с репозиторием и следующий шаг.

Запуск: python3 progress.py [путь/к/progress.toml] [--json]
Без пути ищет progress.toml в текущей папке и выше, затем в docs/*/.
Нужен только Python 3.11+ (tomllib), без сторонних пакетов.
"""
import datetime as dt
import glob
import json
import os
import sys
import tomllib

# статус -> (подпись, вес готовности, значок)
STATUSY = {
    "ne_nachato": ("не начато", 0.0, "·"),
    "brif": ("задание", 0.15, "○"),
    "chernovik": ("черновик", 0.5, "◐"),
    "vychitka": ("на вычитке", 0.8, "◑"),
    "odobreno": ("одобрено", 1.0, "●"),
}


def najti(start="."):
    d = os.path.abspath(start)
    while True:
        p = os.path.join(d, "progress.toml")
        if os.path.isfile(p):
            return p
        nxt = os.path.dirname(d)
        if nxt == d:
            break
        d = nxt
    found = sorted(glob.glob(os.path.join(os.path.abspath(start), "docs", "*", "progress.toml")))
    return found[0] if found else None


def koren_repo(path):
    """Папка, относительно которой записаны пути `fail` — корень репозитория (где .git)."""
    d = os.path.dirname(os.path.abspath(path))
    while d != os.path.dirname(d):
        if os.path.exists(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    return os.path.dirname(os.path.abspath(path))


def polosa(dolya, n=20):
    k = round(dolya * n)
    return "█" * k + "░" * (n - k)


def sobrat(data, path, segodnya):
    root = koren_repo(path)
    razdely, zhdut, rashozhdeniya, v_rabote = [], [], [], []
    sled = None
    for r in data.get("razdel", []):
        punkty = r.get("punkt", [])
        schet = {s: 0 for s in STATUSY}
        ves = 0.0
        for p in punkty:
            st = p.get("status", "ne_nachato")
            if st not in STATUSY:
                rashozhdeniya.append(f"{r['id']} {p['id']}: неизвестный статус «{st}»")
                st = "ne_nachato"
            schet[st] += 1
            ves += STATUSY[st][1]
            if p.get("zhdet") and st != "odobreno":
                zhdut.append(f"{p['id']} {p['nazvanie']} — {STATUSY[st][0]}, ждёт: {p['zhdet']}")
            elif st == "vychitka":
                zhdut.append(f"{p['id']} {p['nazvanie']} — на вычитке")
            if p.get("etap"):  # незаконченная работа: с неё продолжают после сброса контекста
                # команда продолжения: из начала etap («review: …», «brief: …»), иначе команда раздела
                kmd = p["etap"].split(":", 1)[0].strip()
                kmd = f"/{kmd}" if kmd in ("brief", "review", "doc", "istochniki") else r.get("komanda", "").strip()
                v_rabote.append(f"{kmd} {p['id']}".strip() + f" — {p['nazvanie']}: {p['etap']}")
            briefy = data.get("nastrojki", {}).get("briefy")
            if briefy and STATUSY[st][1] >= 0.15 and not os.path.exists(os.path.join(root, briefy, f"{p['id']}.md")):
                if st == "brif":
                    rashozhdeniya.append(f"{p['id']}: статус «задание», но нет {briefy}/{p['id']}.md (/brief {p['id']})")
            f = p.get("fail")
            if f:
                est = os.path.exists(os.path.join(root, f))
                if not est and STATUSY[st][1] >= 0.5:
                    rashozhdeniya.append(f"{p['id']}: статус «{STATUSY[st][0]}», но файла нет: {f}")
                if est and st == "ne_nachato":
                    rashozhdeniya.append(f"{p['id']}: файл есть ({f}), а статус «не начато»")
            if sled is None and st in ("ne_nachato", "brif") and not p.get("zhdet"):
                sled = f"{r.get('komanda', '').strip()} {p['id']}".strip() + f" — {p['nazvanie']}"
        dolya = ves / len(punkty) if punkty else 0.0
        razdely.append({"id": r["id"], "nazvanie": r.get("nazvanie", r["id"]), "vsego": len(punkty),
                        "dolya": dolya, "schet": schet})
    vehi = []
    for v in sorted(data.get("veha", []), key=lambda v: v["srok"]):
        srok = v["srok"] if isinstance(v["srok"], dt.date) else dt.date.fromisoformat(str(v["srok"]))
        dney = (srok - segodnya).days
        vehi.append({"srok": srok.isoformat(), "nazvanie": v["nazvanie"], "status": v.get("status", "ozhidaet"),
                     "kto": v.get("kto", ""), "dney": dney})
    return {
        "proekt": data.get("proekt", ""), "segodnya": segodnya.isoformat(), "fail": path,
        "razdely": razdely, "zhdut": zhdut, "v_rabote": v_rabote, "vehi": vehi, "rashozhdeniya": rashozhdeniya,
        "sleduyushchee": (f"продолжить {v_rabote[0]}" if v_rabote else None) or data.get("sleduyushchee") or sled,
    }


def pechat(o):
    print(f"{o['proekt']} — прогресс на {dt.date.fromisoformat(o['segodnya']).strftime('%d.%m.%Y')}\n")
    w = max((len(r["nazvanie"]) for r in o["razdely"]), default=10)
    for r in o["razdely"]:
        s = r["schet"]
        detali = ", ".join(f"{STATUSY[k][2]} {STATUSY[k][0]} {v}" for k, v in s.items() if v)
        print(f"{r['nazvanie']:<{w}}  {polosa(r['dolya'])} {round(r['dolya'] * 100):>3} %  "
              f"({s['odobreno']}/{r['vsego']} одобрено; {detali})")
    if o["v_rabote"]:
        print("\nНе закончено (продолжить с записанного шага):")
        for z in o["v_rabote"]:
            print(f"  ▶ {z}")
    if o["vehi"]:
        print("\nВехи:")
        for v in o["vehi"]:
            if v["status"] == "sdelano":
                metka = "✓ сделано"
            elif v["dney"] < 0:
                metka = f"! просрочено на {-v['dney']} дн."
            else:
                metka = f"через {v['dney']} дн."
            kto = f" — {v['kto']}" if v["kto"] else ""
            print(f"  {dt.date.fromisoformat(v['srok']).strftime('%d.%m.%Y')}  {v['nazvanie']}  [{metka}]{kto}")
    if o["zhdut"]:
        print("\nЖдёт человека:")
        for z in o["zhdut"]:
            print(f"  – {z}")
    if o["rashozhdeniya"]:
        print("\nРасхождения с репозиторием:")
        for z in o["rashozhdeniya"]:
            print(f"  ! {z}")
    if o["sleduyushchee"]:
        print(f"\nДальше: {o['sleduyushchee']}")


def main(argv):
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    path = args[0] if args else najti()
    if not path or not os.path.isfile(path):
        print("progress.toml не найден. Создайте его по образцу tools/pisatel/progress.example.toml.")
        return 2
    with open(path, "rb") as f:
        data = tomllib.load(f)
    segodnya = dt.date.fromisoformat(os.environ["PROGRESS_DATE"]) if os.environ.get("PROGRESS_DATE") else dt.date.today()
    o = sobrat(data, path, segodnya)
    if as_json:
        print(json.dumps(o, ensure_ascii=False, indent=1))
    else:
        pechat(o)
    return 1 if o["rashozhdeniya"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
