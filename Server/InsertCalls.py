import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import sqlite3
import time
import pandas as pd

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
        #conn.commit()

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

                #send email to 'ti01@moresco.cnt.br' with json_return
                send_email('ti01@moresco.cnt.br', json_return)
        
        #wait 1 second
        time.sleep(1)

#send email to and json_return to 
def send_email(email, json_return):
    #convert json string to json object
    json_return = json.loads(json_return)
    html = json_return['html']
    
    #get email config from 'email_config.ini'
    mailconfig = configparser.ConfigParser()
    mailconfig.read('email_config.ini')

    #get username and password from section 'gmail' of 'email_config.ini'
    username = mailconfig['gmail']['username']
    password = mailconfig['gmail']['password']

    print('Enviando e-mail para ' + email)
    print('Mensagem: ' + html)
    print('------------------------------------------------------')
    print('Username: ' + username)
    print('Password: ' + password)

    try:
        #create email
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = email
        msg['Subject'] = 'Moresco Robot'
        msg.attach(MIMEText(html, 'html'))
        
        #create server
        server = smtplib.SMTP_SSL('smtp.gmail.com', '587')
        server.login(username, password)
        text = msg.as_string()

        print('Enviando e-mail para ' + email)

        server.sendmail(username, email, text)
        server.close()
    except Exception as e:
        print('Erro ao enviar e-mail para ' + email)
        print(e)

            