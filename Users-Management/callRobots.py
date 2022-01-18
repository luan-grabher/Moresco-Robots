'''
    Gui for calling robots creating a 'call' in 'calls' table of database.
    The call is created with the user of system.
    Equals on 'manageRobots.py', show a gui to choice a department, 
        show a gui to choice enterprise of robots on that department,
        and finally show a gui to choice robots on that enterprise and department.
'''

# Importing libraries
from tkinter.constants import END
import pandas as pd
import sqlite3
import sys
import os
import time
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json
import webbrowser
from tkcalendar import DateEntry

# Get config of 'moresco-robots.ini'
from configparser import ConfigParser
config = ConfigParser()
config.read('../moresco-robots.ini')

# Connect to database.path on config and get all robots with sqlite3 and pandas
conn = sqlite3.connect(config['database']['path'])

# Get all robots from database with pandas
robots = pd.read_sql_query("SELECT * FROM robots order by name", conn)

# List of unique departments
departments = robots['department'].unique()
# List of unique enterprises
enterprises = robots['enterprise'].unique()

# Get user of system
user = os.getlogin()

#months
months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

# Class for gui
class CallRobots():
    # Constructor
    def __init__(self):
        #gui call
        self.window = None
        
        # form_parameters is a list of tuples, with the name of parameters and values
        self.form_parameters = []

        # Variables of call robot
        self.department = None
        self.enterprise = None
        self.robot = None

        #show dialog box 'Deseja chamar um robô ou ver os chamados?' to choose options 'Chamar' and 'Chamados'
        self.window = tk.Tk()
        self.window.title('Chamar Robôs')
        self.window.resizable(False, False)

        # Center window on screen
        # Get screen width and height
        # Calculate x and y coordinates for the Tk root window
        # Set the ange of the window
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        x = w/2 - 1000/2
        y = h/2 - 600/2
        self.window.geometry("1000x600+%d+%d" % (x, y))

        # Label 'Deseja chamar um robô ou ver os chamados?'
        self.callLabel = tk.Label(self.window, text='Deseja chamar um robô ou ver os chamados?', font=('Arial', 12), anchor='center')
        self.callLabel.pack()
        
        # Button 'Chamar', with command 'callRobot'
        self.callButton = tk.Button(self.window, text='Chamar', command=self.callRobots, font=('Arial', 12))
        self.callButton.pack()

        # margin between buttons
        self.margin= tk.Label(self.window, text='', font=('Arial', 4))
        self.margin.pack()
        
        # Button 'Chamados', with command 'showCalls'
        self.callsButton = tk.Button(self.window, text='Chamados', command=self.showCalls, font=('Arial', 12))
        self.callsButton.pack()

        # Show window
        self.window.mainloop()
    
    # Function to call robot
    def callRobots(self):
        # for each widget in window, destroy it
        for widget in self.window.winfo_children():
            widget.destroy()

        # Call to choice a department
        self.choiceDepartment()

    #function to validate if the entry is a int
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    
    #function to validade if the entry is a float
    def validateFloat(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        #if text is ',' replace by '.'
        if text == ',':
            text = '.'
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    

    # Function to choice a department, and show a gui to choice enterprise of robots on that department
    def choiceDepartment(self):
        # Empty the window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Label 'Escolha o Departamento', with anchor 'center'
        departmentLabel = tk.Label(self.window, text='Escolha o Departamento', font=('Arial', 12), anchor='center')
        departmentLabel.pack()

        # Combobox with departments, with anchor 'center'
        self.department = ttk.Combobox(self.window, values=list(departments), state='readonly', width=30, font=('Arial', 12))
        #select first value
        self.department.current(0)
        self.department.pack()

        # Button 'Escolher', with command 'choiceEnterprise'
        departmentButton = tk.Button(self.window, text='Escolher', command=self.choiceEnterprise, font=('Arial', 12),pady=10)
        departmentButton.pack()
    
    # Function to choice enterprise of robots on that department, and show a gui to choice robots on that enterprise and department
    def choiceEnterprise(self):
        # Get department
        self.department = self.department.get()

        # Empty the window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Label 'Escolha a Empresa', with anchor 'center'
        enterpriseLabel = tk.Label(self.window, text='Escolha a Empresa', font=('Arial', 12), anchor='center')
        enterpriseLabel.pack()

        #List of unique enterprises of that department
        departmentsEnterprises = robots[robots['department'] == self.department]['enterprise'].unique()

        # Combobox with enterprises, with anchor 'center'
        self.enterprise = ttk.Combobox(self.window, values=list(departmentsEnterprises), state='readonly', width=30, font=('Arial', 12))
        #select first value
        self.enterprise.current(0)
        self.enterprise.pack()

        # Button 'Escolher', with command 'choiceRobot'
        enterpriseButton = tk.Button(self.window, text='Escolher', command=self.choiceRobot, font=('Arial', 12),pady=10)
        enterpriseButton.pack()

    # Function to choice robots on that enterprise and department, and show a gui to choice robots on that enterprise and department
    def choiceRobot(self):
        # Get enterprise
        self.enterprise = self.enterprise.get()

        # Empty the window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Label 'Escolha o Robô', with anchor 'center'
        robotLabel = tk.Label(self.window, text='Escolha o Robô', font=('Arial', 12), anchor='center')
        robotLabel.pack()

        #List of unique robots of that enterprise and department
        departmentsEnterprisesRobots = robots[(robots['department'] == self.department) & (robots['enterprise'] == self.enterprise)]['name'].unique()

        # Combobox with robots, with anchor 'center'
        self.robotCombobox = ttk.Combobox(self.window, values=list(departmentsEnterprisesRobots), state='readonly', width=30, font=('Arial', 12))
        #select first value
        self.robotCombobox.current(0)
        self.robotCombobox.pack()

        # Button 'Escolher', with command 'showParameters' to show parameters of robot
        robotButton = tk.Button(self.window, text='Escolher', command=self.showParameters, font=('Arial', 12),pady=10)
        robotButton.pack()

    # Function to show parameters of robot using table 'robots_parameters', for that robot.
    def showParameters(self):
        #  Convert robots pandas dataframe to list
        robotsList = robots.to_dict('records')

        # Remove of robots array the robots that are not in the department and enterprise
        robotsList = [x for x in robotsList if x['department'] == self.department and x['enterprise'] == self.enterprise]

        # Get robot of robots with robot selected on robotCombobox
        self.robot = robotsList[self.robotCombobox.current()]

        #print position of robot
        print("Robô escolhido: " + self.robot['name'])
        print(self.robot)
        

        # Empty the window
        for widget in self.window.winfo_children():
            widget.destroy()

        # Get parameters of robot
        parameters = pd.read_sql_query("SELECT * FROM robots_parameters WHERE robot = '" + str(self.robot['id']) + "'", conn)

        if not parameters.empty:
            # For each parameter, show a label and a entry with 'default_value' and restrict the entry with 'type' (int, float, string, boolean(Sim/Não))
            for index, row in parameters.iterrows():
                # Label with parameter name
                parameterLabel = tk.Label(self.window, text=row['name'], font=('Arial', 12), anchor='center')
                parameterLabel.pack()

                # Entry with parameter value
                parameterEntry = tk.Entry(self.window, width=30, font=('Arial', 12))
                
                print('Parameter: ' + row['parameter_name'])
                print('Type: ' + row['type'])
                print('Default value: ' + str(row['default_value']))


                #If type is int
                if row['type'] == 'int':
                    #if the name is 'mes', comboBox with months
                    if row['parameter_name'] == 'mes':
                        parameterEntry = ttk.Combobox(self.window, values=list(months), state='readonly', width=30, font=('Arial', 12))
                        parameterEntry.current(int(row['default_value'])-1)
                        parameterEntry.pack()
                    #if the name is 'ano', comboBox with last 5 years until next year
                    elif row['parameter_name'] == 'ano':
                        years = [str(year) for year in range(int(row['default_value'])-5, int(row['default_value'])+2)]
                        parameterEntry = ttk.Combobox(self.window, values=list(years), state='readonly', width=30, font=('Arial', 12))
                        #select current year
                        parameterEntry.current(int(row['default_value'])-int(row['default_value'])+5)

                        parameterEntry.pack()
                    else:
                        #Restrict the entry with 'validate'
                        parameterEntry = tk.Entry(self.window, width=30, font=('Arial', 12), validate='key', validatecommand=(self.window.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
                        parameterEntry.insert(END, row['default_value'])
                        
                #if type is float
                elif row['type'] == 'float':
                    #Restrict the entry with 'validate_float'
                    parameterEntry = tk.Entry(self.window, width=30, font=('Arial', 12), validate='key', validatecommand=(self.window.register(self.validateFloat), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'))
                    #set default value
                    parameterEntry.insert(0, float(row['default_value']))
                #if type is boolean, select 'Sim' or 'Não'
                elif row['type'] == 'boolean':
                    #Combobox with 'Sim' and 'Não'
                    parameterEntry = ttk.Combobox(self.window, values=['Não', 'Sim'], state='readonly', width=30, font=('Arial', 12))
                    #select value                
                    parameterEntry.current(row['default_value'])
                #if type is string
                elif row['type'] == 'string':
                    #set default value
                    parameterEntry.insert(0, row['default_value'])
                #if type is date, DateEntry with default value
                elif row['type'] == 'date':
                    parameterEntry = DateEntry(self.window, width=30, font=('Arial', 12), date_pattern='dd/mm/yyyy', state='readonly')
                    parameterEntry.pack()
                    parameterEntry.insert(0, row['default_value'])
                #if type is select, show a combobox with options in 'default_value', and select the first option
                elif row['type'] == 'select':
                    parameterEntry = ttk.Combobox(self.window, values=list(row['default_value'].split(';')), state='readonly', width=30, font=('Arial', 12))
                    parameterEntry.current(0)
                #else type is hidden
                elif row['type'] == 'hidden':
                    parameterEntry = tk.Entry(self.window, width=30, font=('Arial', 12))
                    #set default value
                    parameterEntry.insert(0, row['default_value'])

                #if type is hidden, hide entry and label
                if row['type'] == 'hidden':
                    parameterLabel.pack_forget()
                else:
                    #pack the entry
                    parameterEntry.pack()

                #space between parameters
                tk.Label(self.window, text='', font=('Arial', 12)).pack()            
                
                # Add parameter to form_parameters with name = row['parameter_name'] and value = parameterEntry
                self.form_parameters.append((row['parameter_name'], parameterEntry))

        # Button 'Chamar', with command 'callRobot'
        callButton = tk.Button(self.window, text='Chamar', command=self.callRobot, font=('Arial', 12),pady=10)
        callButton.pack()
    
    # Function to call robot
    def callRobot(self):
        #object with parameters name and value
        parameters = {}

        # For each form_parameters, get the value of entry in value
        for parameter in self.form_parameters:
            # If the name is 'mes', get index of month in months and add to parameters
            if parameter[0] == 'mes':
                #get index of month in months with month name
                index = months.index(parameter[1].get())
                #add to parameters
                parameters[parameter[0]] = index+1
            # If the value is 'Sim' or 'Não', convert to boolean and add to parameters
            elif parameter[1].get() == 'Sim' or parameter[1].get() == 'Não':
                #convert to boolean
                parameters[parameter[0]] = parameter[1].get() == 'Sim'
            #if the value is in format 'dd/mm/yyyy', convert to sql format and add to parameters
            elif parameter[1].get() in format('dd/mm/yyyy'):
                #convert to sql format
                parameters[parameter[0]] = datetime.strptime(parameter[1].get(), '%d/%m/%Y').strftime('%Y-%m-%d')
            #else put value of entry in parameters
            else:
                parameters[parameter[0]] = parameter[1].get()

        #Convert parameters to json
        parameters = json.dumps(parameters)
        print(parameters)

        #get datetime now in sql format
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # insert into table 'calls' the robot = self.robot['id'], user, created_at, json_parameters
        sql = "INSERT INTO calls (robot, user, created_at, json_parameters) VALUES ('" + str(self.robot['id']) + "', '" + user + "', '" + now + "', '" + parameters + "')"
        conn.execute(sql)
        conn.commit()

        #show messagebox with 'Chamado realizado com sucesso'
        messagebox.showinfo('Chamado realizado com sucesso', 'Chamado realizado com sucesso')

        #show calls in window
        self.showCalls()

    # Function to show calls of robots of user
    def showCalls(self):
        #for each widget in window, destroy it
        for widget in self.window.winfo_children():
            widget.destroy()
        
        #with pandas Get  robots.name and all colls on table 'calls' all calls of user descending by created_at
        calls = pd.read_sql_query("SELECT robots.name, calls.* FROM calls INNER JOIN robots ON calls.robot = robots.id WHERE calls.user = '" + user + "' ORDER BY calls.created_at DESC", conn)

        # Label with 'Chamados'
        callsLabel = tk.Label(self.window, text='Chamados (Clique para visualizar a resposta completa)', font=('Arial', 20), anchor='center')
        callsLabel.pack()

        # Table for calls  'Robô', 'Data', 'Parâmetros', 'Status', 'Retorno', 'Visualizar'
        self.callsTable = ttk.Treeview(self.window, columns=('Robô', 'Data', 'Parâmetros', 'Status', 'Retorno'), show='headings', height=10)
        #full width of table
        self.callsTable.pack(fill='both', expand=True)

        # Header of table: 'Robô', 'Data', 'Parâmetros', 'Status', 'Retorno', 'Visualizar'
        self.callsTable.heading('Robô', text='Robô')
        self.callsTable.heading('Data', text='Data')
        self.callsTable.heading('Parâmetros', text='Parâmetros')
        self.callsTable.heading('Status', text='Status')
        self.callsTable.heading('Retorno', text='Retorno')

        # For each call, add to table
        for index, row in calls.iterrows():
            #if json_return is null, set to '-'
            if row['json_return'] == None:
                return_json = 'Nenhum Retorno'
            else:
                #extract json_return and get html
                return_json = json.loads(row['json_return'])['html']       

            #if started_at is null, set status to 'Aguardando Execução'
            if row['started_at'] == None:
                status = 'Aguardando Execução'
            #if started_at is not null, set status to 'Em Execução'
            else:
                #if eded_at is null, set status to 'Em Execução'
                if row['ended_at'] == None:
                    status = 'Em Execução'
                #if ended_at is not null, set status to 'Finalizado'
                else:
                    status = 'Finalizado'

            #for name, created_at, json_parameters and return_json, first 20 characters of value and replace '\n' with ' '
            self.callsTable.insert('', 'end', text=return_json ,values=(row['name'][:20].replace('\n', ' '), row['created_at'], row['json_parameters'][:20].replace('\n', ' '), status, return_json[:20].replace('\n', ' ')))

            #If double click on row, createHtml
            self.callsTable.bind('<Double-1>', lambda event, row=row: self.createHtml())
        
        #wait 2 seconds and show calls again
        self.window.after(2000, self.showCalls)

    # Function to create html file on desktop with return_text and open it
    def createHtml(self):
        tree_item = self.callsTable.selection()[0]
        tree_item = self.callsTable.item(tree_item)
        #get return_json
        return_json = tree_item['text']

        #get datetime now in sql format
        now = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        #file path
        file_path = os.path.expanduser('~\\Desktop\\') + tree_item['values'][0] + ' ' + now + '.html'
        
        #create html file on desktop
        with open(file_path, 'w') as f:
            f.write(return_json)

        #open html file on desktop
        webbrowser.open_new_tab(file_path)
            

    # Function to show call
    def showCall(self, call):
        print(call)
        


gui = CallRobots()
# show window
gui.window.mainloop()
