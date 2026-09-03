import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from telethon import TelegramClient, events
from telethon.sessions import StringSession


# =========================
# LOAD CONFIG
# =========================

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "telethon_bot")

# Example:
# X_CHAT=@mychat
# or
# X_CHAT=-1001234567890
X_CHAT = os.getenv("X_CHAT")


# =========================
# VALIDATION
# =========================

if not API_ID:
    raise ValueError("API_ID missing in .env")

if not API_HASH:
    raise ValueError("API_HASH missing in .env")

if not SESSION_STRING:
    raise ValueError("SESSION_STRING missing in .env")

if not MONGO_URI:
    raise ValueError("MONGO_URI missing in .env")

if not X_CHAT:
    raise ValueError("X_CHAT missing in .env")


# Convert numeric X_CHAT to int
try:
    X_CHAT = int(X_CHAT)
except ValueError:
    pass


# =========================
# TELEGRAM CLIENT
# =========================

client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH
)


# =========================
# MONGODB
# =========================

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo[DB_NAME]

users_collection = db["users"]


# =========================
# SAVE USER
# =========================

async def save_user(user):
    """
    User already exists:
        -> Nothing happens

    User does not exist:
        -> User gets inserted
    """

    if not user:
        return

    # Bots / users without normal user ID
    if not getattr(user, "id", None):
        return

    user_id = user.id

    await users_collection.update_one(
        {
            "_id": user_id
        },
        {
            "$setOnInsert": {
                "user_id": user_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "created_at": datetime.now(timezone.utc)
            }
        },
        upsert=True
    )


# =========================
# NEW MESSAGE EVENT
# =========================

@client.on(events.NewMessage)
async def message_handler(event):

    # /get ko user tracking se exclude karo
    if event.raw_text.strip().lower() == "/get":
        return

    try:
        sender = await event.get_sender()

        if sender:
            await save_user(sender)

    except Exception as e:
        print(f"[ERROR] User save error: {e}")


# =========================
# /GET COMMAND
# ONLY X_CHAT
# =========================

@client.on(events.NewMessage(chats=X_CHAT))
async def get_stats(event):

    # Exact /get command
    if event.raw_text.strip().lower() != "/get":
        return

    try:
        total_users = await users_collection.count_documents({})

        await event.reply(
            "📊 **Database Stats**\n\n"
            f"👤 Total Users: `{total_users}`"
        )

    except Exception as e:

        print(f"[ERROR] Stats error: {e}")

        await event.reply(
            "❌ Database stats fetch karte waqt error aa gaya."
        )


# =========================
# START BOT
# =========================

async def main():

    print("Connecting to Telegram...")

    await client.start()

    me = await client.get_me()

    print()
    print("================================")
    print("      USERBOT STARTED")
    print("================================")
    print(f"Name : {me.first_name}")
    print(f"ID   : {me.id}")
    print("================================")
    print()

    await client.run_until_disconnected()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())