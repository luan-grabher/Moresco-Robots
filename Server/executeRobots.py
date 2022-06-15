#Import SQLLite3
import sqlite3
#Import Pandas as pd
import pandas as pd
#Import configparser
import configparser
#import os
import os, sys
import json
import subprocess

#import time
import time

#import Robot upping two levels
p = os.path.abspath('..') # get parent directory
sys.path.insert(1, p) # add current directory to path
from Robots.Python.libs.Robot import Robot


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

            #String command to execute the robot
            command = ''
            #If the robot file extension is .jar
            if robot_extension == 'jar':
                #Execute the jar with the command 'java -jar'
                command = 'java -jar {} {}'.format(robot_path, call.id)
            #If the robot file extension is .py
            elif robot_extension == 'py':
                #Execute the python with the command 'py'
                command = 'python {} {}'.format(robot_path, call.id)
            #If the robot file extension is .bat or .cmd
            elif robot_extension == 'bat' or robot_extension == 'cmd':
                #Execute the bat with the command 'cmd'
                command = '{} {}'.format(robot_path, call.id)
            #If the robot file extension is .xlsm
            elif robot_extension == 'xlsm':
                #Execute the excel with the command 'excel'
                command = 'excel {}'.format(robot_path)

            #Call the command
            processo = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            output = processo.stdout.read()
            #remove b' from the output
            output = output.decode('utf-8')        
            
            '''
                PARAMETERS FILE
            '''
            print("Execução solicitada")
            
            #If the robot has parameters
            if robot.with_parameters_file == 1:
                print("Esperando robô retornar que iniciou pelo arquivo de parametros...")
                counter = 0
                
                #wait the file has the text 'usado' while the counter is less than max start time
                while counter < int(config['parameters']['max_start_time']):
                    #show counter of seconds waiting
                    counter = counter + 1
                    print(counter, end="\r")
                    
                    #Open the file
                    parameters_file = open(parameters_file_path, 'r')
                    #Read the file
                    parameters_file_text = parameters_file.read()
                    #Close the file
                    parameters_file.close()

                    #If the file has the text 'usado'
                    if 'usado' in parameters_file_text:
                        #Instantiate the robot to set started_at
                        Robot(call.id)
                        #break the loop
                        break
                    
                    #Wait 1 second
                    time.sleep(1)

                #If the counter is greater than or equal max start time
                if counter >= int(config['parameters']['max_start_time']):
                    #Instantiate the robot to set started_at
                    call = Robot(call.id)
                    #Set return to output of console
                    call.setReturn(str(output))
        else:
            #set message return
            message_return = "Arquivo do robô '", robot_path, "' não encontrado, contate o programador"
            
            #instantiate a new robot
            call = Robot(call.id)
            #set the message return
            call.setReturn(message_return)

            #print the error
            print(message_return)

        #Commit the changes
        conn.commit()
