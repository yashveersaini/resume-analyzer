import os
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from config import APP_NAME, DEBUG
from src import logger
from src.services.file_extractor import FileExtractor
from src.core.matcher import ResumeMatcher
from src.core.skill_gap import SkillGapAnalyzer
from src.core.grammar_checker import GrammarChecker
from src.core.info_extractor import ResumeInfoExtractor
from flask import render_template



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
        return render_template("index.html")


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
    

    @app.route("/match", methods=["POST"])
    def match_resume():
        try:
            data = request.json

            if not data or "resume_text" not in data or "job_description" not in data:
                return jsonify({"error": "resume_text and job_description required"}), 400

            resume_text = data["resume_text"]
            job_description = data["job_description"]

            result = ResumeMatcher.calculate_ats_score(
                resume_text,
                job_description
            )

            return jsonify(result)

        except Exception as e:
            logger.error(f"Match API failed: {str(e)}")
            return jsonify({"error": "Matching failed"}), 500


    @app.route("/skill-gap", methods=["POST"])
    def skill_gap():

        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        resume_text = data.get("resume_text")
        job_description = data.get("job_description")

        if not resume_text or not job_description:
            return jsonify({"error": "Missing required fields"}), 400

        result = SkillGapAnalyzer.analyze(resume_text, job_description)

        return jsonify(result)



    @app.route("/grammar-check", methods=["POST"])
    def grammar_check():

        data = request.json

        if not data or "text" not in data:
            return jsonify({"error": "text field required"}), 400

        text = data["text"]

        corrected = GrammarChecker.correct_text(text)

        return jsonify({
            "original_text": text,
            "corrected_text": corrected
        })


    @app.route("/extract-info", methods=["POST"])
    def extract_info():

        data = request.json

        if not data or "resume_text" not in data:
            return jsonify({"error": "resume_text required"}), 400

        resume_text = data["resume_text"]

        result = ResumeInfoExtractor.extract_all(resume_text)

        return jsonify(result)


    return app


app = create_app()

if __name__ == "__main__":
    logger.info("Starting Flask Application...")
    app.run(host="0.0.0.0", port=5000)
