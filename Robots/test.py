import sys
from Robot import Robot

#Initialize Robot with call_id(first argument)
robot = Robot(sys.argv[1])

retorno = "<br><br><b>Isso é um retorno</b>"

#Set the json as the return
robot.setReturn({'html': retorno})