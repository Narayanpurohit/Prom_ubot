"""Group listener and consent-based messaging for userbot session 1."""
import asyncio
import random

from telethon import events, utils


def register(client, db, x_chat):
    peer_bots = db["peer_bot"]
    users = db["users"]

    async def own_bot_id():
        me = await client.get_me()
        return int(me.id) if me else None

    @client.on(events.NewMessage(chats=x_chat, incoming=True))
    async def handle_group_message(event):
        sender = await event.get_sender()
        if not sender or getattr(sender, "bot", False) or not getattr(sender, "id", None):
            return

        user_id = int(sender.id)
        try:
            input_sender = await event.get_input_sender()
            if not input_sender:
                return
            peer_id = int(utils.get_peer_id(input_sender))
        except Exception:
            return

        bot_id = await own_bot_id()
        if not bot_id:
            return

        await peer_bots.update_one(
            {"_id": bot_id},
            {
                "$setOnInsert": {"bot_id": bot_id},
                "$addToSet": {
                    "user_ids": {"$each": [bot_id, user_id]},
                    "peer_ids": peer_id,
                },
            },
            upsert=True,
        )

    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private, pattern=r"^/subscribe(?:@\w+)?$"))
    async def subscribe(event):
        user_id = int(event.sender_id)
        bot_id = await own_bot_id()
        if not bot_id or user_id == bot_id:
            return
        await users.update_one(
            {"bot_id": bot_id, "user_id": user_id},
            {"$set": {"bot_id": bot_id, "user_id": user_id, "subscribed": True}},
            upsert=True,
        )
        await event.reply("You’re subscribed. Reply /stop any time to stop receiving messages.")

    @client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private, pattern=r"^/stop(?:@\w+)?$"))
    async def unsubscribe(event):
        user_id = int(event.sender_id)
        bot_id = await own_bot_id()
        if not bot_id:
            return
        result = await users.delete_one({"bot_id": bot_id, "user_id": user_id})
        if result.deleted_count:
            await event.reply("You’ve been unsubscribed. No further broadcasts will be sent.")
        else:
            await event.reply("You weren’t subscribed; no broadcast messages will be sent.")

    @client.on(events.NewMessage(outgoing=True, pattern=r"^/broadcast(?:@\w+)?$"))
    async def broadcast(event):
        bot_id = await own_bot_id()
        if not bot_id:
            return
        import config

        if bot_id not in {int(owner_id) for owner_id in config.OWNERS_ID}:
            await event.reply("This command is restricted to configured owners.")
            return

        source = await event.get_reply_message()
        if not source:
            await event.reply("Reply to a message with /broadcast to send it to subscribed users.")
            return

        cursor = users.find({"bot_id": bot_id, "subscribed": True}, {"user_id": 1})
        user_ids = [int(doc["user_id"]) async for doc in cursor if doc.get("user_id")]
        sent = 0
        failed = 0
        for user_id in user_ids:
            try:
                await client.forward_messages(user_id, source)
                sent += 1
            except Exception:
                failed += 1
            if user_id != user_ids[-1]:
                await asyncio.sleep(random.uniform(2, 20))
        await event.reply(f"Broadcast finished. Sent: {sent}; failed: {failed}.")
