from ast import While
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
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
    #list of calls to execute
    calls_to_execute = []

    #insert calls in database
    for call in calls_to_execute:
        sql = "INSERT INTO calls (robot, user, created_at, json_parameters) VALUES (?, ?, ?, ?)"
        conn.execute(sql, (call['robot'], call['user'], call['created_at'], call['json_parameters']))

    #For each call in calls to exec
    for call in calls_to_execute:
        # get the id of the call where the robot = call.robot and created_at = today
        call_id = pd.read_sql_query("SELECT id FROM calls WHERE robot = ? AND created_at = ?", conn, params=(call['robot'], call['created_at'])).iloc[0]['id']

        #add the id of the call
        call['id'] = call_id


    #callsOK = count of calls with status = Finalizado 
    callsOK = 0

    while callsOK != len(calls_to_execute):
        #for each call in calls to execute
        for call in calls_to_execute:
            #get status of call from database
            status = pd.read_sql_query("SELECT status FROM calls WHERE id = ?", conn, params=(call['id'],)).iloc[0]['status']

            #if call has no 'status' and status in db is 'Finalizado'
            if not call.get('status') and status == 'Finalizado':
                #increment callsOK
                callsOK += 1
                #put status = 'Finalizado' in call
                call['status'] = 'Finalizado'

                #send email to 'ti01@moresco.cnt.br' with json_return
                send_email('ti01@moresco.cnt.br', call['json_return'])

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

    #create email
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = email
    msg['Subject'] = 'Moresco Robot'
    msg.attach(MIMEText(html, 'html'))
    
    #create server
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    text = msg.as_string()
    server.sendmail(username, email, text)
    server.quit()

            