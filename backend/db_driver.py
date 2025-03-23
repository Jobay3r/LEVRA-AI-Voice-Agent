from dataclasses import dataclass
from typing import Optional, List
import sqlite3
import os

@dataclass
class CareerProfile:
    id: str  # Using id instead of vin
    dream_job: str  # Instead of make
    current_skills: str  # Instead of model
    education: str  # Instead of year
    
class DatabaseDriver:
    def __init__(self):
        self._db_path = os.path.join(os.path.dirname(__file__), "career_assistant.db")
        self._init_db()
        
    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS career_profiles (
                    id TEXT PRIMARY KEY,
                    dream_job TEXT,
                    current_skills TEXT,
                    education TEXT
                )
            """)
            conn.commit()
            
    def _get_connection(self):
        return sqlite3.connect(self._db_path)
    
    def create_career_profile(self, id: str, dream_job: str, current_skills: str, education: str) -> CareerProfile:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO career_profiles (id, dream_job, current_skills, education) VALUES (?, ?, ?, ?)",
                    (id, dream_job, current_skills, education)
                )
                conn.commit()
                return CareerProfile(id=id, dream_job=dream_job, current_skills=current_skills, education=education)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def get_profile_by_id(self, id: str) -> Optional[CareerProfile]:
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM career_profiles WHERE id = ?", (id,))
                row = cursor.fetchone()
                if not row:
                    return None
                
                return CareerProfile(
                    id=row[0],
                    dream_job=row[1],
                    current_skills=row[2],
                    education=row[3]
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

# Initialize the database driver
DB = DatabaseDriver()
