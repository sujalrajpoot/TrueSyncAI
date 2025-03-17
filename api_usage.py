import requests

# Set API Base URL
# BASE_URL = "http://127.0.0.1:5000"  # Change if hosted elsewhere
BASE_URL = "https://sujalrajpoot-truesyncai.hf.space"  # Change if hosted elsewhere

# 1️⃣ Fetch Available Models
def get_available_models() -> str:
    url = f"{BASE_URL}/v1/models"
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json().get("models")
        print(f"✅ Available Models: {models}")
        return models
    else:
        return "❌ Failed to fetch models"

# 2️⃣ Check API Usage
def usage(api_key:str) -> None:
    # 📤 Send request
    response = requests.get(f"{BASE_URL}/usage", params={"api_key": api_key})
    
    # 📥 Print response
    if response.status_code == 200:
        usage_data = response.json()
        print(f"📊 API Usage Details:\n"
              f"🔑 API Key: {usage_data['api_key']}\n"
              f"✅ Requests Used: {usage_data['requests_used']}\n"
              f"🕒 Remaining Requests: {usage_data['remaining_requests']}\n"
              f"⏳ Reset Time: {usage_data['reset_time']}")
    else:
        print(f"❌ Error: {response.json().get('error', 'Unknown error')}")

# 3️⃣ Check API Status
def check_status() -> None:
    url = f"{BASE_URL}/status"
    response = requests.get(url)
    print(f"Status          : {response.json().get('status', 'N/A')}")
    print(f"Uptime          : {response.json().get('uptime', 'N/A')}\n")
    
# 4️⃣ Chat Request (Non-Streaming Response)
def chat_request(api_key, message, model="deepseek-r1", stream=False) -> None:
    url = f"{BASE_URL}/v1/chat/completions"
    payload = {
        "api_key": api_key,
        "message": message,
        "stream": stream,
        "model": model,
        "temperature": 0.2,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "top_p": 1,
        "max_tokens": 500
    }
    
    response = requests.post(url, json=payload, stream=stream)
    
    if response.status_code == 200:
        if stream:
            print("\n✅ Streaming Response:")
            for line in response.iter_lines(decode_unicode=True):
                if line and "[DONE]" not in line:
                    print(line, end="", flush=True)  # Stream response live
        else:
            print(f"✅ Non-Streaming Response: {response.json().get('response')}")
    else:
        print(f"❌ Chat request failed: {response.json()['error']}")

# 5️⃣ Streaming Chat Request
def chat_request_stream(api_key, message, model="deepseek-r1") -> None:
    chat_request(api_key, message, model, stream=True)

# 🔥 Run All Functions
if __name__ == "__main__":
    api_key = "Enter Your API KEY Here"
    get_available_models()  # Fetch available models
    usage(api_key)  # Check API usage
    check_status()  # Check API status
    
    # Chat Requests
    chat_request(api_key, "Hello, how are you?")  # Non-Streaming
    chat_request_stream(api_key, "Tell me a joke")  # Streaming Response
