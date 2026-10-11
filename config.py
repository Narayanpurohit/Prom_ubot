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

# First-contact permission messages for general, non-adult promotions.
# Be specific about the actual promotions you send and contact only appropriate recipients.
NS1 = "Hi! 👋 Would you like to receive occasional updates and promotions from us? Reply /subscribe to opt in, or /stop to decline. No promotional updates unless you subscribe."
NS2 = "Hello! I’m asking your permission first: may I send you general promotional offers and updates? Reply /subscribe if yes, or /stop if no. Your choice will be respected."
NS3 = "Hey 🙂 Interested in occasional updates about our offers and promotions? Send /subscribe to opt in. Send /stop to decline. We’ll only send further promotions if you subscribe."
NS4 = "Quick permission check: would you like to receive occasional messages about our general offers and promotions? Reply /subscribe for yes or /stop for no."
NS5 = "Hello 👋 This is a one-time request for permission to share general promotional updates and offers. Reply /subscribe if you want them, or /stop if you don’t."
NS6 = "Hi! We don’t want to send promotions without your permission. Would you like occasional updates about our offers? Reply /subscribe to opt in, or /stop to decline."
NS7 = "Permission request: may we send you general promotional messages and offers from time to time? Reply /subscribe only if you agree. Reply /stop to decline."

# Telegram numeric user IDs allowed to run owner-only commands.
OWNERS_ID = []
