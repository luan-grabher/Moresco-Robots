#Import SQLLite3
import sqlite3
#Import Pandas as pd
import pandas as pd
#Import configparser
import configparser
#import os
import os
import json

#import time
import time


#Get the configuration of 'moresco-robots.ini' file
config = configparser.ConfigParser()
config.read('../moresco-robots.ini')

#Connect to the database with the config 'database.path'
conn = sqlite3.connect(config['database']['path'])

#Get all calls from the database where 'started_at' and 'ended_at' is NULL
calls = pd.read_sql_query("SELECT * FROM calls WHERE started_at IS NULL AND ended_at IS NULL", conn)

#For each call
for call in calls.itertuples():
    #Get the robot from the call
    robot = pd.read_sql_query("SELECT * FROM robots WHERE id = ?", conn, params=(call.robot,))

    #if the robot is not empty
    if not robot.empty:
        #get first row of the robot
        robot = robot.iloc[0]

        #If the robot has parameters
        if robot.with_parameters_file == 1:
            #Get the parameters file path
            parameters_file_path = config['parameters']['path']
            #If the file exists, delete it
            if os.path.exists(parameters_file_path):
                os.remove(parameters_file_path)

            #create a new file to save the parameters
            parameters_file = open(parameters_file_path, 'w')

            #parameters = array of 'json_parameters' of call
            parameters = json.loads(call.json_parameters)

            #write '[idTarefa:call.id]/n' in the file
            parameters_file.write('[idTarefa:' + str(call.id) + ']\n')
            
            #For each parameter, convert to '[parameter:value]' and write in the file
            for parameter in parameters:       
                parameters_file.write('[{}:{}]\n'.format(parameter, str(parameters[parameter])))

            #Close the file
            parameters_file.close()

            #print the content of the file
            print("Content of the parameter file:")
            print(open(parameters_file_path).read())
        
        #Get the robot path
        robot_path = robot.path

        #If the robot file exists
        if os.path.exists(robot_path):
            '''
                OPEN ROBOT FILE
            '''
            #Get the robot file extension
            robot_extension = robot_path.split('.')[-1]

            #go to the parent directory of the robot file
            os.chdir(os.path.dirname(robot_path))

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
                os.system('{} {}'.format(robot_path, call.id))
            #If the robot file extension is .cmd
            elif robot_extension == 'cmd':
                #Execute the cmd with the command 'cmd'
                os.system('{} {}'.format(robot_path, call.id))
            #If the robot file extension is .xlsm
            elif robot_extension == 'xlsm':
                #Execute the excel with the command 'excel'
                os.system('excel {}'.format(robot_path))
            
            '''
                PARAMETERS FILE
            '''
            #If the robot has parameters
            if robot.with_parameters_file == 1:
                #wait the file has the text 'usado'
                while True:
                    #Open the file
                    parameters_file = open(parameters_file_path, 'r')
                    #Read the file
                    parameters_file_text = parameters_file.read()
                    #Close the file
                    parameters_file.close()

                    #If the file has the text 'usado'
                    if 'usado' in parameters_file_text:
                        #change the started_at of the call to now in sql format
                        conn.execute("UPDATE calls SET started_at = ? WHERE id = ?", (time.strftime('%Y-%m-%d %H:%M:%S'), call.id))
                        #commit the changes
                        conn.commit()

                        #break the loop
                        break
                    
                    #Wait 1 second
                    time.sleep(1)
        else:
            #json_return = '{"html":"Arquivo do robô não encontrado, contate o programador."}'
            json_return = '{"html":"Arquivo do robô não encontrado, contate o programador."}'
            #now in sql format
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            #change the started_at and ended_at of the call to now in sql format
            conn.execute("UPDATE calls SET started_at = ?, ended_at = ?, json_return = ? WHERE id = ?", (now, now, json_return, call.id))
            #commit the changes
            conn.commit()

            #print the error
            print("Arquivo do robô '", robot_path, "' não encontrado.")

        #Commit the changes
        conn.commit()