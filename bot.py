impot os
from datetime import datetime, timezone

from telethon import TelegramClient, events
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


# =========================
# CONFIG
# =========================

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "userbot")

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "telethon_bot")

# Username: @mychat
# Ya numeric chat ID bhi use kar sakte ho
X_CHAT = os.getenv("X_CHAT")


# =========================
# TELEGRAM
# =========================

client = TelegramClient(
    SESSION_NAME,
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
    User DB me already exist karta hai to ignore.
    Nahi karta to insert.
    """

    if not user:
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
# EVENT HANDLER
# =========================

@client.on(events.NewMessage)
async def message_handler(event):

    # /get ko normal user tracking se exclude kar rahe hain
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
            "❌ Stats fetch karte waqt error aa gaya."
        )


# =========================
# START
# =========================

async def main():

    print("Connecting to Telegram...")

    await client.start()

    me = await client.get_me()

    print("--------------------------------")
    print("✅ Userbot Started")
    print(f"👤 Account: {me.first_name}")
    print(f"🆔 ID: {me.id}")
    print("--------------------------------")

    await client.run_until_disconnected()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
