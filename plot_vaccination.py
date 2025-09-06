import sqlite3, pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect("vaccination_data.db")

# Load vaccination coverage data for India
df = pd.read_sql_query("""
    SELECT NAME, YEAR, ANTIGEN, COVERAGE
    FROM coverage
    WHERE NAME='India' AND YEAR >= 2015
    ORDER BY YEAR;
""", conn)

conn.close()

# Drop rows with missing coverage values
df_clean = df.dropna(subset=['COVERAGE'])

# Select important vaccines
important_vaccines = ['BCG', 'POL3', 'DTP3', 'MCV1', 'HEPB3']

plt.figure(figsize=(10,6))

for vaccine in important_vaccines:
    subset = df_clean[df_clean['ANTIGEN'] == vaccine]
    plt.plot(subset['YEAR'], subset['COVERAGE'], marker='o', label=vaccine)

plt.title("India Vaccination Coverage Trends (2015–2023)")
plt.xlabel("Year")
plt.ylabel("Coverage (%)")
plt.legend()
plt.grid(True)

# Save chart as PNG
plt.savefig("india_vaccination_trends.png", dpi=300, bbox_inches="tight")

# Show chart
plt.show()
