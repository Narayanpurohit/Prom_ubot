"""Group listener for userbot session 4."""
from telethon import events, utils


def register(client, db, x_chat):
    peer_bots = db["peer_bot"]

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

        me = await client.get_me()
        if not me:
            return

        bot_id = int(me.id)
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
