import sqlite3

class databaseHandler():
    def __init__(self):
        self.conn = sqlite3.connect('lib/scores.db')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS humanVAI
        (NAME           TEXT  PRIMARY KEY  NOT NULL,
        SCORE            INT);''')
        self.conn.execute('''CREATE TABLE IF NOT EXISTS humanVHuman
        (NAME           TEXT  PRIMARY KEY  NOT NULL,
        SCORE            INT);''')
        self.conn.commit()
        self.tableName = ""

    def clearTable(self,tableCode):
        if tableCode==0:
            self.tableName = "humanVHuman"
        else:
            self.tableName = "humanVAI"
        self.conn.execute("DELETE FROM "+self.tableName)
        statement = "INSERT INTO " + self.tableName + "(NAME, SCORE) VALUES ('Draw',0)"
        self.conn.execute(statement)
        if tableCode==1:
            statement = "INSERT INTO " + self.tableName + "(NAME, SCORE) VALUES ('Computer',0)"
            self.conn.execute(statement)
        self.conn.commit()
    
    def incrementScore(self,name,tableCode):
        if tableCode==0:
            self.tableName = "humanVHuman"
        else:
            self.tableName = "humanVAI"
        data = self.conn.execute("SELECT NAME, SCORE FROM "+ self.tableName +" WHERE NAME = '"+name+"'" )
        statement = "INSERT INTO " + self.tableName + "(NAME, SCORE) VALUES ('" + name + "',1) ON CONFLICT (NAME) DO UPDATE SET Score=((SELECT SCORE FROM "+ self.tableName +" WHERE NAME='"+ name +"')+1)"
        self.conn.execute(statement)
        self.conn.commit()

    def returnTable(self,tableCode):
        if tableCode==0:
            self.tableName = "humanVHuman"
        else:
            self.tableName = "humanVAI"
        cursor = self.conn.execute("Select * from "+self.tableName + " ORDER BY NAME")
        data = []
        for row in cursor:
            data.append([row[0],row[1]])
        return data
        
    def __del__(self):
        self.conn.close()