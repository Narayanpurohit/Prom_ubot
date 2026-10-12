from pymongo.errors import DuplicateKeyError


async def is_user_in_collection(collection, user_id):
    """
    Check whether a user ID exists in a collection.
    """
    document = await collection.find_one(
        {"_id": int(user_id)},
        {"_id": 1}
    )

    return document is not None


async def add_user_to_collection(collection, user_id):
    """
    Add a user ID to a collection.
    Returns True if inserted, False if already present.
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


async def remove_user_from_collection(collection, user_id):
    """
    Remove a user ID from a collection.
    Returns True if a document was deleted.
    """
    result = await collection.delete_one(
        {"_id": int(user_id)}
    )

    return result.deleted_count > 0