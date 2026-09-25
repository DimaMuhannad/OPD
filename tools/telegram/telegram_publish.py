#!/usr/bin/env python3
"""
telegram_publish.py
Публикация сообщений, файлов и опросов в группы Telegram (форум-режим с темами)
через Bot API.

НАСТРОЙКА
1. Бот создан через @BotFather, добавлен администратором в обе группы.
2. Токен — только в переменной окружения TG_BOT_TOKEN (в код и в вывод не попадает).
3. ID групп и тем — в groups.json рядом со скриптом (не секрет). Узнать их:
       python3 telegram_publish.py updates
   (перед этим написать что-нибудь в каждую тему — бот видит только новые
   сообщения, отправленные после его добавления, и хранит их не дольше суток).

КОМАНДЫ
    updates                              — группы и темы из getUpdates
    publish <папка> [--group G] [--send] [--no-files]
                                         — комплект постов (по умолчанию только
                                           показать, что будет отправлено;
                                           --no-files — без вложений .files)
    test <группа> <тема> [текст]         — тестовое сообщение, печатает message_id
    delete <группа> <message_id>         — удалить сообщение

Группа — ключ из groups.json (m631k, m531) или all; тема — ключ темы
(obyavleniya, materialy, domashnee_zadanie, literatura).

КОМПЛЕКТ ПОСТОВ — папка с файлами <N>_<тема>.txt (порядок — по N).
Рядом может лежать <N>_<тема>.files — список приложений, по пути от корня
репозитория на строку; они уходят вслед за текстом в ту же тему.
«Объявления» отправляются последними: строка-плейсхолдер вида
«[после публикации вставить сюда ссылки …]» заменяется ссылками на уже
отправленные сообщения этого комплекта.

Требуется: pip install requests
"""

import html
import json
import os
import re
import sys
from pathlib import Path

import requests

# ── НАСТРОЙКИ ────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TG_CHAT_ID", "")  # группа по умолчанию, например -1001234567890

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
GROUPS_FILE = HERE / "groups.json"
SENT_LOG = HERE / "sent_log.jsonl"

ANNOUNCE_TOPIC = "obyavleniya"
TOPIC_TITLES = {
    "obyavleniya": "Объявления",
    "materialy": "Материалы",
    "domashnee_zadanie": "Домашнее задание",
    "literatura": "Литература",
}
PLACEHOLDER_RE = re.compile(r"^\[после публикации вставить[^\]]*\]\s*$", re.M)


# ── БАЗОВЫЕ ФУНКЦИИ ──────────────────────────────────────────────────────
# thread_id — ID темы (message_thread_id). None или 1 — тема «General»:
# в неё Bot API требует писать без message_thread_id.
def _thread(payload: dict, thread_id):
    if thread_id not in (None, "", 1, "1"):
        payload["message_thread_id"] = int(thread_id)
    return payload


def send_message(text: str, chat_id: str = None, thread_id=None,
                 parse_mode: str = "HTML", link_preview: bool = True):
    """Отправить текстовое сообщение. parse_mode: HTML, Markdown или None."""
    payload = {"chat_id": chat_id or CHAT_ID, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if not link_preview:
        payload["link_preview_options"] = {"is_disabled": True}
    return _call("sendMessage", json=_thread(payload, thread_id))


def send_document(file_path: str, caption: str = "", chat_id: str = None,
                  thread_id=None):
    """Отправить файл (docx, pdf, pptx и т.д.), например методичку."""
    with open(file_path, "rb") as f:
        return _call("sendDocument",
                     data=_thread({"chat_id": chat_id or CHAT_ID,
                                   "caption": caption}, thread_id),
                     files={"document": f})


def send_documents(file_paths: list, chat_id: str = None, thread_id=None):
    """Отправить 2–10 файлов одним альбомом (sendMediaGroup)."""
    if len(file_paths) == 1:
        return send_document(file_paths[0], chat_id=chat_id, thread_id=thread_id)
    handles = {f"f{i}": open(p, "rb") for i, p in enumerate(file_paths)}
    try:
        media = [{"type": "document", "media": f"attach://{k}"} for k in handles]
        return _call("sendMediaGroup",
                     data=_thread({"chat_id": chat_id or CHAT_ID,
                                   "media": json.dumps(media)}, thread_id),
                     files=handles)
    finally:
        for h in handles.values():
            h.close()


def send_photo(file_path: str, caption: str = "", chat_id: str = None,
               thread_id=None):
    """Отправить изображение (например, слайд или инфографику)."""
    with open(file_path, "rb") as f:
        return _call("sendPhoto",
                     data=_thread({"chat_id": chat_id or CHAT_ID,
                                   "caption": caption}, thread_id),
                     files={"photo": f})


def send_poll(question: str, options: list, chat_id: str = None, thread_id=None,
              anonymous: bool = True, allows_multiple: bool = False):
    """Отправить опрос — удобно для быстрой обратной связи от студентов."""
    return _call("sendPoll", json=_thread({
        "chat_id": chat_id or CHAT_ID,
        "question": question,
        "options": [{"text": o} for o in options],
        "is_anonymous": anonymous,
        "allows_multiple_answers": allows_multiple,
    }, thread_id))


def pin_message(message_id: int, chat_id: str = None):
    """Закрепить сообщение (в форуме — закрепляется в своей теме)."""
    return _call("pinChatMessage",
                 json={"chat_id": chat_id or CHAT_ID, "message_id": message_id})


def delete_message(message_id: int, chat_id: str = None):
    """Удалить сообщение (бот-администратор может удалить и чужое)."""
    return _call("deleteMessage",
                 json={"chat_id": chat_id or CHAT_ID, "message_id": message_id})


def message_link(chat_id, thread_id, message_id) -> str:
    """Ссылка на сообщение в теме закрытой группы: t.me/c/<id без -100>/<тема>/<id>."""
    internal = str(chat_id).removeprefix("-100")
    if thread_id in (None, "", 1, "1"):
        return f"https://t.me/c/{internal}/{message_id}"
    return f"https://t.me/c/{internal}/{thread_id}/{message_id}"


def _call(method: str, **kwargs):
    if not BOT_TOKEN:
        sys.exit("Не задана переменная окружения TG_BOT_TOKEN.")
    try:
        resp = requests.post(f"{API_URL}/{method}", timeout=60, **kwargs)
        data = resp.json()
    except Exception as e:  # в тексте исключения может оказаться URL с токеном
        print(f"Сбой запроса {method}: {str(e).replace(BOT_TOKEN, '***')}",
              file=sys.stderr)
        return None
    if not data.get("ok"):
        print(f"Ошибка Telegram API ({method}): {data}", file=sys.stderr)
        return None
    return data


# ── ГРУППЫ И ТЕМЫ ────────────────────────────────────────────────────────
def load_groups() -> dict:
    """groups.json: {"m631k": {"chat_id": -100…, "topics": {"materialy": 3, …}}, …}"""
    if not GROUPS_FILE.exists():
        sys.exit(f"Нет {GROUPS_FILE.name} — сначала узнать ID: команда updates.")
    return json.loads(GROUPS_FILE.read_text(encoding="utf-8"))


def pick_groups(groups: dict, key: str) -> list:
    if key == "all":
        return list(groups)
    if key not in groups:
        sys.exit(f"Группа «{key}» не найдена в {GROUPS_FILE.name}: {list(groups)}")
    return [key]


def get_updates():
    """
    Показать группы и темы, из которых бот получил сообщения.
    Порядок: 1) написать что-нибудь в каждую тему группы, где бот — админ;
             2) запустить: telegram_publish.py updates
    Название темы берётся из сервисного сообщения о создании темы
    (forum_topic_created) — своего или того, на которое «отвечает» сообщение.
    """
    data = _call("getUpdates", json={"allowed_updates": []})
    if not data:
        return
    chats, topics = {}, {}
    for upd in data.get("result", []):
        msg = (upd.get("message") or upd.get("edited_message")
               or upd.get("channel_post"))
        if not msg or "chat" not in msg:
            continue
        chat = msg["chat"]
        chats[chat["id"]] = (f'{chat.get("title") or chat.get("username")} '
                             f'({chat.get("type")}, форум: {bool(chat.get("is_forum"))})')
        tid = msg.get("message_thread_id") if msg.get("is_topic_message") else None
        created = (msg.get("forum_topic_created")
                   or (msg.get("reply_to_message") or {}).get("forum_topic_created"))
        key = (chat["id"], tid)
        if tid is None:
            topics[key] = "General (без message_thread_id)"
        elif created or topics.get(key, "?") == "?":
            topics[key] = (created or {}).get("name", "?")
    if not chats:
        print("Обновлений нет. Бот хранит сообщения не дольше суток и видит "
              "только написанные после его добавления администратором — "
              "напишите в каждую тему заново и повторите.")
    for cid, label in chats.items():
        print(f"CHAT_ID: {cid}    →    {label}")
        for (c, tid), name in sorted(topics.items(), key=lambda x: x[0][1] or 0):
            if c == cid:
                print(f"    message_thread_id: {tid}    →    {name}")


# ── КОМПЛЕКТ ПОСТОВ ──────────────────────────────────────────────────────
def load_kit(folder: Path) -> list:
    """Посты комплекта: [(номер, тема, текст, [приложения])], порядок по номеру."""
    posts = []
    for p in folder.glob("*.txt"):
        m = re.fullmatch(r"(\d+)_(\w+)\.txt", p.name)
        if not m:
            continue
        num, topic = int(m[1]), m[2]
        if topic not in TOPIC_TITLES:
            sys.exit(f"{p.name}: неизвестная тема «{topic}», ожидается {list(TOPIC_TITLES)}")
        files = []
        manifest = p.with_suffix(".files")
        if manifest.exists():
            for line in manifest.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    fp = REPO_ROOT / line
                    if not fp.is_file():
                        sys.exit(f"{manifest.name}: нет файла {line}")
                    files.append(fp)
        if len(files) > 10:
            sys.exit(f"{manifest.name}: больше 10 файлов — Telegram не отправит альбомом")
        posts.append((num, topic, p.read_text(encoding="utf-8").strip(), files))
    posts.sort()
    # «Объявления» — последними: в них подставляются ссылки на остальные посты
    return ([x for x in posts if x[1] != ANNOUNCE_TOPIC]
            + [x for x in posts if x[1] == ANNOUNCE_TOPIC])


def render(text: str, links: list) -> str:
    """Текст поста → HTML; плейсхолдер заменяется списком ссылок."""
    body = html.escape(text, quote=False)
    link_block = "\n".join(f'→ <a href="{url}">{html.escape(title)}</a>'
                           for title, url in links)
    return PLACEHOLDER_RE.sub(lambda _: link_block, body) if links else body


def publish_kit(folder: Path, group_key: str, group: dict, send: bool,
                with_files: bool = True):
    posts = load_kit(folder)
    if not with_files:
        posts = [(n, t, x, []) for n, t, x, _ in posts]
    chat_id, topic_ids = group["chat_id"], group["topics"]
    for _, topic, _, _ in posts:
        if topic not in topic_ids:
            sys.exit(f"В groups.json для {group_key} нет темы «{topic}»")
        if send and (chat_id is None or topic_ids[topic] is None):
            sys.exit(f"В groups.json для {group_key} не заполнены ID (группа/тема «{topic}»)")
    links, log = [], []
    print(f"\n══ {folder.name} → {group_key} ({chat_id}) "
          f"{'ОТПРАВКА' if send else '— пробный прогон, ничего не отправляется'}")
    for num, topic, text, files in posts:
        tid = topic_ids[topic]
        is_announce = topic == ANNOUNCE_TOPIC
        body = render(text, links if is_announce else [])
        print(f"\n── {num}. {TOPIC_TITLES[topic]} (тема {tid})")
        print(body)
        for f in files:
            print(f"   📎 {f.relative_to(REPO_ROOT)}")
        if is_announce and PLACEHOLDER_RE.search(text) is None and links:
            print("   (плейсхолдера для ссылок нет — ссылки не подставлены)")
        if not send:
            links.append((TOPIC_TITLES[topic], message_link(chat_id, tid, "…")))
            continue
        res = send_message(body, chat_id=chat_id, thread_id=tid,
                           link_preview=not is_announce)
        if not res:
            sys.exit(f"Остановлено на посте {num} — уже отправленное см. в {SENT_LOG.name}")
        mid = res["result"]["message_id"]
        url = message_link(chat_id, tid, mid)
        log.append({"kit": folder.name, "group": group_key, "topic": topic,
                    "message_id": mid, "url": url})
        if files:
            fres = send_documents([str(f) for f in files], chat_id=chat_id, thread_id=tid)
            if not fres:
                sys.exit(f"Файлы к посту {num} не отправлены — текст уже в группе: {url}")
            r = fres["result"]
            for m in (r if isinstance(r, list) else [r]):
                log.append({"kit": folder.name, "group": group_key, "topic": topic,
                            "message_id": m["message_id"], "attachment": True})
        links.append((TOPIC_TITLES[topic], url))
        print(f"   ✔ {url}")
        with SENT_LOG.open("a", encoding="utf-8") as fh:
            for rec in log:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        log = []


# ── КОМАНДНАЯ СТРОКА ─────────────────────────────────────────────────────
def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    if cmd in ("updates", "--get-chat-id"):
        get_updates()
    elif cmd == "publish":
        if not args:
            sys.exit("Укажите папку комплекта: publish tools/telegram/posts/<папка>")
        folder = Path(args[0])
        group = args[args.index("--group") + 1] if "--group" in args else "all"
        groups = load_groups()
        for key in pick_groups(groups, group):
            publish_kit(folder, key, groups[key], send="--send" in args,
                        with_files="--no-files" not in args)
    elif cmd == "test":
        if len(args) < 2:
            sys.exit("test <группа> <тема> [текст]")
        g = load_groups()[args[0]]
        if g["chat_id"] is None or g["topics"].get(args[1], None) is None:
            sys.exit(f"В groups.json для {args[0]} не заполнены ID (группа/тема «{args[1]}»)")
        text = " ".join(args[2:]) or "Тестовое сообщение бота — будет удалено."
        res = send_message(text, chat_id=g["chat_id"], thread_id=g["topics"][args[1]],
                           parse_mode=None)
        if res:
            mid = res["result"]["message_id"]
            print(f"message_id: {mid}    {message_link(g['chat_id'], g['topics'][args[1]], mid)}")
    elif cmd == "delete":
        if len(args) != 2:
            sys.exit("delete <группа> <message_id>")
        if delete_message(int(args[1]), chat_id=load_groups()[args[0]]["chat_id"]):
            print("Удалено.")
    else:
        sys.exit(f"Неизвестная команда: {cmd}. См. --help")


if __name__ == "__main__":
    main(sys.argv[1:])
