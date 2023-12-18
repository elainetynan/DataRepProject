# DataRepProject
Project for Data Representation 2023

Ensure Wamp/Xampp server is running

To create the database and populate it.
---------------------------------------
Run the exportDataToDatabase.py python file. This gets the data from the CSO website and populates the database as follows:
Database: datarepproj
Main data table:  graduates
                  Primary key: Institution, GraduationYear, FieldOfStudy & NFQ_Level
                  Unique Key: id (Auto increment)

Reference tables: fieldOfStudy (graduates.FieldOfStudy <---> fieldOfStudy.id)
                  graduationYear (graduates.GraduationYear <---> graduationYear.id)
                  institutions (graduates.Institutions <---> institutions.id)
                  nfqLevel (graduates.NFQ_Level <---> nfqLevel.id)
All Reference 
tables Primary key: id (Auto increment)

The reference tables eliminate duplicate data, which should make the database more efficient.

exportDataToDatabase.py calls the importJsonToDataframe.py file. This is the python that actually imports the data from the CSO website. It also has a function to clean the data. This does the following:
Removes spaces from field names.
It removes the aggreagte rows (i.e., number of graduates for: all instutions combined; all fields of study combined; all NFQ levels combined). This is data that can be later generated through scripts or applications. The dataset is quite large also so this extra data slows down the operation of the web server.


To view and run the web page with the data.
-------------------------------------------
Run serverproject.py

Go to the ip address /gradviewer.html. E.g., http://127.0.0.1:5000/gradviewer.html

To see the json format of all the data use /grads. E.g., http://127.0.0.1:5000/grads

To use
------

Create -->
A second create button is added to the end of the page. The data can be quite long so this is for ease of use. It  mirrors the functionality of the create button at the top.

Duplicate records will not be allowed. (Key: Institution, GraduationYear, FieldOfStudy & NFQ_Level)

Cancel button added to 'create form' for user friendliness.



Update -->
Each record has it's own update button to update that record.
Cancel button added to 'update form' for user friendliness.



Delete -->
Delete is a simply function with each record having it's own delete button to delete that record.