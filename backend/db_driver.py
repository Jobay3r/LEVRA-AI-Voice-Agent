"""
Database Driver Module for Career Assistant Application with HSF Support

This module provides a database abstraction layer for LEVRA's AI Learning Coach,
supporting the Human Skills Framework (HSF) and Gen Z-optimized learning features.
It uses SQLite for persistent storage of career profiles, skill tracking, learning
pathways, and performance data.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict
import sqlite3
import os
import json
from datetime import datetime

@dataclass
class CareerProfile:
    """
    Data Transfer Object (DTO) representing a user's career profile.
    
    This class serves as a clean data structure for transferring profile data
    between the database and application layers without exposing implementation details.
    
    Attributes:
        id (str): Unique identifier for the user
        dream_job (str): The user's career aspiration
        current_skills (str): Skills the user currently possesses
        education (str): The user's educational background
    """
    id: str
    dream_job: str
    current_skills: str
    education: str
    
@dataclass
class HSFSkillProfile:
    """
    DTO for a user's HSF skill profile and progression.
    
    Attributes:
        user_id (str): ID of the user this profile belongs to
        skill_name (str): Name of the HSF skill (e.g., communication_clarity)
        current_level (float): Current skill level (0-10)
        target_level (float): Target skill level (0-10)
        trend (str): Current learning trend (improving, maintaining, baseline)
        last_updated (str): Timestamp of last update
    """
    user_id: str
    skill_name: str
    current_level: float
    target_level: float
    trend: str
    last_updated: str

@dataclass
class PerformanceEntry:
    """
    DTO for tracking performance in scenarios and skill development.
    
    Attributes:
        user_id (str): ID of the user
        scenario_type (str): Type of scenario completed
        skill_scores (Dict[str, float]): Scores for each skill assessed
        overall_score (float): Average score across skills
        timestamp (str): When the performance was recorded
        user_feedback (str): Optional feedback from the user
    """
    user_id: str
    scenario_type: str
    skill_scores: Dict[str, float]
    overall_score: float
    timestamp: str
    user_feedback: Optional[str]

@dataclass
class LearningPathway:
    """
    DTO for a user's personalized learning journey.
    
    Attributes:
        user_id (str): ID of the user
        current_module (str): Current learning module/stage
        completed_scenarios (List[str]): List of completed scenario IDs
        next_recommended_skills (List[str]): Skills recommended for focus
        engagement_score (float): Gen Z engagement metric (0-10)
        last_activity (str): Timestamp of last learning activity
    """
    user_id: str
    current_module: str
    completed_scenarios: List[str]
    next_recommended_skills: List[str]
    engagement_score: float
    last_activity: str

class DatabaseDriver:
    """
    Manages database operations for LEVRA's AI Learning Coach.
    
    This class handles all interactions with the SQLite database including
    HSF skill tracking, learning pathways, and performance history.
    """
    def __init__(self):
        """
        Initialize the database driver with HSF support.
        """
        self._db_path = os.path.join(os.path.dirname(__file__), "levra_coach.db")
        self._init_db()
        
    def _init_db(self):
        """
        Initialize the database schema with HSF-related tables.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Base profile table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS career_profiles (
                    id TEXT PRIMARY KEY,
                    dream_job TEXT,
                    current_skills TEXT,
                    education TEXT
                )
            """)
            
            # HSF skill profiles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hsf_skill_profiles (
                    user_id TEXT,
                    skill_name TEXT,
                    current_level REAL,
                    target_level REAL,
                    trend TEXT,
                    last_updated TEXT,
                    PRIMARY KEY (user_id, skill_name),
                    FOREIGN KEY (user_id) REFERENCES career_profiles(id)
                )
            """)
            
            # Performance history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS performance_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    scenario_type TEXT,
                    skill_scores TEXT,  -- JSON string of skill:score mapping
                    overall_score REAL,
                    timestamp TEXT,
                    user_feedback TEXT,
                    FOREIGN KEY (user_id) REFERENCES career_profiles(id)
                )
            """)
            
            # Learning pathways
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_pathways (
                    user_id TEXT PRIMARY KEY,
                    current_module TEXT,
                    completed_scenarios TEXT,  -- JSON array of scenario IDs
                    next_recommended_skills TEXT,  -- JSON array of skill names
                    engagement_score REAL,
                    last_activity TEXT,
                    FOREIGN KEY (user_id) REFERENCES career_profiles(id)
                )
            """)
            
            conn.commit()
            
    def _get_connection(self):
        """
        Establish and return a database connection.
        
        Returns:
            sqlite3.Connection: Active connection to the SQLite database
        """
        return sqlite3.connect(self._db_path)
    
    # Career profile methods
    def create_career_profile(self, id: str, dream_job: str, current_skills: str, education: str) -> Optional[CareerProfile]:
        """Create a new career profile with default HSF skill tracking."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Create base profile
                cursor.execute(
                    "INSERT INTO career_profiles (id, dream_job, current_skills, education) VALUES (?, ?, ?, ?)",
                    (id, dream_job, current_skills, education)
                )
                
                # Initialize HSF skill profiles
                default_skills = [
                    "communication_clarity", "digital_leadership", "generational_bridge_building",
                    "purpose_driven_communication", "cultural_intelligence", "emotional_intelligence",
                    "future_ready_mindset"
                ]
                
                now = datetime.now().isoformat()
                for skill in default_skills:
                    cursor.execute(
                        "INSERT INTO hsf_skill_profiles (user_id, skill_name, current_level, target_level, trend, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
                        (id, skill, 0.0, 8.0, "baseline", now)
                    )
                
                # Initialize learning pathway
                cursor.execute(
                    "INSERT INTO learning_pathways (user_id, current_module, completed_scenarios, next_recommended_skills, engagement_score, last_activity) VALUES (?, ?, ?, ?, ?, ?)",
                    (id, "assessment", "[]", json.dumps(default_skills[:2]), 10.0, now)
                )
                
                conn.commit()
                return CareerProfile(id=id, dream_job=dream_job, current_skills=current_skills, education=education)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_profile_by_id(self, id: str) -> Optional[CareerProfile]:
        """Retrieve a career profile by ID."""
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
    
    # HSF skill tracking methods
    def update_skill_level(self, user_id: str, skill_name: str, new_level: float) -> Optional[HSFSkillProfile]:
        """Update a user's skill level and trend."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Get current skill profile
                cursor.execute(
                    "SELECT current_level FROM hsf_skill_profiles WHERE user_id = ? AND skill_name = ?",
                    (user_id, skill_name)
                )
                row = cursor.fetchone()
                if not row:
                    return None
                
                current_level = row[0]
                trend = "improving" if new_level > current_level else "maintaining"
                now = datetime.now().isoformat()
                
                # Update skill profile
                cursor.execute(
                    "UPDATE hsf_skill_profiles SET current_level = ?, trend = ?, last_updated = ? WHERE user_id = ? AND skill_name = ?",
                    (new_level, trend, now, user_id, skill_name)
                )
                
                conn.commit()
                return self.get_skill_profile(user_id, skill_name)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_skill_profile(self, user_id: str, skill_name: str) -> Optional[HSFSkillProfile]:
        """Get a user's skill profile for a specific skill."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM hsf_skill_profiles WHERE user_id = ? AND skill_name = ?",
                    (user_id, skill_name)
                )
                row = cursor.fetchone()
                if not row:
                    return None
                
                return HSFSkillProfile(
                    user_id=row[0],
                    skill_name=row[1],
                    current_level=row[2],
                    target_level=row[3],
                    trend=row[4],
                    last_updated=row[5]
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_all_skill_profiles(self, user_id: str) -> List[HSFSkillProfile]:
        """Get all skill profiles for a user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM hsf_skill_profiles WHERE user_id = ?", (user_id,))
                rows = cursor.fetchall()
                
                return [HSFSkillProfile(
                    user_id=row[0],
                    skill_name=row[1],
                    current_level=row[2],
                    target_level=row[3],
                    trend=row[4],
                    last_updated=row[5]
                ) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    # Performance tracking methods
    def record_performance(self, user_id: str, scenario_type: str, skill_scores: Dict[str, float], feedback: Optional[str] = None) -> Optional[PerformanceEntry]:
        """Record a performance entry for a completed scenario."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                now = datetime.now().isoformat()
                overall_score = sum(skill_scores.values()) / len(skill_scores) if skill_scores else 0
                
                cursor.execute(
                    "INSERT INTO performance_history (user_id, scenario_type, skill_scores, overall_score, timestamp, user_feedback) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, scenario_type, json.dumps(skill_scores), overall_score, now, feedback)
                )
                
                # Update learning pathway
                cursor.execute("SELECT completed_scenarios FROM learning_pathways WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if row:
                    completed = json.loads(row[0])
                    completed.append(scenario_type)
                    cursor.execute(
                        "UPDATE learning_pathways SET completed_scenarios = ?, last_activity = ? WHERE user_id = ?",
                        (json.dumps(completed), now, user_id)
                    )
                
                conn.commit()
                return PerformanceEntry(
                    user_id=user_id,
                    scenario_type=scenario_type,
                    skill_scores=skill_scores,
                    overall_score=overall_score,
                    timestamp=now,
                    user_feedback=feedback
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_performance_history(self, user_id: str, limit: int = 10) -> List[PerformanceEntry]:
        """Get recent performance history for a user."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM performance_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (user_id, limit)
                )
                rows = cursor.fetchall()
                
                return [PerformanceEntry(
                    user_id=row[1],
                    scenario_type=row[2],
                    skill_scores=json.loads(row[3]),
                    overall_score=row[4],
                    timestamp=row[5],
                    user_feedback=row[6]
                ) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
    
    # Learning pathway methods
    def update_learning_pathway(self, user_id: str, current_module: str, next_skills: List[str]) -> Optional[LearningPathway]:
        """Update a user's learning pathway."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute(
                    "UPDATE learning_pathways SET current_module = ?, next_recommended_skills = ?, last_activity = ? WHERE user_id = ?",
                    (current_module, json.dumps(next_skills), now, user_id)
                )
                
                conn.commit()
                return self.get_learning_pathway(user_id)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def get_learning_pathway(self, user_id: str) -> Optional[LearningPathway]:
        """Get a user's current learning pathway."""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM learning_pathways WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if not row:
                    return None
                
                return LearningPathway(
                    user_id=row[0],
                    current_module=row[1],
                    completed_scenarios=json.loads(row[2]),
                    next_recommended_skills=json.loads(row[3]),
                    engagement_score=row[4],
                    last_activity=row[5]
                )
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

# Singleton database driver instance
DB = DatabaseDriver()

"""
LEVRA's AI Learning Coach - Database Integration Guide

This module implements persistent storage for LEVRA's Human Skills Framework (HSF),
supporting Gen Z-optimized learning features and comprehensive skill tracking.

Key Features:
1. HSF Skill Profiles
   - Track current and target levels for each skill
   - Monitor skill development trends
   - Support personalized learning objectives

2. Performance History
   - Record scenario completion and skill scores
   - Track engagement metrics
   - Store user feedback and reflections

3. Learning Pathways
   - Manage personalized learning journeys
   - Track completed scenarios
   - Recommend next skills for development

4. Gen Z Optimization
   - High engagement through gamification metrics
   - Immediate feedback storage and retrieval
   - Progress visualization data

Usage Examples:
    # Create a new user profile with HSF tracking
    profile = DB.create_career_profile("user123", "Data Scientist", "Python, SQL", "BS Computer Science")
    
    # Update skill level after scenario completion
    DB.update_skill_level("user123", "communication_clarity", 7.5)
    
    # Record performance in a scenario
    DB.record_performance("user123", "gen_z_leadership_emergence", 
                         {"communication_clarity": 8.0, "leadership": 7.5})
    
    # Update learning pathway
    DB.update_learning_pathway("user123", "advanced_scenarios", 
                             ["cultural_intelligence", "digital_leadership"])
"""
