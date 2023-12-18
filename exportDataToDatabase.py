import pandas as pd
import mysql.connector
import numpy as np
import importJsonToDataframe as jtd

# Get Dataframe from JSON
result, df = jtd.getFormatted("HEO14")
jtd.cleanData(df)

# Display the first few rows of the dataset & summary statistics
print("Dataset:")
print(df.head())
print("The Column Headers :", list(df.columns.values))

# MariaDB connection parameters
db_params = {
    "host": "localhost",
    "user": "root",
    "password": "",
}

def CreateRefTable(tablename, fieldname):
    # Connect to MariaDB server
    #conn = mysql.connector.connect(**db_params)
    #cursor = conn.cursor()

    sql = "CREATE TABLE IF NOT EXISTS "+tablename+ """(
        id INT AUTO_INCREMENT PRIMARY KEY,
        """+fieldname+""" TEXT
    )"""
    # Create a reference table in the database
    cursor.execute(sql)

# Connect to MariaDB server
conn = mysql.connector.connect(**db_params)
cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS datarepproj")
cursor.execute("USE datarepproj")

###
# Create reference tables

# Create an Institutions table and insert data into it
CreateRefTable("institutions", "Institutions")
uniqueInstitutions = df.Institutions.unique()
for i in uniqueInstitutions:
    cursor.execute("INSERT INTO institutions (Institutions) VALUES (%s)", (i,))

# Create a Field of Study table and insert data into it
CreateRefTable("fieldofstudy", "FieldOfStudy")
uniqueFieldStudy = df.FieldofStudy.unique()
for s in uniqueFieldStudy:
    cursor.execute("INSERT INTO fieldofstudy (FieldOfStudy) VALUES (%s)", (s,))

# Create an NFQ table and insert data into it
CreateRefTable("nfqlevel", "NFQLevel")
uniqueNFQ = df.NFQLevel.unique()
for nfq in uniqueNFQ:
    cursor.execute("INSERT INTO nfqlevel (NFQLevel) VALUES (%s)", (nfq,))

# Create Year of Graduation table and insert data into it
CreateRefTable("graduationyear", "GraduationYear")
uniqueYear = df.GraduationYear.unique()
for y in uniqueYear:
    cursor.execute("INSERT INTO graduationyear (GraduationYear) VALUES (%s)", (int(y),))

###
# Convert all values in data table to corresponding foreign keys to reference tables

# Function to convert all values of main data to their corresponding foreign keys
def ConvertDataToForeignKeys(uniqueList, refTable, df, fieldname):
    for val in uniqueList:
        cursor = conn.cursor(buffered=True)
        sql = "select * from "+refTable+" where "+refTable+"."+fieldname+" = %s"
        cursor.execute(sql, (val,))
        result = cursor.fetchone()
        df.loc[df[fieldname] == val, fieldname] = result[0]

ConvertDataToForeignKeys(uniqueInstitutions, "institutions", df, "Institutions")
ConvertDataToForeignKeys(uniqueFieldStudy, "fieldofstudy", df, "FieldofStudy")
ConvertDataToForeignKeys(uniqueNFQ, "nfqLevel", df, "NFQLevel")
ConvertDataToForeignKeys(uniqueYear, "graduationyear", df, "GraduationYear")

###
# Now create the Data table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Graduates (
        id INT AUTO_INCREMENT,
        `Institution` INT,
        `GraduationYear` INT,
        `FieldOfStudy` INT,
        `NFQ_Level` INT,
        `NumGraduates` INT,
        PRIMARY KEY (Institution, GraduationYear, FieldOfStudy, NFQ_Level),
        UNIQUE KEY id_inique (id)
    )
""")

# Insert data into the table
for index, row in df.iterrows():
    cursor.execute("""
        INSERT INTO Graduates
        (`Institution`, `GraduationYear`, `FieldOfStudy`, `NFQ_Level`, `NumGraduates`)
        VALUES (%s, %s, %s, %s, %s)
    """, (row['Institutions'], row['GraduationYear'], row['FieldofStudy'], row['NFQLevel'], row['NumberofGraduates']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")