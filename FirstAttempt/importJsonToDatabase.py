import requests
import mysql.connector
import json

# Fetch data from the JSON URL
url = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/HEO14/JSON-stat/2.0/en"
response = requests.get(url)
data = response.json()

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

# Create a table in the database
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dataset (
        dimension TEXT,
        label TEXT,
        value DOUBLE
    )
""")

# Insert data into the table
for item in data["dimension"]["STATISTIC"]["category"]["label"].items():
    cursor.execute("INSERT INTO dataset (dimension, label, value) VALUES (%s, %s, %s)", ("STATISTIC", item[0], item[1]))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully.")