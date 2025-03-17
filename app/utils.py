import logging, requests, json, time
from app.config import Config

# Logging Configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def stream_response(api_payload):
    """Stream AI response"""
    try:
        response = requests.post(Config.ENDPOINT, json=api_payload, stream=True)
        if response.status_code == 200:
            for value in response.iter_lines(decode_unicode=True):
                if value and "[DONE]" not in value:
                    try:
                        data = json.loads(value[6:])
                        yield data['choices'][0]['delta']['content']
                    except:
                        continue
        else:
            yield f"Error {response.status_code}: {response.content}"
    except:
        yield Config.EXCEPTION

def non_stream_response(api_payload):
    """Return AI response without streaming"""
    try:
        response = requests.post(Config.ENDPOINT, json=api_payload)
        return response.json()["choices"][0]["message"]["content"] if response.ok else f"Error {response.status_code}"
    except:
        return Config.EXCEPTION

def calculate_uptime(start_time):
    """Calculate API uptime"""
    uptime_seconds = int(time.time() - start_time)
    days, rem = divmod(uptime_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"
