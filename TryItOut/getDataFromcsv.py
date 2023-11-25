import pandas as pd
import mysql.connector
import numpy as np

# Replace 'your_file.csv' with the path to your CSV file
csv_file_path = 'data.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path)

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
print(df.describe())

uniqueInstitutions = df.Institutions.unique()
uniqueFieldStudy = df.Field_of_Study.unique()
uniqueNFQ = df.NFQ_Level.unique()
uniqueYear = df.Graduation_Year.unique()

# MariaDB connection parameters
db_params = {
    "host": "localhost",
    "user": "root",
    "password": "",
}

# Connect to MariaDB server
conn = mysql.connector.connect(**db_params)
cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS datarepproj")
cursor.execute("USE datarepproj")


# Institutions
# Create a Institution table in the database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Institutions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        `Institutions` TEXT
    )
""")

# Insert data into the table
for i in uniqueInstitutions:
    cursor.execute("INSERT INTO Institutions (Institutions) VALUES (%s)", (i,))

# Field of Study
# Create a Field of Study table in the database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fieldstudy (
        id INT AUTO_INCREMENT PRIMARY KEY,
        `FieldOfStudy` TEXT
    )
""")

# Insert data into the table
for s in uniqueFieldStudy:
    cursor.execute("INSERT INTO Fieldstudy (FieldOfStudy) VALUES (%s)", (s,))

# NFQ Level
# Create a NFQ table in the database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS NFQ_level (
        id INT AUTO_INCREMENT PRIMARY KEY,
        `NFQ_Level` TEXT
    )
""")

# Insert data into the table
for nfq in uniqueNFQ:
    cursor.execute("INSERT INTO NFQ_level (NFQ_Level) VALUES (%s)", (nfq,))

# Year of Graduation
# Create a Institution table in the database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS YearGraduation (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Graduation_Year INT
    )
""")

# Insert data into the table
for y in uniqueYear:
    cursor.execute("INSERT INTO YearGraduation (Graduation_Year) VALUES (%s)", (int(y),))

# Data Table
# Create a table in the database

# First convert all the values to their corresponding foreign keys
for val in uniqueInstitutions:
    cursor = conn.cursor(buffered=True)
    cursor.execute("select * from Institutions where Institutions.Institutions = %s", (val,))
    result = cursor.fetchone()
    df.loc[df["Institutions"] == val, "Institutions"] = result[0]



print(df)


# Now create the table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Graduates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        `Institution` TEXT,
        `GraduationYear` INT,
        `FieldOfStudy` TEXT,
        `NFQ_Level` TEXT,
        `NumGraduates` INT
    )
""")

# Insert data into the table
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Graduates
        (`Institution`, `GraduationYear`, `FieldOfStudy`, `NFQ_Level`, `NumGraduates`)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['Institutions'], row['Graduation_Year'], row['Field_of_Study'], row['NFQ_Level'], row['VALUE']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")