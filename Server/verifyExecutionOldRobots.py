import configparser
import os
import sqlite3
import time
import pandas as pd
import json
import sys

# Get the configuration of 'moresco-robots.ini' file
config = configparser.ConfigParser()
config.read('../moresco-robots.ini')

# connect to the database with the config 'database.path'
conn = sqlite3.connect(config['database']['path'])


def verify():
    # Na pasta da config 'parameters.return_path'
    path = config['parameters']['return_path']
    # For each file in the path
    for file in os.listdir(path):
        # If the file extension is 'html'
        if file.split('.')[-1] == 'html':
            try:
                # If the file name without '.html' is integer
                if int(file.split('.')[0]):
                    # Get the id from the file name
                    id = int(file.split('.')[0])
                    # Get the call from the database
                    call = pd.read_sql_query(
                        "SELECT * FROM calls WHERE id = ?", conn, params=(str(id),))
                    # If the call exists
                    if not call.empty:
                        # Get the html file path
                        html_file_path = os.path.join(path, file)
                        # Get the html file text
                        html_file = open(html_file_path, 'r')
                        # Get the html file text
                        html_text = html_file.read()
                        # Replace first § by '<br><br>'
                        html_text = html_text.replace('§', '<br><br>')
                        # Close the file
                        html_file.close()
                        # Delete the file
                        # os.remove(html_file_path)

                        # Get the return json
                        return_json = json.dumps({'html': html_text})

                        # Define the call as finished in the database and json_return with the return json
                        conn.execute("UPDATE calls SET ended_at = ?, json_return = ? WHERE id = ?",
                                     (time.strftime('%Y-%m-%d %H:%M:%S'), return_json, str(id)))

                        # commit the changes
                        conn.commit()

                        # print that the call was finished
                        print('Call {} finished'.format(id))

            except Exception as e:
                # print full error with the line number
                print('Error in line {}'.format(
                    sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


verify()
