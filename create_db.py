import sqlite3
import pandas as pd

# Path to your database
DB_PATH = "vaccination_data.db"

# Connect to database
conn = sqlite3.connect(DB_PATH)

# Get all table names
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)

print("Tables in the database:\n", tables)

# Show first 5 rows from each table
for table in tables['name']:
    print(f"\n🔹 Preview of table: {table}")
    df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 5;", conn)
    print(df)

# Close connection
conn.close()
