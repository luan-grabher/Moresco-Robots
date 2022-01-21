import time

from InsertCalls import execute_calls

today = time.strftime("%Y-%m-%d %H:%M:%S")

#list of calls to execute
calls_to_execute = []

#array call with robot = 125, user = ti01, 'created_at' = now, json_parameters = {}
#calls_to_execute.append({'robot': 125, 'user': 'ti01', 'created_at': today, 'json_parameters': '{}'})
calls_to_execute.append({'robot': 125, 'user': 'ti01', 'created_at': '2022-01-20 12:57:21', 'json_parameters': '{}', 'id': 30})

#call with robot = 127, user = ti01, 'created_at' = now, json_parameters = {}
#calls_to_execute.append({'robot': 127, 'user': 'ti01', 'created_at': today, 'json_parameters': '{}'})

execute_calls(calls_to_execute)