from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

app = Flask(__name__)

# ============================================
# CONFIGURATION - FIXED ✅
# ============================================
API_ID = int(os.environ.get('API_ID', '36879151'))
API_HASH = os.environ.get('API_HASH', '45360a236343352099ffa29570f48700')
SESSION_STRING = os.environ.get('SESSION_STRING', '')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, loop=loop)

# ============================================
# ROUTES
# ============================================
@app.route('/')
def home():
    return "<h1 style='color:#0ff;text-align:center;padding:50px;'>🆔 BRONX ULTRA API ✅</h1>"

@app.route('/chatid')
def chatid():
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify({"error": "Missing username"}), 400
    
    async def get():
        await client.connect()
        e = await client.get_entity(username.replace("@", ""))
        return {
            "status": "success",
            "chat_id": e.id,
            "username": getattr(e, 'username', username),
            "first_name": getattr(e, 'first_name', ''),
            "credit": "@BRONX_ULTRA"
        }
    
    return jsonify(loop.run_until_complete(get()))

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
