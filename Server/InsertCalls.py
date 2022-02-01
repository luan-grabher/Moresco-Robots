import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import sqlite3
import time
import pandas as pd
from Email import send_email

#import config of '../moresco-robots.ini'
config = configparser.ConfigParser()
config.read('../moresco-robots.ini')
#connect to database with 'database.path'
conn = sqlite3.connect(config['database']['path'])

today = time.strftime("%Y-%m-%d %H:%M:%S")

#function to excecute calls
def execute_calls(calls_to_execute):
    #insert calls in database
    for call in calls_to_execute:
        sql = "INSERT INTO calls (robot, user, created_at, json_parameters) VALUES (?, ?, ?, ?)"
        conn.execute(sql, (call['robot'], call['user'], call['created_at'], call['json_parameters']))
        conn.commit()

    #For each call in calls to exec
    for call in calls_to_execute:
        # get the id of the call where the robot = call.robot and created_at = today
        call_id = pd.read_sql_query("SELECT id FROM calls WHERE robot = ? AND created_at = ?", conn, params=(call['robot'], call['created_at'])).iloc[0]['id']

        #add the id of the call
        call['id'] = call_id


    #callsOK = count of calls with status = Finalizado 
    callsOK = 0

    while callsOK != len(calls_to_execute):
        print('Esperando resposta do robô...')

        #for each call in calls to execute
        for call in calls_to_execute:
            #query to select on database the call with id = call.id and ended_at is not null
            query = "SELECT json_return FROM calls WHERE id = " + str(call['id']) + " AND ended_at IS NOT NULL"
            #select the call with id = call.id and ended_at is not null
            json_return = conn.execute(query).fetchone()

            #if the call is ended and not exists 'status' in call
            if json_return and 'status' not in call:
                #set the status of the call to 'Finalizado'
                call['status'] = 'Finalizado'
                #increment callsOK
                callsOK += 1

                #json_return is the first element of json_return
                json_return = json_return[0]
                
                print('Tarefa ' + str(call['id']) + ' finalizada com sucesso, enviando e-mail para ti01')

                #convert json_return to json and get the 'html'
                html = json.loads(json_return)['html']

                #send email to 'ti01@moresco.cnt.br' with json_return
                send_email('ti01@moresco.cnt.br', html, 'Retorno Tarefa ' + str(call['id']))
        
        #wait 1 second
        time.sleep(1)

            