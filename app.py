from flask import Flask, request, jsonify, render_template_string
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio
import os

# ============================================
# BRONX ULTRA API - FRESH CODE
# ============================================
app = Flask(__name__)

# Environment Variables
API_ID = int(os.environ.get('API_ID', '31968824'))
API_HASH = os.environ.get('API_HASH', 'd9847a6694b961248f4052d16b89b912')
SESSION_STRING = os.environ.get('SESSION_STRING', '')

# Telegram Client
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ============================================
# DASHBOARD
# ============================================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>BRONX ULTRA API</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #00d4ff; 
            font-family: 'Courier New', monospace; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            min-height: 100vh; 
            padding: 20px;
        }
        .card { 
            border: 2px solid #00d4ff; 
            padding: 40px; 
            border-radius: 20px; 
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.3); 
            text-align: center; 
            max-width: 600px;
            background: rgba(10, 10, 10, 0.9);
        }
        h1 { 
            font-size: 28px; 
            margin-bottom: 10px; 
            color: #00d4ff;
            text-shadow: 0 0 10px #00d4ff55;
        }
        .badge { 
            background: #00d4ff; 
            color: #000; 
            padding: 5px 20px; 
            border-radius: 30px; 
            font-weight: bold; 
            display: inline-block;
            margin: 15px 0;
        }
        .endpoint { 
            background: #111; 
            padding: 15px; 
            border-radius: 10px; 
            margin: 20px 0;
            border: 1px solid #333;
        }
        code { 
            background: #000; 
            padding: 8px 12px; 
            border-radius: 5px; 
            color: #ffaa00; 
            font-size: 14px;
        }
        .footer { 
            margin-top: 20px; 
            color: #555; 
            font-size: 12px;
        }
        a {
            color: #00d4ff;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🆔 BRONX ULTRA API</h1>
        <span class="badge">⚡ ONLINE & RUNNING</span>
        <p style="color:#ccc; margin:15px 0;">Telegram Username → Chat ID</p>
        
        <div class="endpoint">
            <p style="color:#00d4ff; margin-bottom:10px;">📌 ENDPOINT</p>
            <code>GET /chatid?username=USERNAME</code>
        </div>
        
        <p style="color:#888; font-size:13px;">
            Example: <code style="background:#1a1a1a;">/chatid?username=BRONX_ULTRA</code>
        </p>
        
        <div class="footer">
            🔒 @BRONX_ULTRA | v1.0.0
        </div>
    </div>
</body>
</html>
"""

# ============================================
# ROUTES
# ============================================
@app.route('/')
def home():
    return render_template_string(HTML)

@app.route('/chatid')
def chatid():
    username = request.args.get('username', '').strip()
    
    if not username:
        return jsonify({
            "status": "error",
            "message": "Missing 'username' parameter",
            "credit": "@BRONX_ULTRA"
        }), 400
    
    async def get_entity():
        try:
            await client.connect()
            clean = username.replace("@", "")
            entity = await client.get_entity(f"@{clean}")
            
            result = {
                "status": "success",
                "chat_id": entity.id,
                "username": getattr(entity, 'username', clean),
            }
            
            # Type detection
            if hasattr(entity, 'broadcast') and entity.broadcast:
                result["type"] = "channel"
                result["title"] = getattr(entity, 'title', '')
            elif hasattr(entity, 'megagroup') and entity.megagroup:
                result["type"] = "supergroup"
                result["title"] = getattr(entity, 'title', '')
            elif hasattr(entity, 'title'):
                result["type"] = "group"
                result["title"] = entity.title
            elif hasattr(entity, 'bot') and entity.bot:
                result["type"] = "bot"
                result["first_name"] = getattr(entity, 'first_name', '')
            else:
                result["type"] = "user"
                result["first_name"] = getattr(entity, 'first_name', '')
                result["last_name"] = getattr(entity, 'last_name', '')
            
            # Additional info
            result["is_verified"] = getattr(entity, 'verified', False)
            result["phone"] = getattr(entity, 'phone', None)
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    # Run async function
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_entity())
        loop.close()
    except Exception as e:
        result = {"status": "error", "message": str(e)}
    
    # Add branding
    result["credit"] = "@BRONX_ULTRA"
    result["developer"] = "@BRONX_ULTRA"
    
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "credit": "@BRONX_ULTRA",
        "timestamp": "2026-04-21"
    })

# ============================================
# ERROR HANDLERS
# ============================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "error",
        "message": "Endpoint not found",
        "credit": "@BRONX_ULTRA"
    }), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({
        "status": "error",
        "message": "Internal server error",
        "credit": "@BRONX_ULTRA"
    }), 500

# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
