'''
    Class Robot to get the robot and call information from the database
'''

#Imports the configparser
import configparser
#import database
import sqlite3
import pandas as pd
import json

#Get config from 'moresco-robots.ini' file
config = configparser.ConfigParser()
config.read('../moresco-robots.ini')

#Connect to the database with the config 'database.path'
conn = sqlite3.connect(config['database']['path'])

class Robot():
    #Constructor with call_id
    def __init__(self, call_id):
        #Get the call from the database
        self.call = pd.read_sql_query("SELECT * FROM calls WHERE id = ?", conn, params=(call_id,))
        self.robot = None
        self.parameters = None

        #If the call is not empty
        if not self.call.empty:
            #Get the first row of the call
            self.call = self.call.iloc[0]

            #Update started_at in the call with the current datetime   in sql format (YYYY-MM-DD HH:MM:SS)
            self.call.started_at = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            #Sql to update the call started_at as current datetime
            sql = "UPDATE calls SET started_at = ? WHERE id = ?"
            #Execute the sql
            conn.execute(sql, (str(self.call.started_at), str(self.call.id)))
            #Commit the changes
            conn.commit()

            #SQL query to get the robot from the call
            sql = "SELECT * FROM robots WHERE id = " + str(self.call.robot)
            #Get the robot from the database
            robot = pd.read_sql_query(sql, conn)

            #If the robot is not empty
            if not robot.empty:
                #Get the first row of the robot
                self.robot = robot.iloc[0]
                
                #convert parameters_json in call to a dictionary
                self.parameters = json.loads(self.call.json_parameters)
    
    #Function to set call.json_return, and call.ended_at as current datetime
    def setReturn(self, json_return):
        #if json_return is not empty
        if json_return:
            #if json_return not is a string, dump it to json
            if not isinstance(json_return, str):
                json_return = json.dumps(json_return)

            #Get the current datetime in sql format (YYYY-MM-DD HH:MM:SS)
            ended_at = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
            #Sql to update the call ended_at as current datetime and json_return
            sql = "UPDATE calls SET json_return = ?, ended_at = ? WHERE id = ?"
            #Execute the sql
            conn.execute(sql, (str(json_return), str(ended_at), str(self.call.id)))
            #Commit the changes
            conn.commit()

        

    