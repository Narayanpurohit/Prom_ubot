import os
from dotenv import load_dotenv
load_dotenv()
# =====================================
# USERBOT 1 CONFIG
# =====================================

API_ID_1 = int(os.getenv("API_ID_1", "12345678"))
API_HASH_1 = os.getenv("API_HASH_1", "YOUR_API_HASH_1")
STRING_SESSION_1 = os.getenv("STRING_SESSION_1", "YOUR_SESSION_STRING_1")


# =====================================
# USERBOT 2 CONFIG
# =====================================

API_ID_2 = int(os.getenv("API_ID_2", "12345678"))
API_HASH_2 = os.getenv("API_HASH_2", "YOUR_API_HASH_2")
STRING_SESSION_2 = os.getenv("STRING_SESSION_2", "YOUR_SESSION_STRING_2")


# =====================================
# MONGODB CONFIG
# =====================================

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "support_userbot"
)


# =====================================
# TELEGRAM CHAT CONFIG
# =====================================

SUPPORT_CHAT_ID = int(
    os.getenv("SUPPORT_CHAT_ID", "-1002673539918")
)

LOG_CHAT_ID = int(
    os.getenv("LOG_CHAT_ID", "5597521952")
)


# =====================================
# DATABASE COLLECTIONS
# =====================================

COLLECTION1_NAME = os.getenv(
    "COLLECTION1_NAME",
    "collection1"
)

COLLECTION2_NAME = os.getenv(
    "COLLECTION2_NAME",
    "collection2"
)