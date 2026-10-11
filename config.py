"""Configuration for Prom_ubot.

Fill these placeholders locally. Do not commit real API hashes, session strings,
MongoDB credentials, or other secrets to a public repository.
"""
API_ID = 0
API_HASH = ""

STRING1 = ""
STRING2 = ""
STRING3 = ""
STRING4 = ""

# Telegram chat ID or @username, e.g. -1001234567890 or "@your_group"
X_CHAT = ""

MONGO_URI = ""
DB_NAME = "prom_ubot"

# First-contact permission messages. Replace [purpose] with a clear description.
# Send only where contact is appropriate; honor /stop immediately.
NS1 = "Hi! 👋 May I send you occasional messages about [purpose]? Reply /subscribe to opt in, or /stop to decline. No updates will be sent unless you subscribe."
NS2 = "Hello! Before sending anything further, I’d like your permission to share messages about [purpose]. Reply /subscribe if you agree, or /stop if you don’t. Your choice will be respected."
NS3 = "Hey there 🙂 I’m asking first: would you like to receive messages about [purpose]? Send /subscribe to give permission, or /stop to decline. I won’t send updates without your opt-in."
NS4 = "Quick permission check: may I message you about [purpose] from time to time? Reply /subscribe to say yes, or /stop to say no. Thanks for choosing."
NS5 = "Hello 👋 You’re receiving this one-time permission request about [purpose]. If you’d like future messages, reply /subscribe. If not, reply /stop; I’ll respect that."
NS6 = "Hi! I don’t want to message you without consent. Would you like occasional updates about [purpose]? Reply /subscribe to opt in or /stop to decline."
NS7 = "Permission request: would you like to receive messages related to [purpose]? Reply /subscribe only if you agree. Reply /stop to decline; no further updates will be sent without your permission."

# Telegram numeric user IDs allowed to run owner-only commands.
OWNERS_ID = []
