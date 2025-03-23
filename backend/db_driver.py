"""
Database Driver Module for Career Assistant Application

This module provides a database abstraction layer that isolates the application from 
the underlying database implementation. Using SQLite for persistent storage of career profiles,
it encapsulates all database operations and provides a clean API for the rest of the application.

The module follows the Data Access Object (DAO) pattern to separate data persistence logic
from business logic.
"""

from dataclasses import dataclass
from typing import Optional
import sqlite3
import os

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
    
class DatabaseDriver:
    """
    Manages database operations for career profiles.
    
    This class handles all interactions with the SQLite database including
    connection management, schema initialization, and CRUD operations
    for career profiles.
    """
    def __init__(self):
        """
        Initialize the database driver.
        
        Creates a database connection to a SQLite file in the same directory
        and ensures required tables exist.
        """
        self._db_path = os.path.join(os.path.dirname(__file__), "career_assistant.db")
        self._init_db()
        
    def _init_db(self):
        """
        Initialize the database schema if it doesn't exist.
        
        Creates the career_profiles table with appropriate columns
        for storing user career data.
        """
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
        """
        Establish and return a database connection.
        
        Returns:
            sqlite3.Connection: Active connection to the SQLite database
        """
        return sqlite3.connect(self._db_path)
    
    def create_career_profile(self, id: str, dream_job: str, current_skills: str, education: str) -> Optional[CareerProfile]:
        """
        Create a new career profile record in the database.
        
        Args:
            id (str): Unique identifier for the user
            dream_job (str): The user's career aspiration
            current_skills (str): Skills the user currently possesses
            education (str): The user's educational background
            
        Returns:
            CareerProfile: Created profile object if successful, None otherwise
            
        Raises:
            No exceptions are raised; errors are logged and None is returned on failure
        """
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
        """
        Retrieve a career profile by its unique identifier.
        
        Args:
            id (str): Unique identifier of the profile to retrieve
            
        Returns:
            CareerProfile: The found profile or None if not found
            
        Raises:
            No exceptions are raised; errors are logged and None is returned on failure
        """
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

# Singleton database driver instance for application-wide use
# This provides a single point of access to database operations
DB = DatabaseDriver()
