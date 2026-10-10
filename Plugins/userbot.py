"""Shared group plugin for all configured user sessions.

To respect members' consent, a user is added to MongoDB only after they send
/join in X_CHAT. They can opt out at any time with /leave.
"""
from datetime import datetime, timezone

from telethon import events, utils


def register(client, db, x_chat):
    pending_users = db["pending_users"]
    peer_bots = db["peer_bot"]

    @client.on(events.NewMessage(chats=x_chat, incoming=True))
    async def handle_group_message(event):
        sender = await event.get_sender()

        # Ignore bots and messages without a resolvable user sender.
        if not sender or getattr(sender, "bot", False) or not getattr(sender, "id", None):
            return

        text = (event.raw_text or "").strip().lower()
        user_id = int(sender.id)

        # Only store users who explicitly opt in.
        if text == "/join":
            try:
                # Resolve the peer through Telegram; get_peer_id returns its marked peer ID.
                entity = await client.get_input_entity(user_id)
                peer_id = int(utils.get_peer_id(entity))
            except Exception:
                # If Telegram cannot resolve the peer, do not store a guessed ID.
                return

            now = datetime.now(timezone.utc)
            await pending_users.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "peer_id": peer_id,
                        "source_chat": str(x_chat),
                        "status": "pending",
                        "opted_in_at": now,
                        "updated_at": now,
                    }
                },
                upsert=True,
            )

            # Each userbot account has its own record. Keep its own ID and
            # explicitly opted-in user IDs in that account's user_ids list.
            me = await client.get_me()
            if me:
                await peer_bots.update_one(
                    {"_id": int(me.id)},
                    {
                        "$setOnInsert": {"bot_id": int(me.id)},
                        "$addToSet": {"user_ids": {"$each": [int(me.id), user_id]}},
                    },
                    upsert=True,
                )

            await event.reply("You're registered. Send /leave any time to opt out.")

        elif text == "/leave":
            await pending_users.update_one(
                {"user_id": user_id},
                {"$set": {"status": "opted_out", "updated_at": datetime.now(timezone.utc)}},
            )
            me = await client.get_me()
            if me:
                await peer_bots.update_one(
                    {"_id": int(me.id)},
                    {"$pull": {"user_ids": user_id}},
                )
            await event.reply("You've been removed from the active list.")
