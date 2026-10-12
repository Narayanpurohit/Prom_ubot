import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession
from motor.motor_asyncio import AsyncIOMotorClient

import config

from Plugins import userbot1, userbot2


async def main():
    # =====================================
    # MONGODB CONNECTION
    # =====================================

    mongo_client = AsyncIOMotorClient(
        config.MONGO_URI,
        serverSelectionTimeoutMS=10000
    )

    db = mongo_client[config.MONGO_DB_NAME]

    # Verify MongoDB connection.
    await mongo_client.admin.command("ping")

    print("[MongoDB] Connected successfully.")

    # =====================================
    # USERBOT 1 CLIENT
    # =====================================

    client1 = TelegramClient(
        StringSession(config.STRING_SESSION_1),
        config.API_ID_1,
        config.API_HASH_1
    )

    # =====================================
    # USERBOT 2 CLIENT
    # =====================================

    client2 = TelegramClient(
        StringSession(config.STRING_SESSION_2),
        config.API_ID_2,
        config.API_HASH_2
    )

    clients = [client1, client2]

    try:
        # Connect both clients.
        await asyncio.gather(
            *[
                client.start()
                for client in clients
            ]
        )

        # Confirm account identities.
        me1, me2 = await asyncio.gather(
            client1.get_me(),
            client2.get_me()
        )

        print(
            f"[Userbot 1] Connected: "
            f"@{me1.username or me1.id}"
        )

        print(
            f"[Userbot 2] Connected: "
            f"@{me2.username or me2.id}"
        )

        # Register plugin handlers.
        userbot1.register(
            client1,
            db,
            config.SUPPORT_CHAT_ID,
            config.LOG_CHAT_ID
        )

        userbot2.register(
            client2,
            db,
            config.SUPPORT_CHAT_ID,
            config.LOG_CHAT_ID
        )

        print("[System] Both userbots are running.")

        # Keep both clients running.
        await asyncio.gather(
            *[
                client.run_until_disconnected()
                for client in clients
            ]
        )

    finally:
        # Disconnect both clients and close MongoDB.
        await asyncio.gather(
            *[
                client.disconnect()
                for client in clients
            ],
            return_exceptions=True
        )

        mongo_client.close()

        print("[System] All connections closed.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[System] Stopped by user.")