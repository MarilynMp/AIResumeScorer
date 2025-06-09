from flask import Flask, request, jsonify
from scorer import score_resume
from db_service import DBService
import os

app = Flask(__name__)
db = DBService()

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    resume_path = data.get("resume_path")
    job_description = data.get("job_description")

    if not resume_path or not job_description:
        return jsonify({"error": "Missing resume_path or job_description"}), 400

    if not os.path.exists(resume_path):
        return jsonify({"error": "Resume file not found"}), 404

    #Find resume score 
    result = score_resume(resume_path, job_description)

    #Insert into job fitness score table
    db.insert_fitness_result(os.path.basename(resume_path), result)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
