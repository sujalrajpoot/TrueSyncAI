from app.config import Config

def get_available_models():
    """Return list of supported AI models"""
    return {"models": ", ".join(Config.AVAILABLE_MODELS)}
