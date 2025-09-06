import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Path to your database
DB_PATH = "vaccination_data.db"

# Connect to DB
conn = sqlite3.connect(DB_PATH)

# Query Measles reported cases for India
df = pd.read_sql_query("""
    SELECT NAME, YEAR, DISEASE, CASES
    FROM reported_cases
    WHERE NAME='India' AND DISEASE='MEASLES' AND YEAR >= 2015
    ORDER BY YEAR;
""", conn)

conn.close()

print("📊 Data Preview:")
print(df)

# Drop missing values
df_clean = df.dropna(subset=['CASES'])

# Plot
plt.figure(figsize=(8,5))
plt.plot(df_clean['YEAR'], df_clean['CASES'], marker='o', color='red', linewidth=2)

plt.title("India Measles Reported Cases (2015–2023)")
plt.xlabel("Year")
plt.ylabel("Number of Cases")
plt.grid(True)

# Save chart
plt.savefig("india_measles_cases.png", dpi=300, bbox_inches="tight")

plt.show()
