import asyncio

from telethon import events

from Plugins.function import (
    is_user_in_collection,
    add_user_to_collection,
    process_users,
)

# =====================================
# USERBOT 1 SETTINGS
# =====================================

COLLECTION1 = "collection1"
COLLECTION2 = "collection2"

P_MSG = (
    "🚀 Process Started!\n\n"
    "User processing has started successfully."
)


def register(client, db, support_chat_id, log_chat_id):

    collection1 = db[COLLECTION1]
    collection2 = db[COLLECTION2]

    @client.on(events.NewMessage(chats=support_chat_id))
    async def monitor_support_group(event):

        if not event.is_group:
            return

        try:
            sender = await event.get_sender()

            if sender is None:
                return

            # Ignore bot accounts.
            if getattr(sender, "bot", False):
                return

            user_id = sender.id

            if not isinstance(user_id, int) or user_id <= 0:
                return

            # Ignore users already in either collection.
            if await is_user_in_collection(collection1, user_id):
                return

            if await is_user_in_collection(collection2, user_id):
                return

            # Try resolving the input peer.
            await client.get_input_entity(user_id)

            await add_user_to_collection(
                collection1,
                user_id
            )

            print(
                f"[Userbot 1] User {user_id} processed."
            )

        except Exception as error:

            await send_error_log(
                client,
                log_chat_id,
                "Userbot 1",
                error,
                event.id
            )

    @client.on(events.NewMessage(
        chats=support_chat_id,
        pattern=r"^/process(?:@\w+)?$"
    ))
    async def process_command(event):

        try:
            # Only allow commands from group admins.
            permissions = await event.get_permissions(
                event.chat_id,
                event.sender_id
            )

            if not (
                permissions.is_admin
                or permissions.is_creator
            ):
                return

            await process_users(
                client=client,
                collection1=collection1,
                collection2=collection2,
                p_msg=P_MSG,
                log_chat_id=log_chat_id,
                bot_name="Userbot 1",
            )

        except Exception as error:

            await send_error_log(
                client,
                log_chat_id,
                "Userbot 1",
                error,
                event.id
            )


async def send_error_log(
    client,
    log_chat_id,
    bot_name,
    error,
    message_id=None
):
    try:
        await client.send_message(
            log_chat_id,
            (
                f"⚠️ {bot_name} ERROR\n\n"
                f"Type: {type(error).__name__}\n"
                f"Details: {error}\n"
                f"Message ID: {message_id}"
            )
        )
    except Exception as log_error:
        print(f"[Logging Error] {log_error}")