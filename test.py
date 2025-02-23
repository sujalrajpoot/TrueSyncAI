import requests

BASE_URL = "https://sujalrajpoot-truesyncai.hf.space"

def generate_api_key():
    response = requests.post(f"{BASE_URL}/generate_api_key")
    if response.status_code == 200:
        return response.json().get("api_key")
    else:return "Error generating API key:", response.json()

def chat_with_ai(api_key, message):
    data = {"api_key": api_key, "message": message}
    response = requests.post(f"{BASE_URL}/v1/chat/completions", json=data)
    if response.status_code == 200:
        return response.json()["response"]
    else:return "Error in chat response:", response.json()["error"]

def get_api_status():
    try:
        api_url = f"{BASE_URL}/status"
        response = requests.get(api_url, timeout=5)  # Set a timeout for the request
        response_time = response.elapsed.total_seconds()  # Get response time
        
        # Check if the API returns JSON data
        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            data = response.text  # If not JSON, return raw text

        return {
            "status_code": response.status_code,
            "response_time": response_time,
            "data": data
        } 
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

if __name__ == "__main__":
    api_key = "TrueSyncAI-888d3e23fa5801834aa385118e05bd72-394215579bc4e6ac"
    message = input("Enter your message: ")
    response = chat_with_ai(api_key, message)
    if response:
        print("TrueSyncAI Response:", response)
    status_info = get_api_status()
    print(f"API Status Code  : {status_info['status_code']}")
    print(f"Response Time    : {status_info['response_time']:.2f} seconds")
    print(f"Status          : {status_info['data'].get('status', 'N/A')}")
    print(f"Total Requests  : {status_info['data'].get('total_requests', 'N/A')}")
    print(f"Uptime          : {status_info['data'].get('uptime', 'N/A')}")
  
