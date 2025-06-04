from flask import Flask, request, jsonify
from scorer import score_resume
import os

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    resume_path = data.get("resume_path")
    job_description = data.get("job_description")

    if not resume_path or not job_description:
        return jsonify({"error": "Missing resume_path or job_description"}), 400

    if not os.path.exists(resume_path):
        return jsonify({"error": "Resume file not found"}), 404

    result = score_resume(resume_path, job_description)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
