from flask import Flask, Blueprint,jsonify, request
from db_service import DBService

resumes_bp = Blueprint('resumes', __name__)
db = DBService()

@resumes_bp.route("/api/resumes_for_job", methods=["GET"])
def get_resumes_for_job():
    job_id = request.args.get("jobId")

    if not job_id:
        return jsonify({"error": "Missing job_id"}), 400

    resumes = db.get_resume_by_job_id(job_id)
    # Convert to JSON-friendly format
    result = [
        {
            'ResumeJobMappingID': r[0],
            'ResumeName': r[1],
            'JobID': r[2]
        }
        for r in resumes
    ]
    return jsonify(result)

