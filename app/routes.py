from flask import Blueprint, request, jsonify, Response, render_template, stream_with_context
import time
from app.auth import validate_api_key
from app.utils import stream_response, non_stream_response, logger, calculate_uptime
from app.models import get_available_models
from app.config import Config
from app.database import *

api_blueprint = Blueprint("api", __name__)

start_time = time.time()

@api_blueprint.route("/")
def home():
    return render_template("index.html")

@api_blueprint.route("/documentation.html")
def documentation():
    return render_template("documentation.html")

@api_blueprint.route("/status", methods=["GET"])
def status():
    """Check API status"""
    uptime_str = calculate_uptime(start_time)
    logger.info(f"🕒 {Config.BRIGHT_MAGENTA}Status Check | Uptime: {uptime_str}{Config.RESET}")
    return jsonify({"status": "API is running", "uptime": uptime_str})

@api_blueprint.route("/usage", methods=["GET"])
def usage():
    """Check API key usage"""
    api_key = request.args.get("api_key")
    if not api_key or not validate_api_key(api_key):
        logger.warning(f"❌ {Config.BRIGHT_RED}Invalid API Key Attempt | API Key: {api_key}{Config.RESET}")
        return jsonify({"error": "Invalid API Key"}), 401
    
    # Load user data from local JSON file
    users = load_users()    
    # If API key is not found, return default values
    user_data = users.get(api_key, {"count": 0, "reset_time": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()})
    
    remaining_requests = max(0, Config.REQUEST_LIMIT - user_data["count"])
    reset_time = datetime.fromisoformat(user_data["reset_time"]).strftime("%Y-%m-%d %H:%M:%S UTC")

    logger.info(f"📊 {Config.BRIGHT_MAGENTA}API Usage requested | API Key: {api_key}{Config.RESET}")

    return jsonify({
        "api_key": api_key,
        "requests_used": user_data["count"],
        "remaining_requests": remaining_requests,
        "reset_time": reset_time
    })

@api_blueprint.route("/v1/models", methods=["GET"])
def available_models():
    """Return list of available AI models"""
    logger.info(f"📜 {Config.BRIGHT_MAGENTA}Model list requested{Config.RESET}")
    return jsonify(get_available_models())

@api_blueprint.route("/v1/chat/completions", methods=["POST"])
def chat():
    """Handle AI chat requests"""
    data = request.json
    api_key = data.get("api_key")
    message = data.get("message", "").strip()

    logger.info(f"🔹 {Config.BRIGHT_YELLOW}Incoming Chat Request | API Key: {api_key} | Message: {message}{Config.RESET}")

    if not api_key or not validate_api_key(api_key):
        logger.warning(f"❌ {Config.BRIGHT_RED}Invalid API Key Attempt{Config.RESET}")
        return jsonify({"error": "Invalid API Key"}), 401
    if not message:
        logger.warning(f"⚠️ {Config.BRIGHT_RED}Empty message received{Config.RESET}")
        return jsonify({"error": "Message cannot be empty"}), 400

    reset_usage_if_needed(api_key)
    user_data = get_user(api_key)

    # Enforce API request limit
    if user_data["count"] >= Config.REQUEST_LIMIT:
        return jsonify({"error": "Request limit reached."}), 429

    api_payload = {
        "messages": [{"role": "system", "content": Config.SYSTEM_PROMPT}, {"role": "user", "content": message}],
        "stream": data.get("stream", False),
        "model": data.get("model", "deepseek-r1"),
        "temperature": data.get("temperature", 0.2),
        "top_p": data.get("top_p", 1),
        "max_tokens": data.get("max_tokens", 4000)
    }
    logger.info(f"✅ {Config.BRIGHT_GREEN}Response Sent | API Key: {api_key}{Config.RESET}")

    # Increase request count
    update_user(api_key, "count", user_data["count"] + 1)

    return Response(stream_with_context(stream_response(api_payload))) if data.get("stream", False) else jsonify({"response": non_stream_response(api_payload)})
