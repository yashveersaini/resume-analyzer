from flask import Flask, jsonify
from config import APP_NAME, DEBUG
from src import logger

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = DEBUG

    @app.route("/")
    def home():
        logger.info("Home route accessed")
        return jsonify({
            "message": "Resume Analyzer Backend Running Successfully"
        })

    return app

app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask Application...")
    app.run(host="0.0.0.0", port=5000)
