'''
    Na pasta da config 'parameters.return_path':
        - para todos os arquivos html:
            - Se o nome do arquivo sem o '.html' for integer,
                - procura no banco de dados uma call que tenha o id igual ao nome do arquivo sem o '.html'
                - se a call existir,
                    - pega o texto do arquivo html
                    - define no banco de dados as informações da call:
                        - status = 'finalizado'
                        - ended_at = datetime.now()
                        - return_json = json.dumps({'html': texto_do_arquivo_html})

'''
import configparser
import os
import sqlite3
import pandas as pd
import json


#Get the configuration of 'moresco-robots.ini' file
config = configparser.ConfigParser()
config.read('./moresco-robots.ini')

#connect to the database with the config 'database.path'
conn = sqlite3.connect(config['database']['path'])

def verify():
    #Na pasta da config 'parameters.return_path'
    path = config['parameters']['return_path']
    #For each file in the path
    for file in os.listdir(path):
        #If the file extension is 'html'
        if file.split('.')[-1] == 'html':
            try:
                #If the file name without '.html' is integer
                if int(file.split('.')[0]):
                    #Get the id from the file name
                    id = int(file.split('.')[0])
                    #Get the call from the database
                    call = pd.read_sql_query("SELECT * FROM calls WHERE id = ?", conn, params=(str(id),))
                    #If the call exists
                    if not call.empty:
                        #Get the html file path
                        html_file_path = os.path.join(path, file)
                        #Get the html file text
                        html_file = open(html_file_path, 'r')
                        #Get the html file text
                        html_text = html_file.read()
                        #Close the file
                        html_file.close()
                        #Delete the file
                        os.remove(html_file_path)
                        #Define the call as finished
                        pd.read_sql_query("UPDATE calls SET status = 'Finalizado', ended_at = datetime('now') WHERE id = ?", conn, params=(str(id),))
                        #Get the return json
                        return_json = json.dumps({'html': html_text})
                        #Define the return json in the database
                        pd.read_sql_query("UPDATE calls SET return_json = ? WHERE id = ?", conn, params=(return_json, str(id)))

                        #commit the changes
                        conn.commit()
            except:
                pass

verify()