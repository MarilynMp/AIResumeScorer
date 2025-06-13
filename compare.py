from flask import Flask, Blueprint,jsonify, request
from db_service import DBService

compare_bp = Blueprint('compare', __name__)
db = DBService()

@compare_bp.route('/api/jobfitness', methods=['GET'])
def get_job_fitness():
    job_id = request.args.get('job_id', type=int)
    resume_name = request.args.get('resume_name', type=str)

    if not job_id or not resume_name:
        return jsonify({'error': 'Missing job_id or resume_name'}), 400
    result = db.get_job_fitness_by_job_and_resume(job_id, resume_name)
    if result:
        # Parse comma-separated skills if needed
        result['MatchedSkills'] = result.get('MatchedSkills', '').split(',') if result.get('MatchedSkills') else []
        result['MissingSkills'] = result.get('MissingSkills', '').split(',') if result.get('MissingSkills') else []
        result['MatchingScore'] = float(result.get('MatchingScore', 0))  # Ensure it's float
        return jsonify(result), 200
    else:
        return jsonify({"error": "No fitness data found for the given ResumeJobMappingID"}), 404