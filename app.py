from flask import Flask, request, jsonify
from telethon import TelegramClient, functions
from telethon.sessions import StringSession
import asyncio
import os
import traceback

app = Flask(__name__)

# ============================================
# CONFIGURATION
# ============================================
API_ID = int(os.environ.get('API_ID', '36879151'))
API_HASH = os.environ.get('API_HASH', '45360a236343352099ffa29570f48700'))
SESSION_STRING = os.environ.get('SESSION_STRING', '')

# Create event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Create client
try:
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH, loop=loop)
except Exception as e:
    print(f"Client Error: {e}")
    client = None

# ============================================
# ROUTES
# ============================================
@app.route('/')
def home():
    return """
    <h1 style='color:#0ff;text-align:center;padding:50px;background:#000;'>
    🆔 BRONX ULTRA API ✅<br>
    <small style='color:#888;'>/chatid?username=USERNAME</small>
    </h1>
    """

@app.route('/chatid')
def chatid():
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({"status": "error", "message": "Missing username"}), 400
    
    if not client:
        return jsonify({"status": "error", "message": "Client not initialized - Check SESSION_STRING"}), 500
    
    async def get_entity():
        try:
            await client.connect()
            clean = username.replace("@", "")
            
            # Try as username first
            try:
                entity = await client.get_entity(f"@{clean}")
            except:
                # Try as numeric ID
                try:
                    entity = await client.get_entity(int(clean))
                except:
                    entity = await client.get_entity(clean)
            
            result = {
                "status": "success",
                "chat_id": entity.id,
                "username": getattr(entity, 'username', clean),
                "first_name": getattr(entity, 'first_name', ''),
                "last_name": getattr(entity, 'last_name', ''),
                "credit": "@BRONX_ULTRA"
            }
            
            # Type detection
            if hasattr(entity, 'broadcast') and entity.broadcast:
                result["type"] = "channel"
                result["title"] = getattr(entity, 'title', '')
            elif hasattr(entity, 'title'):
                result["type"] = "group"
                result["title"] = entity.title
            else:
                result["type"] = "user"
            
            return result
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    try:
        result = loop.run_until_complete(get_entity())
        result["credit"] = "@BRONX_ULTRA"
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "credit": "@BRONX_ULTRA"
        }), 500

@app.route('/health')
def health():
    status = "healthy" if client else "error"
    return jsonify({
        "status": status,
        "client_ok": client is not None,
        "credit": "@BRONX_ULTRA"
    })

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 Starting on port {port}")
    app.run(host='0.0.0.0', port=port)
