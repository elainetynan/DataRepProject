import mysql.connector
import dbconfig as cfg

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
         
    def create(self, values):
        cursor = self.getcursor()
        # ET: need to check if all foreign keys exist, if not create record, return foreign key
        sql="insert into institutions (Institutions) values (%s)"
        vals = (values[0])
        cursor.execute(sql, vals) # Institution
        institutionID = cursor.lastrowid
        sql="insert into graduation_year (GraduationYear) values (%s)"
        cursor.execute(sql, values[1]) # Graduation Year
        yearID = cursor.lastrowid
        sql="insert into field_of_study (Field_Of_Study) values (%s)"
        cursor.execute(sql, values[2]) # Field of Study
        fieldID = cursor.lastrowid
        sql="insert into nfq_level (NFQ_Level) values (%s)"
        cursor.execute(sql, values[3]) # Field of Study
        nfqID = cursor.lastrowid
        values = (institutionID, yearID, fieldID, nfqID, values[4])
        sql="insert into graduates (Institution, GraduationYear, FieldOfStudy, NFQ_Level, NumGraduates) values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, values)

        self.connection.commit()
        newid = cursor.lastrowid
        self.closeAll()
        return newid

    def getAll(self):
        cursor = self.getcursor()
        # ET: Join tables
        #sql="select * from graduates"
        sql = "SELECT graduates.id, institutions.Institutions, graduation_year.Graduation_Year, \
            field_of_study.Field_of_study, nfq_level.NFQ_Level, graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                        LEFT JOIN field_of_study ON graduates.FieldOfStudy = field_of_study.id \
                            LEFT JOIN nfq_level ON graduates. NFQ_Level = nfq_level.id \
                                LEFT JOIN graduation_year ON graduates. GraduationYear = graduation_year.id"

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
        # ET: Join tables
        #sql="select * from graduates where id = %s"
        sql = "SELECT graduates.id, institutions.Institutions, graduation_year.Graduation_Year, \
            field_of_study.Field_of_study, nfq_level.NFQ_Level,graduates.NumGraduates \
                FROM graduates LEFT JOIN institutions ON graduates.Institution = institutions.id \
                    LEFT JOIN field_of_study ON graduates.FieldOfStudy = field_of_study.id \
                        LEFT JOIN nfq_level ON graduates. NFQ_Level = nfq_level.id \
                            LEFT JOIN graduation_year ON graduates. GraduationYear = graduation_year.id \
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
        # ET: This doesn't change
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