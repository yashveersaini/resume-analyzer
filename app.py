import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from config import APP_NAME, DEBUG
from src import logger
from src.services.file_extractor import FileExtractor

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = DEBUG
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.route("/")
    def home():
        logger.info("Home route accessed")
        return jsonify({"message": "Resume Analyzer Backend Running Successfully"})

    @app.route("/upload", methods=["POST"])
    def upload_resume():
        logger.info("Upload endpoint triggered")

        if "file" not in request.files:
            logger.warning("No file part in request")
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "":
            logger.warning("Empty filename submitted")
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                logger.info(f"File saved at {file_path}")

                extracted_text = FileExtractor.extract_text_from_pdf(file_path)

                return jsonify({
                    "message": "File processed successfully",
                    "extracted_text_preview": extracted_text[:500]
                })

            except Exception as e:
                logger.error(f"Processing error: {str(e)}")
                return jsonify({"error": "File processing failed"}), 500

        logger.warning("Invalid file format")
        return jsonify({"error": "Only PDF files allowed"}), 400

    return app


app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask Application...")
    app.run(host="0.0.0.0", port=5000)
