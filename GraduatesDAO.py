import mysql.connector
import dbconfig as cfg
from mysql.connector import errorcode

class GraduatesDAO:
    connection=""
    cursor =''
    host=       ''
    user=       ''
    password=   ''
    database=   ''
    
    def __init__(self):
        self.host=       cfg.mysql['host']
        self.user=       cfg.mysql['user']
        self.password=   cfg.mysql['password']
        self.database=   cfg.mysql['database']

    def getcursor(self): 
        self.connection = mysql.connector.connect(
            host=       self.host,
            user=       self.user,
            password=   self.password,
            database=   self.database,
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        self.connection.close()
        self.cursor.close()
        
    def checkEntryExists(self, table, field, val, cursor):
        sql = "SELECT id FROM "+table+" WHERE "+table+"."+field+" = %s"
        values = (val,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        #returnvalue = self.convertToDictionary(result)
        return result

    # Get reference table id or create new record and return new id
    def getRefTableId(self, table, field, val, cursor):
        foundData = self.checkEntryExists(table, field, val, cursor)
        if not foundData:
            sql="insert into "+table+" ("+field+") values (%s)"
            vals = (val,)
            cursor.execute(sql, vals)
            id = cursor.lastrowid
        else:
            id = foundData[0]
        return id
         
    def create(self, values):
        cursor = self.getcursor()
        # Need to check if all foreign keys exist, if not create record, return foreign key
        institutionID = self.getRefTableId("institutions", "Institutions", values[0], cursor)
        yearID = self.getRefTableId("graduationyear", "GraduationYear", values[1], cursor)
        fieldID = self.getRefTableId("fieldofstudy", "FieldOfStudy", values[2], cursor)
        nfqID = self.getRefTableId("nfqlevel", "NFQLevel", values[3], cursor)

        try:
            values = (institutionID, yearID, fieldID, nfqID, values[4])
            sql="insert into graduates (Institution, GraduationYear, FieldOfStudy, NFQ_Level, NumGraduates) values (%s,%s,%s,%s,%s)"
            cursor.execute(sql, values)
            self.connection.commit()
            newid = cursor.lastrowid
            self.closeAll()
            return newid
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise Exception("Duplicate Record")
        finally:
            # Close the cursor and connection
            self.closeAll()

    def getAll(self):
        cursor = self.getcursor()
        # Join tables
        sql = "SELECT graduates.id, institutions.Institutions, graduationyear.GraduationYear, \
            fieldofstudy.FieldOfStudy, nfqlevel.NFQLevel, graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                        LEFT JOIN fieldofstudy ON graduates.FieldOfStudy = fieldofstudy.id \
                            LEFT JOIN nfqlevel ON graduates.NFQ_Level = nfqlevel.id \
                                LEFT JOIN graduationyear ON graduates.GraduationYear = graduationyear.id"

        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        # Join tables
        sql = "SELECT graduates.id, institutions.Institutions, graduationyear.GraduationYear, \
            fieldofstudy.FieldOfStudy, nfqlevel.NFQLevel, graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                    LEFT JOIN fieldofstudy ON graduates.FieldOfStudy = fieldofstudy.id \
                        LEFT JOIN nfqlevel ON graduates.NFQ_Level = nfqlevel.id \
                            LEFT JOIN graduationyear ON graduates.GraduationYear = graduationyear.id \
                                WHERE graduates.id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def getByInstitute(self, institute):
        cursor = self.getcursor()
        # Join tables
        sql = "SELECT graduates.id, institutions.Institutions, graduationyear.GraduationYear, \
            fieldofstudy.FieldOfStudy, nfqlevel.NFQLevel, graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                        LEFT JOIN fieldofstudy ON graduates.FieldOfStudy = fieldofstudy.id \
                            LEFT JOIN nfqlevel ON graduates.NFQ_Level = nfqlevel.id \
                                LEFT JOIN graduationyear ON graduates.GraduationYear = graduationyear.id \
                                    WHERE institutions.Institutions = %s"

        values = (institute,)
       
        cursor.execute(sql, values)
        results = cursor.fetchall()
        if bool(results):
            returnArray = []
            for result in results:
                #print(result)
                returnArray.append(self.convertToDictionary(result))
        else:
            result = (-1,-1,-1,-1,-1,-1)
            returnArray = []
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray
        

    def update(self, values):
        cursor = self.getcursor()
        # Need to check if all foreign keys exist, if not create record, return foreign key
        institutionID = self.getRefTableId("institutions", "Institutions", values[0], cursor)
        yearID = self.getRefTableId("graduationyear", "GraduationYear", values[1], cursor)
        fieldID = self.getRefTableId("fieldofstudy", "FieldOfStudy", values[2], cursor)
        nfqID = self.getRefTableId("nfqlevel", "NFQLevel", values[3], cursor)

        # Update main table
        sql="update graduates set Institution=%s, GraduationYear=%s, FieldOfStudy=%s, NFQ_Level=%s, NumGraduates=%s where id = %s"
        vals = (institutionID, yearID, fieldID, nfqID, values[4], values[5])

        try:
            cursor.execute(sql, vals)
            self.connection.commit()
            self.closeAll()
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_DUP_ENTRY:
                raise Exception("Duplicate Record")
        finally:
            # Close the cursor and connection
            self.closeAll()
        
    def delete(self, id):
        cursor = self.getcursor()
        sql="delete from graduates where id = %s"
        values = (id,)
        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll()
        print("delete done")

    def convertToDictionary(self, result):
        colnames=['id','Institution','GraduationYear', "FieldOfStudy", "NFQ_Level", "NumGraduates"]
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item
        
GraduatesDAO = GraduatesDAO()