from flask import Flask, Blueprint,jsonify
from db_service import DBService

jobs_bp = Blueprint('jobs', __name__)
db = DBService()

@jobs_bp.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = db.get_all_jobs()
    formatted = [{'JobID': j[0], 'JobPosition': j[1], 'JD': j[2]} for j in jobs]
    return jsonify(formatted)



