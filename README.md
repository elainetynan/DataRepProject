# DataRepProject
Project for Data Representation 2023

The web application can be run online (hosted by pythonanywhere) here: https://tynane.pythonanywhere.com/gradviewer.html


dbconfig.py file includes:

mysql = {
    'host':"localhost",
    'user':"root",
    'password':"",
    'database':"datarepproj"
}

To create the database and populate it.
---------------------------------------

Ensure Wamp/Xampp server is running

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

Note:

The CSO data does not have duplicates so I am not checkingfor this here. If you run the exportDataToDatabase file twice it will crash due to duplicate records. If running it a second time drop all tables in the database first (or delete the database).


To view and run the web page with the data.
-------------------------------------------
Run serverproject.py

Go to the ip address /gradviewer.html. E.g., http://127.0.0.1:5000/gradviewer.html

To see the json format of all the data use /grads. E.g., http://127.0.0.1:5000/grads

To use
------

Create -->

A second create button is added to the end of the page. The data can be quite long so this is for ease of use. It  mirrors the functionality of the create button at the top.

When a record is created all reference tables are checked for the values, if they do not exist in the refernce tables they are added and the new id is returned. If they do exist then the existing id of the value is returned. These ids are then used to create a new record in the 'main' table, along with the number of graduates entered into the web page.

Duplicate records will not be allowed. (Key: Institution, GraduationYear, FieldOfStudy & NFQ_Level)

Cancel button added to 'create form' for user friendliness.



Update -->

Each record has it's own update button to update that record.

When a record is updated all reference tables are checked for the values, if they do not exist in the refernce tables they are added and the new id is returned. If they do exist then the existing id of the value is returned. These ids are then used to update the 'main' table, along with the number of graduates entered into the web page.

The records in the reference tables are not updated as they may be used in other records.
CRUD functionality for the reference tables could be added at a later date.  This would require multiple pages and ideally a menu driven system.

Cancel button added to 'update form' for user friendliness.



Delete -->

Delete is a simply function with each record having it's own delete button to delete that record.

The record is deleted from the 'main' table but no values are deleted from the reference tables as they may be used in other records.


Search -->

A Search can be done by Institution. If the value typed in does not exist in the database no records will be shown, otherwise only the records for that institute will be displayed.

There is a button to clear the search so that all records are again shown. This simply reloads the entire page. (This is also the functionality if the search button is clicked when the seach input is empty).