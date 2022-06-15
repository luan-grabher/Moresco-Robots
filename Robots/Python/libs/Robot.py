'''
    Class Robot to get the robot and call information from the database
'''

#Imports the configparser
import configparser
#import database
import sqlite3
import pandas as pd
import json

config_path  = '../moresco-robots.ini'

#Get config from 'moresco-robots.ini' file
config = configparser.ConfigParser()
config.read(config_path)

#Connect to the database with the config 'database.path'
conn = sqlite3.connect(config['database']['path'])

class Robot():
    #Constructor with call_id
    def __init__(self, call_id, database_path = None):
        self.conn = conn
        #If has database_path set conn to connect to the database with the database_path
        if database_path:
            self.conn = sqlite3.connect(database_path)            

        #if call_id is not None
        if call_id:                
            #Get the call from the database
            self.call = pd.read_sql_query("SELECT * FROM calls WHERE id = ?", self.conn, params=(call_id,))
            self.robot = 0
            self.parameters = []

            #If the call is not empty
            if not self.call.empty:
                #Get the first row of the call
                self.call = self.call.iloc[0]

                #Update started_at in the call with the current datetime   in sql format (YYYY-MM-DD HH:MM:SS)
                self.call.started_at = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                #Sql to update the call started_at as current datetime
                sql = "UPDATE calls SET started_at = ? WHERE id = ?"
                #Execute the sql
                self.conn.execute(sql, (str(self.call.started_at), str(self.call.id)))
                #Commit the changes
                self.conn.commit()

                #SQL query to get the robot from the call
                sql = "SELECT * FROM robots WHERE id = " + str(self.call.robot)
                #Get the robot from the database
                robot = pd.read_sql_query(sql, self.conn)

                #If the robot is not empty
                if not robot.empty:
                    #Get the first row of the robot
                    self.robot = robot.iloc[0]
                    
                    #convert parameters_json in call to a dictionary
                    self.parameters = json.loads(self.call.json_parameters)
        else:
            #If the call_id is empty

            #call os empty
            self.call = pd.DataFrame()
            self.robot = 0
            self.parameters = []
        
    #Function to set call.json_return, and call.ended_at as current datetime
    def setReturn(self, json_return):
        #if json_return is not empty
        if json_return:
            #if json_return not is a string, dump it to json
            if not isinstance(json_return, str):
                #if not has 'html' key, dump it to json with 'html' key
                if not 'html' in json_return:
                    json_return = json.dumps({'html': json_return})
                else:
                    json_return = json.dumps(json_return)
            #if json_return is a string
            else:
                #verify if json_return is a json
                try:
                    #try to convert json_return to json
                    json_load =  json.loads(json_return)

                    #if not has 'html' key, dump it to json with 'html' key
                    if not 'html' in json_load:
                        json_return = json.dumps({'html': json_return})
                except:
                    #if string is not a json, convert it to json with 'html' as key
                    json_return = json.dumps({'html': json_return})
            
            #print 'html' key of json_return replacing '<br>' with '\n'
            print(json_return.replace('<br>', '\n'))

            #if call is not None
            if not self.call.empty:
                #Get the current datetime in sql format (YYYY-MM-DD HH:MM:SS)
                ended_at = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                #Sql to update the call ended_at as current datetime and json_return
                sql = "UPDATE calls SET json_return = ?, ended_at = ? WHERE id = ?"
                #Execute the sql
                self.conn.execute(sql, (str(json_return), str(ended_at), str(self.call.id)))
                #Commit the changes
                self.conn.commit()

                print('Call ' + str(self.call.id) + ' ended at ' + str(ended_at))
            else:
                #If the call is empty, print that is a test
                print("ISSO FOI APENAS UM TESTE")
        else:
            #If json_return is empty, print it
            print("JSON_RETURN VAZIO")