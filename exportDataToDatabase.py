import pandas as pd
import mysql.connector
import numpy as np
import importJsonToDataframe as jtd
import dbconfig as cfg

class exportDataToDatabase:
    def CreateRefTable(self, tablename, fieldname, cursor):
        # Connect to MariaDB server
        #conn = mysql.connector.connect(**db_params)
        #cursor = conn.cursor()

        sql = "CREATE TABLE IF NOT EXISTS "+tablename+ """(
            id INT AUTO_INCREMENT PRIMARY KEY,
            """+fieldname+""" TEXT
        )"""
        # Create a reference table in the database
        cursor.execute(sql)

    # Function to convert all values of main data to their corresponding foreign keys
    def ConvertDataToForeignKeys(self, uniqueList, refTable, df, fieldname, conn):
        for val in uniqueList:
            cursor = conn.cursor(buffered=True)
            sql = "select * from "+refTable+" where "+refTable+"."+fieldname+" = %s"
            cursor.execute(sql, (val,))
            result = cursor.fetchone()
            df.loc[df[fieldname] == val, fieldname] = result[0]

    def ExportDataToDB(self):
        # Get Dataframe from JSON
        result, df = jtd.getFormatted("HEO14")
        jtd.cleanData(df)

        # Display the first few rows of the dataset & summary statistics
        print("Dataset:")
        print(df.head())
        print("The Column Headers :", list(df.columns.values))

        # MariaDB connection parameters
        db_params = {
            "host": cfg.mysql['host'],
            "user": cfg.mysql['user'],
            "password": cfg.mysql['password'],
        }

        # Connect to MariaDB server
        conn = mysql.connector.connect(**db_params)
        cursor = conn.cursor()

        # Create a new database
        cursor.execute("CREATE DATABASE IF NOT EXISTS datarepproj")
        cursor.execute("USE "+cfg.mysql['database'])

        ###
        # Create reference tables

        # Create an Institutions table and insert data into it
        self.CreateRefTable("institutions", "Institutions", cursor)
        uniqueInstitutions = df.Institutions.unique()
        for i in uniqueInstitutions:
            cursor.execute("INSERT INTO institutions (Institutions) VALUES (%s)", (i,))

        # Create a Field of Study table and insert data into it
        self.CreateRefTable("fieldofstudy", "FieldOfStudy", cursor)
        uniqueFieldStudy = df.FieldOfStudy.unique()
        for s in uniqueFieldStudy:
            cursor.execute("INSERT INTO fieldofstudy (FieldOfStudy) VALUES (%s)", (s,))

        # Create an NFQ table and insert data into it
        self.CreateRefTable("nfqlevel", "NFQLevel", cursor)
        uniqueNFQ = df.NFQLevel.unique()
        for nfq in uniqueNFQ:
            cursor.execute("INSERT INTO nfqlevel (NFQLevel) VALUES (%s)", (nfq,))

        # Create Year of Graduation table and insert data into it
        self.CreateRefTable("graduationyear", "GraduationYear", cursor)
        uniqueYear = df.GraduationYear.unique()
        for y in uniqueYear:
            cursor.execute("INSERT INTO graduationyear (GraduationYear) VALUES (%s)", (int(y),))

        ###
        # Convert all values in data table to corresponding foreign keys to reference tables

        self.ConvertDataToForeignKeys(uniqueInstitutions, "institutions", df, "Institutions", conn)
        self.ConvertDataToForeignKeys(uniqueFieldStudy, "fieldofstudy", df, "FieldOfStudy", conn)
        self.ConvertDataToForeignKeys(uniqueNFQ, "nfqlevel", df, "NFQLevel", conn)
        self.ConvertDataToForeignKeys(uniqueYear, "graduationyear", df, "GraduationYear", conn)

        ###
        # Now create the Data table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS graduates (
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
                INSERT INTO graduates
                (`Institution`, `GraduationYear`, `FieldOfStudy`, `NFQ_Level`, `NumGraduates`)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['Institutions'], row['GraduationYear'], row['FieldOfStudy'], row['NFQLevel'], row['NumberofGraduates']))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database and table created successfully.")
        return True

if __name__ == "__main__":
    exportData = exportDataToDatabase()
    exportData.ExportDataToDB()