'''
    A gui to manage the robots, Add or Edit.
'''

# Import the libraries
import os
import sqlite3
from sqlite3.dbapi2 import Cursor
from tkinter.constants import END
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import StringVar
from tkinter import IntVar
from tkinter import BooleanVar
from tkinter import Tk
from tkinter import Label
from tkinter import Entry
from tkinter import Button
import datetime

# Import the config file
import configparser
config = configparser.ConfigParser()
print(config.read("../moresco-robots.ini"))

# Get the list of robots with sqlite3 database on config 'database.path'
conn = sqlite3.connect(config['database']['path'])
# Get the list of robots
robots = pd.read_sql_query("SELECT * FROM robots", conn)
#List with unique enterprises
enterprises = list(robots['enterprise'].unique())
# List with departments - Nenhum, Contábil, Fiscal ou Pessoal
departments = ['Nenhum', 'Contábil', 'Fiscal', 'Pessoal']
    
# Add an robot
def add_robot():

    #Change gui name to 'Adicionar Robô'
    gui.title('Adicionar Robô')

    #Empty the gui
    for widget in gui.winfo_children():
        widget.destroy()
    
    #Input 'Nome do Robô' with anchor 'center'
    Label(gui, text='Nome do Robô:').pack(anchor='center')
    name = Entry(gui)
    name.pack(anchor='center', fill='x', padx=50, pady=10)
    #set width of the input to 50% of the gui

    #Input 'Caminho do Robô' with anchor 'center'
    Label(gui, text='Caminho do Robô:').pack(anchor='center')
    path = Entry(gui)
    path.pack(anchor='center', fill='x', padx=50, pady=10)
    #Set path value to selected file
    path.insert(0, filedialog.askopenfilename(initialdir = os.getcwd(), title = "Selecione o arquivo", filetypes = (("all files","*.*"),("Python","*.py"),("Java","*.jar"))))
    
    #Text Input 'Descrição do Robô' with anchor 'center' and height of 10
    Label(gui, text='Descrição do Robô:').pack(anchor='center')
    description = scrolledtext.ScrolledText(gui, height=3)
    description.pack(anchor='center', fill='x', padx=50, pady=10)

    #Input 'Departamento' with anchor 'center', list of departments or 'Nenhum', block to add a new department
    Label(gui, text='Departamento:').pack(anchor='center')
    department = ttk.Combobox(gui, values=departments, state='readonly')
    department.pack(anchor='center', fill='x', padx=50, pady=10)
    department.current(0)

    #Input 'Empresa' with anchor 'center', list of enterprises or able to add a new enterprise
    Label(gui, text='Empresa:').pack(anchor='center')
    enterprise = ttk.Combobox(gui, values=enterprises)
    enterprise.pack(anchor='center', fill='x', padx=50, pady=10)

    #Botão 'Salvar' with anchor 'center', command to save the robot
    Button(gui, text='Salvar', command=lambda: save_robot(name.get(), path.get(), description.get("1.0",'end-1c'), department.get(), enterprise.get())).pack(anchor='center', fill='x', padx=50, pady=10)

#Function to save the robot with the values of the inputs
def save_robot(name, path, description, department, enterprise):
    #Create sql query to save the robot
    sql = "INSERT INTO robots (name, path, description, department, enterprise) VALUES ('" + name + "', '" + path + "', '" + description + "', '" + department + "', '" + enterprise + "')"
    #Execute the query
    conn.execute(sql)

    #Get the id of the robot saved by name, path and enterprise with query
    sql = "SELECT id FROM robots WHERE name = '" + name + "' AND path = '" + path + "' AND enterprise = '" + enterprise + "'"
    #With pandas, get the id of the robot
    id = pd.read_sql_query(sql, conn)['id'].values[0]

    #Parameter to save the robot
    #month and year now
    month = int(str(datetime.datetime.now().month))
    year = int(str(datetime.datetime.now().year))

    params = []
    #parameter with name='Mês', 'type'='int', 'default_value'= month, parameter_name='mes', robot=id
    params.append({'name':'Mês', 'type':'int', 'default_value': str(month), 'parameter_name':'mes', 'robot':str(id)})
    #parameter with name='Ano', 'type'='int', 'default_value'= year, parameter_name='ano', robot=id
    params.append({'name':'Ano', 'type':'int', 'default_value': str(year), 'parameter_name':'ano', 'robot':str(id)})
    #parameter with name='Ini', 'type'='string', 'default_value'= 'ini.ini', parameter_name='ini', robot=id
    params.append({'name':'Ini', 'type':'string', 'default_value': 'ini.ini', 'parameter_name':'ini', 'robot':str(id)})

    #Add robots_parameters table with the id of the robot saved, and the parameters
    for param in params:
        #Create sql query to save the robot parameters
        sql = "INSERT INTO robots_parameters (robot, name, parameter_name , type, default_value) VALUES ('" + param['robot'] + "', '"+ param['name'] + "', '" + param['parameter_name'] + "', '" + param['type'] + "', '" + param['default_value'] + "')"
        #Execute the query
        conn.execute(sql)

    #Commit the changes
    conn.commit()
    #Close the connection
    conn.close()
    #Show a message to the user
    messagebox.showinfo('Robô salvo', 'Robô salvo com sucesso!')
    #Close program
    gui.destroy()

#Edit an robot
def edit_robot():
    '''
        * Edit an robot
            - show a gui with the select input with departments
            - after select a department, show a gui with the select input with enterprises that robots of the department
            - after select an enterprise, show a gui with the select input with robots of the enterprise and department selected
            - after select a robot, show a gui with the deailts of the robot - name, path, description, etc.
            - on click on the button 'save', save the robot selected
    '''

    #Change gui name to 'Editar Robô'
    gui.title('Editar Robô')

    #Empty the gui
    for widget in gui.winfo_children():
        widget.destroy()

    #List of departments on the database
    db_departments = pd.read_sql_query("SELECT DISTINCT department FROM robots", conn)['department'].values
    
    #Input 'Departamento' with anchor 'center', list of departments or 'Nenhum', block to add a new department
    Label(gui, text='Departamento:').pack(anchor='center')
    department = ttk.Combobox(gui, values=list(db_departments), state='readonly')
    department.pack(anchor='center', fill='x', padx=50, pady=10)
    department.current(0)

    #On select a department, get the enterprises of the robots that are in the department
    department.bind("<<ComboboxSelected>>", lambda event: get_enterprises(department.get()))

    #function to get the enterprises of the robots that are in the department
    def get_enterprises(department):
        #Get the enterprises of the robots that are in the department
        sql = "SELECT DISTINCT enterprise FROM robots WHERE department = '" + department + "'"
        #With pandas, get the enterprises of the robots that are in the department
        enterprises = pd.read_sql_query(sql, conn)['enterprise'].values
        
        #Empty the gui
        for widget in gui.winfo_children():
            widget.destroy()
        
        #Input 'Empresa' with anchor 'center', list of enterprises
        Label(gui, text='Empresa:').pack(anchor='center')
        enterprise = ttk.Combobox(gui, values=list(enterprises), state='readonly')
        enterprise.pack(anchor='center', fill='x', padx=50, pady=10)

        #On select a enterprise, get the robots of the enterprise and department selected
        enterprise.bind("<<ComboboxSelected>>", lambda event: get_robots(department, enterprise.get()))

        #function to get the robots of the enterprise and department selected
        def get_robots(department, enterprise):
            #Get the robots of the enterprise and department selected
            sql = "SELECT * FROM robots WHERE department = '" + department + "' AND enterprise = '" + enterprise + "'"
            #With pandas, get the robots of the enterprise and department selected
            robots = pd.read_sql_query(sql, conn)

            #Empty the gui
            for widget in gui.winfo_children():
                widget.destroy()
            
            #Input 'Robô' with anchor 'center', list of robots or able to add a new robot
            Label(gui, text='Robô:').pack(anchor='center')
            robot = ttk.Combobox(gui, values=list(robots['name'].values), state='readonly')
            robot.pack(anchor='center', fill='x', padx=50, pady=10)

            #On select a robot, show the details of the robot with index of the robot selected
            robot.bind("<<ComboboxSelected>>", lambda event: show_robot(robots.iloc[robot.current()]))

            #function to show the details of the robot
            def show_robot(robot):
                #Change gui name to 'Editar Robô'
                gui.title('Editar Robô')

                #get the robot updated on the database by this id
                sql = "SELECT * FROM robots WHERE id = '" + str(robot['id']) + "'"
                #With pandas, get the robot updated on the database by this id
                robot = pd.read_sql_query(sql, conn)
                robot = robot.iloc[0]                               

                #Empty the gui
                for widget in gui.winfo_children():
                    widget.destroy()

                #Input 'Nome' with anchor 'center', name of the robot
                Label(gui, text='Nome:').pack(anchor='center')
                name = Entry(gui, width=30)
                name.pack(anchor='center', fill='x', padx=50, pady=10)
                name.insert(0, robot['name'])

                #Input 'Caminho' with anchor 'center', path of the robot
                Label(gui, text='Caminho:').pack(anchor='center')
                path = Entry(gui, width=30)
                path.pack(anchor='center', fill='x', padx=50, pady=10)
                path.insert(0, robot['path'])

                #Button 'Escolher' with anchor 'center', open a file dialog to select the path to robot
                Button(gui, text='Escolher Caminho', command=lambda: select_path(path)).pack(anchor='center', fill='x', padx=50, pady=10)

                #function to select the path to robot
                def select_path(path):
                    #Open a file dialog to select the path to robot
                    path.delete(0, END)
                    path.insert(0, filedialog.askopenfilename(initialdir = "/",title = "Selecionar Arquivo",filetypes = (("all files","*.*"),("python files","*.py"))))

                #Input 'Descrição' with anchor 'center', description of the robot
                Label(gui, text='Descrição:').pack(anchor='center')
                description = Entry(gui, width=30)
                description.pack(anchor='center', fill='x', padx=50, pady=10)
                description.insert(0, robot['description'])

                #Button 'Atualizar' with anchor 'center', update the robot
                Button(gui, text='Atualizar', command=lambda: update_robot(name.get(), path.get(), description.get(), robot['id'])).pack(anchor='center', fill='x', padx=50, pady=10)

                #function to update the robot
                def update_robot(name, path, description, id):
                    #Update the robot
                    sql = "UPDATE robots SET name = '" + name + "', path = '" + path + "', description = '" + description + "' WHERE id = " + str(id)
                    conn.execute(sql)
                    conn.commit()

                    #Show a message to the user
                    messagebox.showinfo('Robô atualizado', 'Robô atualizado com sucesso!')

                    #Recall the function to show the details of the robot
                    show_robot(robot)

                #Button 'Editar Parametros' with anchor 'center', open the gui to edit the parameters of the robot
                Button(gui, text='Editar Parametros', command=lambda: edit_parameters(robot['id'])).pack(anchor='center', fill='x', padx=50, pady=10)

                #function to edit the parameters of the robot
                def edit_parameters(robot_id):
                    #create a new gui
                    gui_parameters = Tk()
                    gui_parameters.title('Editar Parametros')

                    #Set size of the gui to 500x500
                    gui_parameters.geometry('500x500')                    

                    #Get the parameters of the robot on the database table 'robot_parameters' with the collumn 'robot' equal to the robot selected
                    sql = "SELECT * FROM robots_parameters WHERE robot = " + str(robot_id)
                    parameters = pd.read_sql_query(sql, conn)

                    #List of parameters, when the user click on a parameter, the gui will open to edit the parameter
                    for i in range(len(parameters)):
                        #Input 'Parametro' with anchor 'center', name of the parameter
                        Label(gui_parameters, text=parameters.iloc[i]['name']).pack(anchor='center')
                        #Button 'Editar' with anchor 'center', open a new gui to edit the parameter
                        Button(gui_parameters, text='Editar', command=lambda: edit_parameter(parameters.iloc[i])).pack(anchor='center', fill='x', padx=50, pady=10)

                    #button 'Adicionar outro' with anchor 'center', open a new gui to add a new parameter
                    Button(gui_parameters, text='Adicionar outro', command=lambda: add_parameter(robot_id)).pack(anchor='center', fill='x', padx=50, pady=10)

                    #function to add a new parameter with name, type ('int', 'float', 'string', 'boolean'), parameter_name and default_value
                    def add_parameter(robot_id):
                        #create a new gui
                        gui_add_parameter = Tk()
                        gui_add_parameter.title('Adicionar Parametro')

                        #Input 'Nome' with anchor 'center', name of the parameter
                        Label(gui_add_parameter, text='Nome Exibido:').pack(anchor='center')
                        name = Entry(gui_add_parameter, width=30)
                        name.pack(anchor='center', fill='x', padx=50, pady=10)

                        #Input 'Tipo' with anchor 'center', type of the parameter
                        Label(gui_add_parameter, text='Tipo:').pack(anchor='center')
                        type = ttk.Combobox(gui_add_parameter, values=['int', 'float', 'string', 'boolean'], state='readonly')
                        type.pack(anchor='center', fill='x', padx=50, pady=10)

                        #Input 'Nome do Parametro' with anchor 'center', parameter_name of the parameter
                        Label(gui_add_parameter, text='Nome do Parametro:').pack(anchor='center')
                        parameter_name = Entry(gui_add_parameter, width=30)
                        parameter_name.pack(anchor='center', fill='x', padx=50, pady=10)

                        #Input 'Valor Padrão' with anchor 'center', default_value of the parameter
                        Label(gui_add_parameter, text='Valor Padrão:').pack(anchor='center')
                        default_value = Entry(gui_add_parameter, width=30)
                        default_value.pack(anchor='center', fill='x', padx=50, pady=10)

                        #Button 'Adicionar' with anchor 'center', add the parameter to the database
                        Button(gui_add_parameter, text='Adicionar', command=lambda: add_parameter_to_database(name.get(), type.get(), parameter_name.get(), default_value.get(), robot_id)).pack(anchor='center', fill='x', padx=50, pady=10)

                        #function to add the parameter to the database
                        def add_parameter_to_database(name, type, parameter_name, default_value, robot_id):
                            #Insert the new parameter to the database
                            sql = "INSERT INTO robots_parameters (name, type, parameter_name, default_value, robot) VALUES ('" + name + "', '" + type + "', '" + parameter_name + "', '" + default_value + "', " + str(robot_id) + ")"
                            conn.execute(sql)
                            conn.commit()

                            #close the gui
                            gui_add_parameter.destroy()

                            #destroy the gui of the parameters
                            gui_parameters.destroy()

                            #Recall the function to show the parameters of the robot
                            edit_parameters(robot_id)

                    
                    #function to edit the parameter name, type, parameter_name and default_value
                    def edit_parameter(parameter):
                        #create a new gui
                        gui_parameter = Tk()
                        gui_parameter.title('Editar Parametro')

                        #Input 'Nome Exibido' with anchor 'center', name of the parameter
                        Label(gui_parameter, text='Nome Exibido:').pack(anchor='center')
                        name = Entry(gui_parameter, width=30)
                        name.pack(anchor='center', fill='x', padx=50, pady=10)
                        name.insert(0, parameter['name'])

                        #Input 'Tipo' with anchor 'center', type of the parameter -> int, float, string, boolean
                        Label(gui_parameter, text='Tipo:').pack(anchor='center')
                        type = ttk.Combobox(gui_parameter, values=['int', 'float', 'string', 'boolean'], state='readonly')
                        type.pack(anchor='center', fill='x', padx=50, pady=10)
                        type.set(parameter['type'])

                        #Input 'Nome do Parametro' with anchor 'center', name of the parameter
                        Label(gui_parameter, text='Nome do Parametro:').pack(anchor='center')
                        parameter_name = Entry(gui_parameter, width=30)
                        parameter_name.pack(anchor='center', fill='x', padx=50, pady=10)
                        parameter_name.insert(0, parameter['parameter_name'])

                        #Input 'Valor Padrão' with anchor 'center', default value of the parameter
                        Label(gui_parameter, text='Valor Padrão:').pack(anchor='center')
                        default_value = Entry(gui_parameter, width=30)
                        default_value.pack(anchor='center', fill='x', padx=50, pady=10)
                        default_value.insert(0, parameter['default_value'])

                        #Button 'Atualizar' with anchor 'center', update the parameter
                        Button(gui_parameter, text='Atualizar', command=lambda: update_parameter(name.get(), type.get(), parameter_name.get(), default_value.get(), parameter['id'])).pack(anchor='center', fill='x', padx=50, pady=10)

                        #function to update the parameter
                        def update_parameter(name, type, parameter_name, default_value, id):
                            #Update the parameter
                            sql = "UPDATE robots_parameters SET name = '" + name + "', type = '" + type + "', parameter_name = '" + parameter_name + "', default_value = '" + default_value + "' WHERE id = " + str(id)
                            conn.execute(sql)
                            conn.commit()

                            #Show a message to the user
                            messagebox.showinfo('Parametro atualizado', 'Parametro atualizado com sucesso!')

                            #Close edit parameter gui
                            gui_parameter.destroy()

                            #Recall the function to edit the parameters to update the gui
                            edit_parameters(robot_id)

# Create a gui with buttons 'Adicionar' and 'Editar'
gui = tk.Tk()
gui.title('Gerenciador de Robots')
gui.geometry('500x500')
gui.configure(background='#FFFFFF')
gui.option_add('*Font', 'Helvetica 12')

#Center the window on the screen
w = gui.winfo_screenwidth()
h = gui.winfo_screenheight()
size = '%dx%d+%d+%d' % (500, 500, (w/2)-250, (h/2)-250)
gui.geometry(size)


# Button 'Adicionar' centered with width
add_button = Button(gui, text='Adicionar', command=add_robot)
add_button.pack(side='top', padx=10, pady=10)

# Button 'Editar' centered with width
edit_button = Button(gui, text='Editar', command=edit_robot)
edit_button.pack(side='top', padx=10, pady=10)


#Show the gui
gui.mainloop()