from flask import Flask, request, jsonify
import hmac, hashlib, secrets, time, os
from openai import OpenAI

app = Flask(__name__)

# 🔑 Secret key for API authentication (Load from environment in production)
SECRET_KEY = os.getenv("SECRET_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
client = OpenAI(base_url=endpoint,api_key=GITHUB_TOKEN)

# Track API statistics
request_count = 0
start_time = time.time()

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>TrueSyncAI</title>
    </head>
    <body style="text-align: center;">
        <h1>Welcome to TrueSyncAI</h1>
        <img src="https://huggingface.co/spaces/sujalrajpoot/truesyncai/resolve/main/TrueSyncAI.jpg" alt="TrueSyncAI Logo" width="500">
    </body>
    </html>
    """

@app.route('/status', methods=['GET'])
def status():
    global request_count
    uptime_seconds = int(time.time() - start_time)

    # Convert uptime to days, hours, minutes, and seconds
    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    uptime_str = f"{days} days, {hours} hours, {minutes} minutes and {seconds} seconds"

    return jsonify({
        "status": "API is running",
        "total_requests": request_count,
        "uptime": uptime_str
    })

# Generate API Key
@app.route("/generate_api_key", methods=["POST"])
def generate_api_key():
    random_part = secrets.token_hex(16)
    signature = hmac.new(SECRET_KEY.encode(), random_part.encode(), hashlib.sha256).hexdigest()[:16]
    api_key = f"TrueSyncAI-{random_part}-{signature}"
    
    return jsonify({"api_key": api_key})

# Validate API Key
def validate_api_key(api_key):
    parts = api_key.split("-")
    if len(parts) != 3 or parts[0] != "TrueSyncAI":
        return False
    
    random_part, received_signature = parts[1], parts[2]
    expected_signature = hmac.new(SECRET_KEY.encode(), random_part.encode(), hashlib.sha256).hexdigest()[:16]
    return expected_signature == received_signature

def generate_response(query:str) -> str:
    try:
        model_name = "gpt-4o"
        response = client.chat.completions.create(
        messages=[{"role": "system","content": "You are TrueSyncAI, a pioneering AI startup founded by Sujal Rajpoot and Anuj Rajpoot. As TrueSyncAI, you are designed to be intelligent, engaging, and helpful in conversations. You should provide insightful, accurate, concise and context-aware responses while maintaining a friendly and professional tone. Your goal is to enhance the user’s experience by adapting to their needs, assisting with various tasks, and learning from interactions to improve over time. Always ensure clarity, relevance, concise and accuracy in your responses, and align with TrueSyncAI’s vision of bridging the gap between virtual intelligence and reality."},{"role": "user","content": query}],temperature=0.7,max_tokens=4096,top_p=0.9,model=model_name,stream=False)
        return response.choices[0].message.content
    except:
        return "API Server is under maintenance. Please Try After Some Time Thank You for using TrueSyncAI Chat API. Have a great day."
    
# Chat Endpoint
@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    global request_count
    data = request.json
    api_key = data.get("api_key")
    message = data.get("message", "").strip()
    
    if not api_key or not validate_api_key(api_key):
        return jsonify({"error": "Invalid API Key"}), 401
    
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # Basic AI response (Can integrate LLMs here)
    response = generate_response(message)
    request_count += 1
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)  # Hugging Face Spaces default port
