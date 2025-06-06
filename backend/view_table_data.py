"""
Database Inspection Utility

This script provides a way to view all LEVRA's database tables including HSF-related data.
It's intended as a debugging and administrative tool to verify data integrity
and monitor application state.

For production use, this functionality should be integrated into a proper
administrative interface with authentication and more robust error handling.
"""

import sqlite3
import json
from datetime import datetime
import os

# Database configuration
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "levra_coach.db")

def print_table_data(cursor, table_name):
    """Print formatted data for a specific table."""
    try:
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Get all records
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Print table header
        print(f"\n===== {table_name.upper()} =====")
        print(" | ".join(columns))
        print("-" * (len(" | ".join(columns)) + 10))
        
        # Print records with proper JSON formatting for complex fields
        for row in rows:
            formatted_row = []
            for i, value in enumerate(row):
                if value and isinstance(value, str) and (value.startswith('[') or value.startswith('{')):
                    try:
                        # Format JSON fields for readability
                        parsed = json.loads(value)
                        value = json.dumps(parsed, indent=2)                    except json.JSONDecodeError:
                        # If not valid JSON, use the raw string
                        pass
                formatted_row.append(str(value))
            print(" | ".join(formatted_row))
            
        print(f"\nTotal records: {len(rows)}")
        print("=" * 50)
        
    except sqlite3.Error as e:
        print(f"Error accessing table {table_name}: {e}")

def main():
    """View all tables in the LEVRA database."""
    try:
        # Establish connection with context manager
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if not tables:
                print("No tables found in database")
                return
                
            # Print data for each table
            for (table_name,) in tables:
                print_table_data(cursor, table_name)
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()