#Import SQLLite3
import sqlite3
#Import Pandas as pd
import pandas as pd
#Import configparser
import configparser
#import os
import os


#Get the configuration of 'moresco-robots.ini' file
config = configparser.ConfigParser()
config.read('moresco-robots.ini')

#Connect to the database with the config 'database.path'
conn = sqlite3.connect(config['database']['path'])

#Get all calls from the database where 'started_at' and 'ended_at' is NULL
calls = pd.read_sql_query("SELECT * FROM calls WHERE started_at IS NULL AND ended_at IS NULL", conn)

#For each call
for call in calls.itertuples():
    #Get the robot from the call
    robot = pd.read_sql_query("SELECT * FROM robots WHERE id = ?", conn, params=(call.robot,))

    #If the robot has parameters
    if robot.with_parameters_file == 1:
        #Get json from the call
        json = call.json

        #Get the parameters file path
        parameters_file_path = config['parameters']['path']
        #If the file exists, delete it
        if os.path.exists(parameters_file_path):
            os.remove(parameters_file_path)

        #create a new file to save the parameters
        parameters_file = open(parameters_file_path, 'w')

        #Decode the json
        parameters = json.decode('utf-8')
        
        #For each parameter, convert to '[parameter=value]' and write in the file
        for parameter in parameters.itertuples():
            #Write the parameter in the file
            parameters_file.write('[{}={}]\n'.format(parameter.name, parameter.value))
        #Close the file
        parameters_file.close()        
    
    #Get the robot path
    robot_path = robot.path

    #If the robot file exists
    if os.path.exists(robot_path):
        #Get the robot file extension
        robot_extension = robot_path.split('.')[-1]

        #If the robot file extension is .jar
        if robot_extension == 'jar':
            #Execute the jar with the command 'java -jar'
            os.system('java -jar {} {}'.format(robot_path, call.id))
        #If the robot file extension is .py
        elif robot_extension == 'py':
            #Execute the python with the command 'py'
            os.system('py {} {}'.format(robot_path, call.id))
        #If the robot file extension is .bat
        elif robot_extension == 'bat':
            #Execute the bat with the command 'cmd'
            os.system('cmd {} {}'.format(robot_path, call.id))
        #If the robot file extension is .xlsm
        elif robot_extension == 'xlsm':
            #Execute the excel with the command 'excel'
            os.system('excel {} {}'.format(robot_path, call.id))

    #Update the call with the started_at = now
    conn.execute("UPDATE calls SET started_at = datetime('now') WHERE id = ?", (call.id,))

    #Commit the changes
    conn.commit()

    #If the robot has parameters
    if robot.with_parameters_file == 1:
        #wait 30 seconds
        os.system('sleep 30')
