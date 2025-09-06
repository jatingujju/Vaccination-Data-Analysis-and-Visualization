import sqlite3, pandas as pd

conn = sqlite3.connect("vaccination_data.db")

df = pd.read_sql_query("""
    SELECT NAME, YEAR, ANTIGEN, COVERAGE
    FROM coverage
    WHERE NAME='India' AND YEAR >= 2015
    ORDER BY YEAR;
""", conn)

print(df)

conn.close()
