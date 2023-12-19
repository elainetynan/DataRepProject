# ASK ANDREW
# Do we upload the venv folder to github?
# Deferral of modules


vals = ("aa", "bb", "cc")
print(type(vals))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Need to check if all foreign keys exist, if not create record, return foreign key
        foundData = self.checkEntryExists("institutions", "Institutions", values[0], cursor)
        if not foundData:
            sql="insert into institutions (Institutions) values (%s)"
            vals = (values[0],)
            cursor.execute(sql, vals) # Institution
            institutionID = cursor.lastrowid
        else:
            institutionID = foundData[0]
        
        foundData = self.checkEntryExists("graduationYear", "GraduationYear", values[1], cursor)
        if not foundData:
            sql="insert into graduationYear (GraduationYear) values (%s)"
            vals = (values[1],)
            cursor.execute(sql, vals) # GraduationYear
            yearID = cursor.lastrowid
        else:
            yearID = foundData[0]
            
        foundData = self.checkEntryExists("fieldofstudy", "FieldOfStudy", values[2], cursor)
        if not foundData:
            sql="insert into fieldofstudy (FieldOfStudy) values (%s)"
            vals = (values[2],)
            cursor.execute(sql, vals) # FieldOfStudy
            fieldID = cursor.lastrowid
        else:
            fieldID = foundData[0]

        foundData = self.checkEntryExists("nfqlevel", "NFQLevel", values[3], cursor)
        if not foundData:
            sql="insert into nfqlevel (NFQLevel) values (%s)"
            vals = (values[3],)
            cursor.execute(sql, vals) # NFQLevel
            nfqID = cursor.lastrowid
        else:
            nfqID = foundData[0]

            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        
        # Need to check if all foreign keys exist, if not create record, return foreign key
        institutionID = self.getRefTableId("institutions", "Institutions", values[0], cursor)
        yearID = self.getRefTableId("graduationYear", "GraduationYear", values[1], cursor)
        fieldID = self.getRefTableId("fieldofstudy", "FieldOfStudy", values[2], cursor)
        nfqID = self.getRefTableId("nfqlevel", "NFQLevel", values[3], cursor)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # Get reference table id or create new record and return new id
    def getRefTableId(self, table, field, val, cursor):
        foundData = self.checkEntryExists(table, field, val, cursor)
        if not foundData:
            sql="insert into table (field) values (%s)"
            vals = (val,)
            cursor.execute(sql, vals)
            id = cursor.lastrowid
        else:
            id = foundData[0]
        return id