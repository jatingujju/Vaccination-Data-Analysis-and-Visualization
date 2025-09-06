import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

coverage_df = pd.read_excel("coverage-data.xlsx", engine="openpyxl")
incidence_df = pd.read_excel("incidence-rate-data.xlsx", engine="openpyxl")
reported_cases_df = pd.read_excel("reported-cases-data.xlsx", engine="openpyxl")
vaccine_intro_df = pd.read_excel("vaccine-introduction-data.xlsx", engine="openpyxl")
vaccine_schedule_df = pd.read_excel("vaccine-schedule-data.xlsx", engine="openpyxl")
