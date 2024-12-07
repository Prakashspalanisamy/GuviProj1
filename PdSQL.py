# as sqlalchemy is not working in local i am going to use normal connection and get the sql and convert that into json and then into dataframe
import pandas as pd
import Db_Connection as DB
import mysql.connector

class PdSQL :
    def __init__(self):
        self.db = DB.Db_Connection()
        self.mycursor = self.db.connect_to_db()

    def getData(self,sql):
        try:
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            columns = [desc[0] for desc in self.mycursor.description]
            return pd.DataFrame(result, columns=columns)
        except mysql.connector.Error as err :
            print(f"Error: {err}")           

    def getDataAsList(self,sql):
        try:
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            flat_list = [item for row in result for item in row]
            return list(flat_list)
        except mysql.connector.Error as err :
            print(f"Error: {err}")    

    def getDataAsIntList(self,sql):
        try:
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            flat_list = [int(item) for row in result for item in row]
            return list(flat_list)
        except mysql.connector.Error as err :
            print(f"Error: {err}")    


    def close_connection(self):
        self.db.close_connection()    