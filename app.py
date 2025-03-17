from app import create_app
from app.routes import logger
from app.config import Config

app = create_app()

if __name__ == "__main__":
    logger.info(f"🚀 {Config.BRIGHT_YELLOW}TrueSyncAI API is starting...{Config.RESET}")
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=7860)
    