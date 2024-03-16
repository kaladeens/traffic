#import required modules
import time
from pymata4 import pymata4

myBoard = pymata4.Pymata4(0)

#Some Variables 
distanceCm = 2
#lists
store = [0]
digitalOutputs = []
digitalInputs = []

#pins
for pin in digitalOutputs:
    myBoard.set_pin_mode_digital_output(pin)
for pin in digitalInputs:
    myBoard.set_pin_mode_digital_input(pin)


#functions
def sonar_callback(data):
    value = data[distanceCm]
    store[0] = value

def sonar_report():
    pass
    return store

def sonar_setup(myBoard, triggerPin, echoPin):

    myBoard.set_pin_mode_sonar(triggerPin, echoPin, sonar_callback, timeout=200000)

    time.sleep(0.1)

sonar_setup(myBoard, 13, 12)

print ("test")

try:
    while True:
        print(sonar_report())   
except:
    quit
#print(sonar_report())
