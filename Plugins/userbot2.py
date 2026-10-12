from telethon import events

from Plugins.function import (
    is_user_in_collection,
    add_user_to_collection,
    process_users,
)


# =====================================
# USERBOT 2 SETTINGS
# =====================================

COLLECTION1 = "002"
COLLECTION2 = "012"

P_MSG = (
    "🚀 Process Started!\n\n"
    "User processing has started successfully."
)


# =====================================
# ERROR LOGGING
# =====================================

async def send_error_log(
    client,
    log_chat_id,
    bot_name,
    error,
    message_id=None,
):
    try:
        message = (
            f"⚠️ {bot_name} ERROR\n\n"
            f"Type: {type(error).__name__}\n"
            f"Details: {str(error)[:2500]}\n"
            f"Message ID: {message_id}"
        )

        await client.send_message(log_chat_id, message)

    except Exception as log_error:
        print(f"[{bot_name}] Logging failed: {log_error}")


# =====================================
# REGISTER HANDLERS
# =====================================

def register(client, db, support_chat_id, log_chat_id):

    collection1 = db[COLLECTION1]
    collection2 = db[COLLECTION2]

    # =================================
    # SUPPORT GROUP MONITOR
    # =================================

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

            user_id = getattr(sender, "id", None)

            if not isinstance(user_id, int) or user_id <= 0:
                return

            # Ignore users already in either collection.
            if await is_user_in_collection(collection1, user_id):
                return

            if await is_user_in_collection(collection2, user_id):
                return

            # Try resolving the user's input peer.
            await client.get_input_entity(sender)

            # Add user to Userbot 2's collection.
            await add_user_to_collection(
                collection2,
                user_id,
            )

            print(
                f"[Userbot 2] User {user_id} "
                f"added to {COLLECTION2}"
            )

        except Exception as error:
            await send_error_log(
                client,
                log_chat_id,
                "Userbot 2",
                error,
                event.id,
            )

    # =================================
    # PROCESS COMMAND
    # =================================

    @client.on(
        events.NewMessage(
            chats=support_chat_id,
            pattern=r"^/process(?:@\w+)?$",
        )
    )
    async def process_command(event):

        try:
            await process_users(
                client=client,
                collection1=collection1,
                collection2=collection2,
                p_msg=P_MSG,
                log_chat_id=log_chat_id,
                bot_name="Userbot 2",
            )

        except Exception as error:
            await send_error_log(
                client,
                log_chat_id,
                "Userbot 2",
                error,
                event.id,
            )

    print("[Userbot 2] Handlers registered.")