#!/usr/bin/env python3
"""
telegram_publish.py
Публикация сообщений, файлов и опросов в группу/канал Telegram через Bot API.

НАСТРОЙКА (см. подробную инструкцию в чате):
1. Создать бота через @BotFather -> получить BOT_TOKEN
2. Добавить бота в группу/канал как АДМИНИСТРАТОРА
3. Узнать CHAT_ID (см. функцию get_updates() ниже)
4. Прописать BOT_TOKEN и CHAT_ID ниже или через переменные окружения

Требуется: pip install requests --break-system-packages
"""

import os
import sys
import requests

# ── НАСТРОЙКИ ────────────────────────────────────────────────────────────
BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "ВСТАВЬТЕ_ТОКЕН_СЮДА")
CHAT_ID = os.environ.get("TG_CHAT_ID", "ВСТАВЬТЕ_CHAT_ID_СЮДА")  # например -1001234567890

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ── БАЗОВЫЕ ФУНКЦИИ ──────────────────────────────────────────────────────
def send_message(text: str, chat_id: str = None, parse_mode: str = "HTML"):
    """Отправить текстовое сообщение. parse_mode: HTML или Markdown."""
    chat_id = chat_id or CHAT_ID
    resp = requests.post(
        f"{API_URL}/sendMessage",
        json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
    )
    return _check(resp)


def send_document(file_path: str, caption: str = "", chat_id: str = None):
    """Отправить файл (docx, pdf, pptx и т.д.), например методичку."""
    chat_id = chat_id or CHAT_ID
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{API_URL}/sendDocument",
            data={"chat_id": chat_id, "caption": caption},
            files={"document": f},
        )
    return _check(resp)


def send_photo(file_path: str, caption: str = "", chat_id: str = None):
    """Отправить изображение (например, слайд или инфографику)."""
    chat_id = chat_id or CHAT_ID
    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{API_URL}/sendPhoto",
            data={"chat_id": chat_id, "caption": caption},
            files={"photo": f},
        )
    return _check(resp)


def send_poll(question: str, options: list, chat_id: str = None,
              anonymous: bool = True, allows_multiple: bool = False):
    """Отправить опрос — удобно для быстрой обратной связи от студентов."""
    chat_id = chat_id or CHAT_ID
    resp = requests.post(
        f"{API_URL}/sendPoll",
        json={
            "chat_id": chat_id,
            "question": question,
            "options": options,
            "is_anonymous": anonymous,
            "allows_multiple_answers": allows_multiple,
        },
    )
    return _check(resp)


def pin_message(message_id: int, chat_id: str = None):
    """Закрепить сообщение в группе/канале (например, дедлайн или объявление)."""
    chat_id = chat_id or CHAT_ID
    resp = requests.post(
        f"{API_URL}/pinChatMessage",
        json={"chat_id": chat_id, "message_id": message_id},
    )
    return _check(resp)


def get_updates():
    """
    Служебная функция: показать последние сообщения, полученные ботом.
    Используется ОДИН РАЗ при настройке, чтобы узнать CHAT_ID группы/канала.
    Порядок действий: 1) напишите что-нибудь в группе, где есть бот
                       2) запустите этот скрипт с аргументом --get-chat-id
    """
    resp = requests.get(f"{API_URL}/getUpdates")
    data = _check(resp)
    if not data:
        return
    chats = {}
    for upd in data.get("result", []):
        msg = upd.get("message") or upd.get("channel_post")
        if msg and "chat" in msg:
            chat = msg["chat"]
            chats[chat["id"]] = f'{chat.get("title") or chat.get("username")} ({chat.get("type")})'
    if not chats:
        print("Обновлений нет. Убедитесь, что бот добавлен в группу/канал "
              "и там есть хотя бы одно новое сообщение после добавления бота.")
    for cid, label in chats.items():
        print(f"CHAT_ID: {cid}    →    {label}")


def _check(resp):
    data = resp.json()
    if not data.get("ok"):
        print(f"Ошибка Telegram API: {data}", file=sys.stderr)
        return None
    return data


# ── ПРИМЕР ИСПОЛЬЗОВАНИЯ ─────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--get-chat-id":
        get_updates()
        sys.exit(0)

    # Пример: обычное объявление
    send_message(
        "📌 <b>Напоминание</b>\n\n"
        "Завтра — практика №5 (диаграмма Гантта). Принесите ноутбуки, "
        "класс 33-08."
    )

    # Пример: отправка методички
    # send_document("/path/to/OPDVP_Metodichka_Praktiki_1-2.docx",
    #               caption="Методичка к практикам №1-2")

    # Пример: опрос для обратной связи
    # send_poll("Насколько понятна была практика по WBS?",
    #           ["Всё понятно", "Есть вопросы", "Ничего не понял(а)"])
