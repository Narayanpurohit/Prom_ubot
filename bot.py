"""Main entry point: starts every configured Telegram user session."""
import asyncio
import logging

from motor.motor_asyncio import AsyncIOMotorClient
from telethon import TelegramClient
from telethon.sessions import StringSession

import config
from Plugins.userbot import register as register_userbot_plugin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("prom_ubot")


def parse_chat(value):
    value = str(value).strip()
    if not value:
        raise ValueError("X_CHAT is missing in config.py")
    try:
        return int(value)
    except ValueError:
        return value


async def run_session(session_name, session_string, db, x_chat):
    client = TelegramClient(
        StringSession(session_string),
        int(config.API_ID),
        config.API_HASH,
    )

    await client.start()
    me = await client.get_me()
    if not me:
        raise RuntimeError(f"{session_name}: Telegram did not return an account")

    register_userbot_plugin(client, db, x_chat)
    log.info("%s started as @%s (user ID %s)", session_name, me.username, me.id)

    try:
        await client.run_until_disconnected()
    finally:
        await client.disconnect()


async def main():
    if not config.API_ID or not config.API_HASH:
        raise ValueError("Set API_ID and API_HASH in config.py")
    if not config.MONGO_URI:
        raise ValueError("Set MONGO_URI in config.py")

    sessions = [
        ("String1", config.STRING1),
        ("String2", config.STRING2),
        ("String3", config.STRING3),
        ("String4", config.STRING4),
    ]
    sessions = [(name, value.strip()) for name, value in sessions if value and value.strip()]
    if not sessions:
        raise ValueError("Add at least one valid session string (STRING1–STRING4) in config.py")

    x_chat = parse_chat(config.X_CHAT)
    mongo = AsyncIOMotorClient(config.MONGO_URI)
    db = mongo[config.DB_NAME]

    try:
        results = await asyncio.gather(
            *(run_session(name, session, db, x_chat) for name, session in sessions),
            return_exceptions=True,
        )
        failures = [result for result in results if isinstance(result, BaseException)]
        for failure in failures:
            log.exception("A userbot session stopped with an error", exc_info=failure)
        if failures:
            raise RuntimeError(f"{len(failures)} userbot session(s) failed to start or stopped")
    finally:
        mongo.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Shutdown requested")
