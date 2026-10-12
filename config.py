import os

# ==============================
# TELEGRAM USERBOT 1 CONFIG
# ==============================

API_ID_1 = int(os.getenv("API_ID_1", "12345678"))
API_HASH_1 = os.getenv("API_HASH_1", "YOUR_API_HASH_1")
STRING_SESSION_1 = os.getenv("STRING_SESSION_1", "YOUR_STRING_SESSION_1")


# ==============================
# TELEGRAM USERBOT 2 CONFIG
# ==============================

API_ID_2 = int(os.getenv("API_ID_2", "12345678"))
API_HASH_2 = os.getenv("API_HASH_2", "YOUR_API_HASH_2")
STRING_SESSION_2 = os.getenv("STRING_SESSION_2", "YOUR_STRING_SESSION_2")


# ==============================
# MONGODB DATABASE CONFIG
# ==============================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "support_userbot"
)


# ==============================
# SUPPORT GROUP CONFIG
# ==============================

SUPPORT_CHAT_ID = int(
    os.getenv("SUPPORT_CHAT_ID", "-1001234567890")
)