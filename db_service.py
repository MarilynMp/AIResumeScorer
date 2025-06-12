import sqlite3
import os
from typing import List, Dict

DB_FILE = "job_matcher.db"

class DBService:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS Jobs (
                    JobID INTEGER PRIMARY KEY AUTOINCREMENT,
                    JobPosition TEXT,
                    JD TEXT
                );

                CREATE TABLE IF NOT EXISTS ResumeJobMapping (
                    ResumeJobMappingID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ResumeName TEXT,
                    JobID INTEGER,
                    FOREIGN KEY(JobID) REFERENCES Jobs(JobID)
                );

                CREATE TABLE IF NOT EXISTS JobFitnessResult (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,     
                    ResumeName TEXT,
                    JobID INTEGER,
                    MatchScore INTEGER,
                    MatchSkills TEXT,
                    MissingSkills TEXT,
                    FOREIGN KEY(JobID) REFERENCES Jobs(JobID)
                );
            """)
            conn.commit()

    def insert_fitness_result(self, resume_name: str, job_id : int,  score_data: Dict):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO JobFitnessResult (ResumeName, JobID, MatchScore, MatchSkills, MissingSkills)
                VALUES (?, ?, ?, ?,?)
            """, (
                resume_name,
                job_id,
                score_data['score'],
                ', '.join(score_data['matching_skills']),
                ', '.join(score_data['missing_skills'])
            ))
            conn.commit()

    def get_all_fitness_results(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM JobFitnessResult")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        
    def get_all_jobs(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT JobID, JobPosition, JD FROM Jobs")
            rows = cursor.fetchall()
            return rows
        
    def get_resume_by_job_id(self,job_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ResumeJobMappingID, ResumeName, JobID FROM ResumeJobMapping WHERE JobID = ?",
        (job_id,)
    )
        resumes = cursor.fetchall()
        conn.close()
        return resumes
    

    def get_top_fitness_results(self, jobID: int, limit: int = 3) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT jfr.ID, jfr.ResumeName, jfr.MatchScore, jfr.MatchSkills, jfr.MissingSkills, jfr.JobID
                    FROM JobFitnessResult jfr
                    WHERE jfr.JobID = ?
                    ORDER BY jfr.MatchScore DESC
                    LIMIT ?
                """, (jobID, limit))

                rows = cursor.fetchall()

                if not rows:
                    return []  # No results found

                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
        except Exception as e:
            print(f"Error: {e}")
            return []