import sqlite3

# Connect to the database
conn = sqlite3.connect("career_assistant.db")
cursor = conn.cursor()

# Query all records
cursor.execute("SELECT * FROM career_profiles")
rows = cursor.fetchall()

# Print records
for row in rows:
    print(f"ID: {row[0]}, Dream Job: {row[1]}, Skills: {row[2]}, Education: {row[3]}")

conn.close()