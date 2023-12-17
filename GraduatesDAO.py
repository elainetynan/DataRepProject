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
         
    def create(self, values):
        cursor = self.getcursor()
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

        foundData = self.checkEntryExists("nfq_level", "NFQLevel", values[3], cursor)
        if not foundData:
            sql="insert into nfq_level (NFQLevel) values (%s)"
            vals = (values[3],)
            cursor.execute(sql, vals) # NFQLevel
            nfqID = cursor.lastrowid
        else:
            nfqID = foundData[0]

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
                return -1
        finally:
            # Close the cursor and connection
            self.closeAll()

    def getAll(self):
        cursor = self.getcursor()
        # Join tables
        sql = "SELECT graduates.id, institutions.Institutions, graduationyear.GraduationYear, \
            fieldofstudy.FieldOfStudy, nfq_level.NFQLevel, graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                        LEFT JOIN fieldofstudy ON graduates.FieldOfStudy = fieldofstudy.id \
                            LEFT JOIN nfq_level ON graduates.NFQ_Level = nfq_level.id \
                                LEFT JOIN graduationyear ON graduates.GraduationYear = graduationyear.id"

        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
        #print(results)
        for result in results:
            #print(result)
            returnArray.append(self.convertToDictionary(result))
        
        self.closeAll()
        return returnArray

    def findByID(self, id):
        cursor = self.getcursor()
        # Join tables
        sql = "SELECT graduates.id, institutions.Institutions, graduation_year.Graduation_Year, \
            field_of_study.Field_of_study, nfq_level.NFQ_Level,graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                    LEFT JOIN fieldofstudy ON graduates.FieldOfStudy = fieldofstudy.id \
                        LEFT JOIN nfq_level ON graduates.NFQ_Level = nfq_level.id \
                            LEFT JOIN graduationyear ON graduates.GraduationYear = graduationyear.id \
                                WHERE graduates.id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        returnvalue = self.convertToDictionary(result)
        self.closeAll()
        return returnvalue

    def update(self, values):
        cursor = self.getcursor()
        # ET: update all tables
        sql="update graduates set Institution= %s,GraduationYear=%s, FieldOfStudy=%s, NFQ_Level=%s, NumGraduates=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
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