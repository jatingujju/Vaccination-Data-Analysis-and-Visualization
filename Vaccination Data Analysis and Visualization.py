import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Step 1: Load datasets from Excel files ---
coverage_df = pd.read_excel("data/coverage-data.xlsx", engine='openpyxl')
incidence_df = pd.read_excel("data/incidence-rate-data.xlsx", engine='openpyxl')
reported_cases_df = pd.read_excel("data/reported-cases-data.xlsx", engine='openpyxl')
vaccine_intro_df = pd.read_excel("data/vaccine-introduction-data.xlsx", engine='openpyxl')
vaccine_schedule_df = pd.read_excel("data/vaccine-schedule-data.xlsx", engine='openpyxl')

# --- Step 2: Data Cleaning ---
def clean_dataframe(df):
    """Cleans column names and handles missing values."""
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("-", "_")
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors='coerce').astype('Int64')
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_cols] = df[num_cols].fillna(0)
    return df

coverage_df = clean_dataframe(coverage_df)
incidence_df = clean_dataframe(incidence_df)
reported_cases_df = clean_dataframe(reported_cases_df)
vaccine_intro_df = clean_dataframe(vaccine_intro_df)
vaccine_schedule_df = clean_dataframe(vaccine_schedule_df)

# --- Step 3: Data Analysis and Visualization ---

# 1. Distribution of Vaccination Coverage
coverage_clean = coverage_df[(coverage_df['coverage'] >= 0) & (coverage_df['coverage'] <= 100)].copy()
plt.figure(figsize=(10, 6))
sns.histplot(coverage_clean['coverage'], bins=20, kde=True, color="skyblue")
plt.title("Distribution of Vaccination Coverage (%)")
plt.xlabel("Coverage %")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig('vaccination_coverage_distribution.png')
plt.show()
plt.close()

# 2. Top 10 countries by reported measles cases
measles_cases = reported_cases_df[reported_cases_df['disease'] == 'MEASLES'].copy()
top_measles = measles_cases.groupby('name')['cases'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 8))
sns.barplot(x=top_measles.values, y=top_measles.index, palette="viridis", hue=top_measles.index, legend=False)
plt.title("Top 10 Countries by Reported Measles Cases (Cumulative)")
plt.xlabel("Cases")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig('top_10_measles_cases.png')
plt.show()
plt.close()

# 3. Correlation between Measles Vaccination Coverage and Incidence Rate
measles_coverage = coverage_df[coverage_df['antigen'] == 'MCV1'].copy()
measles_incidence = incidence_df[incidence_df['disease'] == 'MEASLES'].copy()
merged_df = pd.merge(
    measles_coverage, 
    measles_incidence, 
    on=['code', 'name', 'year'], 
    suffixes=('_coverage', '_incidence')
)
merged_df.dropna(subset=['coverage', 'incidence_rate'], inplace=True)
merged_df = merged_df[(merged_df['coverage'] >= 0) & (merged_df['coverage'] <= 100)].copy()

# Convert 'year' to string for proper plotting as a categorical variable
merged_df['year_str'] = merged_df['year'].astype(str)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=merged_df, 
    x='coverage', 
    y='incidence_rate', 
    hue='year_str',
    palette='viridis'
)
plt.title("Measles Vaccination Coverage vs. Incidence Rate")
plt.xlabel("Coverage (% of population)")
plt.ylabel("Incidence Rate (per million population)")
plt.grid(True)
plt.tight_layout()
plt.savefig('coverage_vs_incidence.png')
plt.show()
plt.close()

# --- Step 4: Time Trend Analysis ---

# Global average coverage over time
global_coverage = measles_coverage.groupby("year")["coverage"].mean()

plt.figure(figsize=(10,6))
plt.plot(global_coverage.index, global_coverage.values, marker="o", color="blue")
plt.title("Global Average Measles Coverage Over Time")
plt.xlabel("Year")
plt.ylabel("Coverage (%)")
plt.grid(True)
plt.tight_layout()
plt.savefig('global_measles_coverage_trend.png')
plt.show()
plt.close()

# Global average incidence over time
global_incidence = measles_incidence.groupby("year")["incidence_rate"].mean()

plt.figure(figsize=(10,6))
plt.plot(global_incidence.index, global_incidence.values, marker="s", color="red")
plt.title("Global Average Measles Incidence Over Time")
plt.xlabel("Year")
plt.ylabel("Incidence Rate")
plt.grid(True)
plt.tight_layout()
plt.savefig('global_measles_incidence_trend.png')
plt.show()
plt.close()
