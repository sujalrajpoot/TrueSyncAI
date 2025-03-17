import json
import os
from datetime import datetime, timedelta, timezone

DB_PATH = "data/database.json"

# Ensure the data directory and JSON file exist
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump({}, f)

# ✅ Load user data from JSON file
def load_users():
    if not os.path.exists(DB_PATH):
        return {}  # Return empty dictionary if file doesn't exist
    
    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}  # Return empty dictionary if JSON is invalid

def get_user(api_key):
    """Retrieve user data from the database."""
    users = load_users()
    now = datetime.now(timezone.utc)

    if api_key not in users:
        # If API key not found, create default entry
        users[api_key] = {"count": 0, "reset_time": (now + timedelta(days=1)).isoformat()}
        save_users(users)  # Save new user data

    return users[api_key]

def update_user(api_key, field, value):
    """Update a user's field in the database."""
    users = load_users()
    now = datetime.now(timezone.utc)

    if api_key not in users:
        users[api_key] = {"count": 0, "reset_time": (now + timedelta(days=1)).isoformat()}

    user_data = users[api_key]
    
    # Reset count if the reset time has passed
    reset_time = datetime.fromisoformat(user_data["reset_time"])
    if now >= reset_time:
        user_data["count"] = 0
        user_data["reset_time"] = (now + timedelta(days=1)).isoformat()
    
    user_data["count"] += 1  # Increment API usage count
    save_users(users)

    return user_data

def reset_usage_if_needed(api_key):
    """Reset API usage if the reset time has passed."""
    user = get_user(api_key)
    if user:
        now = datetime.now(timezone.utc)
        reset_time = datetime.fromisoformat(user["reset_time"])
        if now >= reset_time:
            update_user(api_key, "count", 0)
            update_user(api_key, "reset_time", (now + timedelta(days=1)).isoformat())

# ✅ Save user data to JSON file
def save_users(users):
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)