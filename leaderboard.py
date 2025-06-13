from flask import Flask, Blueprint,jsonify, request
from db_service import DBService

leaderboard_bp = Blueprint('leaderboard', __name__)
db = DBService()

@leaderboard_bp.route('/api/jobTopFitnessResults', methods=['GET'])
def jobTopFitnessResults():
    try:
        # Get jobID from the query parameters
        jobID = request.args.get("jobID")
        
        if not jobID:
            return jsonify({"message": "jobID is required"}), 400
        
        jobID = int(jobID)  # Convert jobID to integer
        
        limit = request.args.get("limit", default=3, type=int)
        
        # Get the top results from the database using DBService
        top_results = db.get_top_fitness_results(jobID=jobID, limit=limit)
        
        # If no results found, return a 404
        if not top_results:
            return jsonify({"message": "No results found"}), 404
        
        # Return the results as a JSON response
        return jsonify(top_results)
    
    except Exception as e:
        return jsonify({"message": f"Error retrieving results: {str(e)}"}), 500