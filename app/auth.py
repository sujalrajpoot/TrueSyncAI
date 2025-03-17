import hmac, hashlib
from app.config import Config
def validate_api_key(api_key):
    """Validate API Key format and signature"""
    parts = api_key.split("-")
    if len(parts) != 3 or parts[0] != "TrueSyncAI":
        return False

    random_part, received_signature = parts[1], parts[2]
    expected_signature = hmac.new(
        Config.SECRET_KEY.encode(), random_part.encode(), hashlib.sha256
    ).hexdigest()[:16]
    
    return expected_signature == received_signature
