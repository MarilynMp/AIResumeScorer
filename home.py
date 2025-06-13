from flask import Flask, request, jsonify
from scorer import score_resume
from db_service import DBService
import os
from flask_cors import CORS
from jobs import jobs_bp
from resumes import resumes_bp
from leaderboard import leaderboard_bp
from compare import compare_bp

app = Flask(__name__)
app.register_blueprint(jobs_bp)
app.register_blueprint(resumes_bp)
app.register_blueprint(leaderboard_bp)
app.register_blueprint(compare_bp)
db = DBService()
CORS(app)

@app.route("/api/score", methods=["POST"])
def score():
    data = request.json
    resumeName = data.get("resumeName")
    resume_path = f'./resumes/{resumeName}'
    job_description = data.get("JD")
    job_id = data.get("jobId")

    if not resume_path or not job_description:
        return jsonify({"error": "Missing resume_path or job_description"}), 400

    
    if not os.path.exists(resume_path):
        return jsonify({"error": "Resume file not found"}), 404

    #Find resume score 
    result = score_resume(resume_path, job_description)

    #Insert into job fitness score table
    db.insert_fitness_result(os.path.basename(resume_path), job_id, result)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
