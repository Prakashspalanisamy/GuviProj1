import mysql.connector
import Db_Connection as DB
import API_Call_Sportradar as AC

class Load_Date:
    def __init__(self):
        self.db = DB.Db_Connection()
        self.mycursor = self.db.connect_to_db()
    

    def load_data(self):

        try:
            ac = AC.API_Call_Sportradar("competitions.json")
            response = ac.call_api()
            res_json = response.json()
            self.load_Competitions(res_json['competitions'])

            ac = AC.API_Call_Sportradar("complexes.json")
            response = ac.call_api()
            res_json = response.json()
            self.load_Complexes(res_json['complexes'])        

            ac = AC.API_Call_Sportradar("rankings.json")
            response = ac.call_api()
            res_json = response.json()
            self.load_Competitor_Rankings(res_json['rankings'])

            
        except Exception as e:
            print(f"An error occurred: {e}")


################################################ load Categories #########################################
    
    def load_Categories(self,data):
        try:
            sql = f'''select count(*) from guviproj1.Categories where category_id = "{data['id']}"'''
            result = self.exesel(sql)
            
            if result[0] <= 0: # handling duplicate data
                sql = f'''insert into guviproj1.Categories values ("{data['id']}" , "{data['name']}")''' # here category can be only one per competition, hence it is dictionary should not loop
                self.exe(sql)
        except Exception as e:
            print(f"An error occurred: {e}")


################################################ load Competition #########################################
    def load_Competitions(self,data):
        try:

            parent_id = ''
            for i in data:
                if 'category' in i:
                    self.load_Categories(i['category']) # by design this if will always pass as there is no blank ID in the table. yet added just in case

                if 'parent_id' in  i:
                    parent_id = i['parent_id']
                else:
                    parent_id = ' '

                sql = f'''select count(*) from guviproj1.Competitions where competition_id = "{i['id']}"'''
                result = self.exesel(sql)
                if result[0] <= 0:
                    sql = f'''insert into guviproj1.Competitions values ("{i['id']}" , "{i['name']}" , "{parent_id}" , "{i['type']}" ,"{i['gender']}" , "{i['category']['id']}")'''
                    self.exe(sql)
        except Exception as e:
            print(f"An error occurred: {e}")


################################################ load Complexes #########################################
    def load_Complexes(self,data):
        try:

            for i in data: #complexes main data some might not have venus as separate entity
                sql = f'''select count(*) from guviproj1.Complexes where complex_id = "{i['id']}"'''
                result = self.exesel(sql)
                if result[0] <= 0:
                    name = self.skipquote(i['name'])
                    sql = f'''insert into guviproj1.Complexes values ("{i['id']}" , "{name}"  )'''
                    self.exe(sql)
                    if 'venues' in i: # as venue is optional only calling if venue is available.
                        self.load_Venues(i['venues'],i['id']) 
        except Exception as e:
            print(f"An error occurred: {e}")


################################################ load Venues #########################################
    def load_Venues(self,data,complexes_id):
        try:

            for i in data: # venue is list in the response hence more than one venue per complex is possible hence looping.
                sql = f'''select count(*) from guviproj1.Venues where venue_id = "{i['id']}"'''
                result = self.exesel(sql)
                if result[0] <= 0:            
                    sql = f'''insert into guviproj1.Venues values ("{i['id']}" , "{i['name']}" , "{i['city_name']}" , "{i['country_name']}" ,"{i['country_code']}" , "{i['timezone']}", "{complexes_id}")'''
                    self.exe(sql)
        except Exception as e:
            print(f"An error occurred: {e}")     


################################################ load Competitors #########################################
    def load_Competitors(self,data):
        try:

            country_code = '' # there is country called ""Neutral""" which dont have country code, but as per requirement it cannot be null so assigning blank.
            #as only there will be only one competitor per rank no loop needed. as response is returning dic not list.

            if 'country_code' in data:
                country_code = data['country_code']
            else:
                country_code = ' '

            sql = f'''select count(*) from guviproj1.Competitors where competitor_id = "{data['id']}"'''
            result = self.exesel(sql)
            if result[0] <= 0:   
                sql = f'''insert into guviproj1.Competitors values ("{data['id']}" , "{data['name']}" , "{data['country']}" , "{country_code}" , "{data['abbreviation']}")'''
                self.exe(sql)
        except Exception as e:
            print(f"An error occurred: {e}")

            

################################################ load Competitor Rankings #########################################
    def load_Competitor_Rankings(self,data):
        try:

            gender = ''
            year = ''
            week = ''
            for j in data:

                gender = j['gender']
                year = j['year']
                week = j['week']

                for i in j['competitor_rankings']:
                    if 'competitor' in i:
                        self.load_Competitors(i['competitor']) # by design this if will always pass as there is no blank ID in the table. yet added just in case
                        
                    sql = f'''insert into guviproj1.Competitor_Rankings values ( null , {i['rank']} , {i['movement']} , {i['points']} ,{i['competitions_played']} , "{gender}" , {year}, {week}, "{i['competitor']['id']}")'''
                    self.exe(sql)
        except Exception as e:
            print(f"An error occurred: {e}")

################################################ delete all data in all the 6 tables  #########################################

    def Delete_tables(self):
        self.delt("guviproj1.Competitions")        
        self.delt("guviproj1.Categories")
        self.delt("guviproj1.Venues")
        self.delt("guviproj1.Complexes")
        self.delt("guviproj1.Competitor_Rankings")        
        self.delt("guviproj1.Competitors")
  
        # self.load_data()


################################################ only rank is based on the year and week, deleting only that table data  #########################################
    def Delete_Current_week(self):
        try:
            ac = AC.API_Call_Sportradar("rankings.json")
            response = ac.call_api()
            res_json = response.json()        
            year = ''
            week = ''
            for i in res_json['rankings']:
                year = i['year']
                week = i['week']
                break

            sql = f"delete from guviproj1.Competitor_Rankings where year = {year} and week = {week}"
            self.exe(sql)
        except Exception as e:
            print(f"An error occurred: {e}")


################################################ Delete all the line in the table #########################################
    def delt(self,table_name):
        sql = f"Delete from {table_name} where 1=1"
        self.exe(sql)


################################################ execute the SQL and commit to database #########################################
    def exe(self,sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit_db()       
        except mysql.connector.Error as err :
            print(f"Error: {err}")   
        

################################################ check for existing data to avoid primary key duplication #########################################        
    def exesel(self,sql):
        try:
            self.mycursor.execute(sql)
            return self.mycursor.fetchone()
        except mysql.connector.Error as err :
            print(f"Error: {err}")           


################################################ skip " in the data to avoid SQL execution Error #########################################  
    def skipquote(self, col):
        col = col.replace('''"''', '''\\"''')
        return col


################################################ close the connection ######################################### 
    def close_connection(self):
        self.db.close_connection()



