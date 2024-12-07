import mysql.connector

class Db_Connection:
    def __init__(self):
        try:

            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",)
            if self.connection.is_connected():
                print("Connected to MySQL database")
            else:
                print("Failed to connect to the database.")

        except mysql.connector.Error as err:
             print(f"Error: {err}")
        

    def connect_to_db(self):
        try:
            if self.connection.is_connected():
                return self.connection.cursor()
            else:
                return ''    
        except mysql.connector.Error as err :
            print(f"Error: {err}")

        

    def commit_db(self):
        try:
            if self.connection.is_connected():
                self.connection.commit()
        except mysql.connector.Error as err :
            print(f"Error: {err}")        

    def close_connection(self):
        try:
            if self.connection.is_connected():
                self.connection.close()
        except mysql.connector.Error as err :
            print(f"Error: {err}")                


# d = Db_Connection()
# mycursor = d.connect_to_db()
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#   print(x)
