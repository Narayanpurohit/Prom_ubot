import asyncio
import random

from pymongo.errors import DuplicateKeyError


# =====================================
# CHECK USER IN COLLECTION
# =====================================

async def is_user_in_collection(collection, user_id):
    """
    Check whether a user ID exists in MongoDB.
    """

    document = await collection.find_one(
        {"_id": int(user_id)},
        {"_id": 1}
    )

    return document is not None


# =====================================
# ADD USER TO COLLECTION
# =====================================

async def add_user_to_collection(collection, user_id):
    """
    Add a user ID to MongoDB.
    Returns True if inserted, otherwise False.
    """

    try:
        result = await collection.update_one(
            {"_id": int(user_id)},
            {"$setOnInsert": {"_id": int(user_id)}},
            upsert=True
        )

        return result.upserted_id is not None

    except DuplicateKeyError:
        return False


# =====================================
# REMOVE USER FROM COLLECTION
# =====================================

async def remove_user_from_collection(collection, user_id):
    """
    Remove a user ID from MongoDB.
    Returns True if removed, otherwise False.
    """

    result = await collection.delete_one(
        {"_id": int(user_id)}
    )

    return result.deleted_count > 0


# =====================================
# PROCESS USERS
# =====================================

async def process_users(
    client,
    collection1,
    collection2,
    p_msg,
    log_chat_id,
    bot_name="Userbot",
):
    """
    1. Send P_MSG to the admin.
    2. Check collection1.
    3. Select one user ID.
    4. Add the ID to collection2.
    5. Remove the ID from collection1.
    6. Wait for a random 35-57 minutes.
    """

    # Send the configured process-start message.
    

    # Fetch one user ID from collection1.
    document = await collection1.find_one(
        {},
        {"_id": 1}
    )

    # Stop if collection1 is empty.
    if document is None:
        await client.send_message(
            log_chat_id,
            (
                f"ℹ️ {bot_name}\n\n"
                "Collection 1 is empty. "
                "No users to process."
            )
        )
        return

    user_id = int(document["_id"])

    # Add to destination before removing from source.
    try:
        await client.send_message(
        user_id,
        p_msg
    )
        await collection2.update_one(
            {"_id": user_id},
            {"$setOnInsert": {"_id": user_id}},
            upsert=True
        )

    except DuplicateKeyError:
        pass

    # Remove the selected ID from collection1.
    await collection1.delete_one(
        {"_id": user_id}
    )

    # Report successful transfer.
    await client.send_message(
        log_chat_id,
        (
            f"✅ {bot_name}\n\n"
            "User ID transferred successfully.\n"
            f"User ID: {user_id}"
        )
    )

    # Random delay between 35 and 57 minutes.
    delay_minutes = random.randint(35, 57)

    await client.send_message(
        log_chat_id,
        (
            f"⏳ {bot_name}\n\n"
            f"Waiting {delay_minutes} minutes."
        )
    )

    await asyncio.sleep(delay_minutes * 60)