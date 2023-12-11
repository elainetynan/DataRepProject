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
print(df.describe())

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

    return ""

# Connect to MariaDB server
conn = mysql.connector.connect(**db_params)
cursor = conn.cursor()

# Create a new database
cursor.execute("CREATE DATABASE IF NOT EXISTS datarepproj")
cursor.execute("USE datarepproj")

###
#Create reference tables
uniqueInstitutions = df.Institutions.unique()
uniqueFieldStudy = df.Field_of_Study.unique()
uniqueNFQ = df.NFQ_Level.unique()
uniqueYear = df.Graduation_Year.unique()

# Create an Institutions table and insert data into it
CreateRefTable("Institutions", "Institutions")
for i in uniqueInstitutions:
    cursor.execute("INSERT INTO Institutions (Institutions) VALUES (%s)", (i,))

# Create a Field of Study table and insert data into it
CreateRefTable("Field_of_Study", "Field_of_Study")
for s in uniqueFieldStudy:
    cursor.execute("INSERT INTO Field_of_Study (Field_of_Study) VALUES (%s)", (s,))

# Create an NFQ table and insert data into it
CreateRefTable("NFQ_Level", "NFQ_Level")
for nfq in uniqueNFQ:
    cursor.execute("INSERT INTO NFQ_Level (NFQ_Level) VALUES (%s)", (nfq,))

# Create Year of Graduation table and insert data into it
CreateRefTable("Graduation_Year", "Graduation_Year")
for y in uniqueYear:
    cursor.execute("INSERT INTO Graduation_Year (Graduation_Year) VALUES (%s)", (int(y),))


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

ConvertDataToForeignKeys(uniqueInstitutions, "Institutions", df, "Institutions")
ConvertDataToForeignKeys(uniqueFieldStudy, "Field_of_Study", df, "Field_of_Study")
ConvertDataToForeignKeys(uniqueNFQ, "NFQ_Level", df, "NFQ_Level")
ConvertDataToForeignKeys(uniqueYear, "Graduation_Year", df, "Graduation_Year")
#print(df)
#print("The Column Headers :", list(df.columns.values))

###
# Now create the Data table
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
    """, (row['Institutions'], row['Graduation_Year'], row['Field_of_Study'], row['NFQ_Level'], row['Number_of_Graduates']))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")