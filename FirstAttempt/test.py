import pandas as pd
import mysql.connector
import numpy as np

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'data.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv("data.csv")

# Replace spaces in column names with underscores as it causes problems.
df.columns = [c.replace(' ', '_') for c in df.columns]

# Remove duplicate (aggregate) rows and records that have no graduates
df.drop(df[df['Institutions'] == "All Institutions"].index, inplace = True)
df.drop(df[df['Field_of_Study'] == "All fields of education"].index, inplace = True)
df.drop(df[df['NFQ_Level'] == "All NFQ Levels"].index, inplace = True)
df.drop(df[df['VALUE'] == 0].index, inplace = True)

# Display the first few rows of the dataset & summary statistics
print("Dataset:")
print(df.head())