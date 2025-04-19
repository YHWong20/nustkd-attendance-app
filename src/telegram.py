"""
Telegram bot utilities
"""

import asyncio
import os
import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)8s: %(message)s"
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
GROUP_CHAT_ID = int(os.environ["GROUP_CHAT_ID"])
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def send_message(day_month, entries=None, duplicates=None, missing=None):
    """
    Send message to telegram chat.

    Args:
        day_month (str): Day and month for attendance data.
        entries (list, optional): List of name (str) entries. Defaults to None.
        duplicates (list, optional): List of duplicate names (str). Defaults to None.
        missing (list, optional): List of missing names (str). Defaults to None.
    """
    formatted_message = None
    if entries:
        logging.info("Generating attendance message.")
        formatted_message = generate_attendance_message(day_month, entries)
    elif duplicates or missing:
        logging.info("Generating export status message.")
        formatted_message = generate_export_message(day_month, duplicates, missing)

    if formatted_message:
        asyncio.run(send_formatted_message(formatted_message))


def generate_attendance_message(day_month, entries):
    """
    Generate formatted attendance message.

    Args:
        day_month (str): Day and month for attendance data.
        entries (list, optional): List of name (str) entries.

    Returns:
        str: Formatted attendance message.
    """
    students = ""
    alumni = ""
    exchangers = ""

    for entry in entries:
        if entry["status"] == "Regular":
            students += f"{entry['name']}\n"
        elif entry["status"] == "Alumni":
            alumni += f"{entry['name']}\n"
        elif entry["status"] == "Exchange":
            exchangers += f"{entry['name']}\n"

    logging.info("Formatted attendance message generated.")
    return (
        f"Attendance for {day_month}:\n\n"
        "<b>Students</b>\n"
        f"{students}\n"
        "<b>Alumni</b>\n"
        f"{alumni}\n"
        "<b>Exchangers</b>\n"
        f"{exchangers}"
    )


def generate_export_message(day_month, duplicates, missing):
    """
    Generate formatted export status message.

    Args:
        day_month (str): Day and month for attendance data.
        duplicates (list, optional): List of duplicate name (str) entries.
        missing (list, optional): List of missing name (str) entries.

    Returns:
        str: Formatted attendance message.
    """
    _duplicates = ""
    _missing = ""

    for dupe in duplicates:
        _duplicates += f"{dupe}\n"

    for miss in missing:
        _missing += f"{miss}\n"

    logging.info("Formatted export status message generated.")
    return (
        f"Attendance for {day_month} exported to Google Drive.\n\n"
        "<b>Missing Members</b>\n"
        f"{_missing}\n"
        "<b>Duplicate Members</b>\n"
        f"{_duplicates}\n"
    )


async def send_formatted_message(message):
    """
    Async send message using Telegram bot.

    Args:
        message (str): Formatted message to send.
    """
    try:
        async with bot:
            await bot.send_message(chat_id=GROUP_CHAT_ID, text=message)
    except Exception as e:
        logging.error("Error sending message. Error: %s", e)
        raise e
