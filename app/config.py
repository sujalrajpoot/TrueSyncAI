import os
from dotenv import load_dotenv;load_dotenv()  # Load environment variables from .env file

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ENDPOINT = os.getenv("ENDPOINT")
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
    EXCEPTION = os.getenv("EXCEPTION")
    REQUEST_LIMIT = 100  # Max requests per day
    AVAILABLE_MODELS = ["gpt-3.5-turbo","gpt-3.5-turbo-202201","gpt-4o","gpt-4o-2024-05-13","o1-preview","chatgpt-4o-latest","claude-3-5-sonnet","claude-sonnet-3.5","claude-3-5-sonnet-20240620","deepseek-r1","deepseek-llm-67b-chat","llama-3.1-405b","llama-3.1-70b","llama-3.1-8b","meta-llama/Llama-3.2-90B-Vision-Instruct","meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo","meta-llama/Meta-Llama-3.1-8B-Instruct","meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo","Meta-Llama-3.1-405B-Instruct-Turbo","Meta-Llama-3.3-70B-Instruct-Turbo","mistral","mistral-large","mistralai/Mixtral-8x22B-Instruct-v0.1","Qwen/Qwen2.5-72B-Instruc","Qwen/Qwen2.5-Coder-32B-Instruct","Qwen-QwQ-32B-Preview","gemini-pro","gemini-1.5-pro","gemini-1.5-pro-latest","gemini-1.5-flash","blackboxai","blackboxai-pro","openchat/openchat-3.6-8b","dbrx-instruct","Nous-Hermes-2-Mixtral-8x7B-DPO"]
    
    # Bright Foreground Colors
    BRIGHT_BLACK = "\033[1m\033[90m"
    BRIGHT_RED = "\033[1m\033[91m"
    BRIGHT_GREEN = "\033[1m\033[92m"
    BRIGHT_YELLOW = "\033[1m\033[93m"
    BRIGHT_BLUE = "\033[1m\033[94m"
    BRIGHT_MAGENTA = "\033[1m\033[95m"
    BRIGHT_CYAN = "\033[1m\033[96m"
    BRIGHT_WHITE = "\033[1m\033[97m"
    RESET = "\033[0m"  # Reset to default