"""
Database Inspection Utility

This script provides a simple way to view all career profiles stored in the database.
It's intended as a debugging and administrative tool to verify data integrity
and monitor application state.

For production use, this functionality should be integrated into a proper
administrative interface with authentication and more robust error handling.
"""

import sqlite3

# Database configuration
# In a more robust implementation, this would be imported from a shared config
DATABASE_PATH = "career_assistant.db"

# Establish connection to the SQLite database
# Using a context manager would be better for automatic resource cleanup
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

# Query all career profile records from the database
# In a larger application, consider pagination for performance
cursor.execute("SELECT * FROM career_profiles")
rows = cursor.fetchall()

# Display header for better readability
print("\n===== CAREER PROFILES IN DATABASE =====")
print("ID | Dream Job | Skills | Education")
print("-------------------------------------")

# Print each record in a formatted way
# For a more sophisticated application, consider using tabulate or similar library
for row in rows:
    print(f"ID: {row[0]}, Dream Job: {row[1]}, Skills: {row[2]}, Education: {row[3]}")

# Display summary information
print(f"\nTotal profiles: {len(rows)}")

# Close database connection to release resources
# Using a context manager (with statement) would handle this automatically
conn.close()