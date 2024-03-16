# Traffic Light System, created to ensure safe travelling for passengers and the vehicles on the road. It will run and react to the users input and the set functions.
# Created By : Sam, James, Will, Sebastian, Liam
# Created Date: 23/05/2022 ..etc
# version ='1.6'
from sre_parse import State
import time 
from pymata4 import pymata4
myBoard=pymata4.Pymata4()
gPin=6
rPin=5
buzzerPin=3
pedgPin=11
pedrPin=10
button=1

myBoard.set_pin_mode_pwm_output(pedrPin)
myBoard.set_pin_mode_pwm_output(pedgPin)
myBoard.set_pin_mode_pwm_output(gPin)
myBoard.set_pin_mode_pwm_output(rPin)
myBoard.set_pin_mode_pwm_output(buzzerPin)
myBoard.set_pin_mode_analog_input(button)
#Some Variables 
distanceCm = 2
#lists
store = [0]
digitalOutputs = []
digitalInputs = []
sonarValues=[time.time()]
buttonValue=[time.time()]
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
    return store[0]

def sonar_setup(myBoard, triggerPin, echoPin):

    myBoard.set_pin_mode_sonar(triggerPin, echoPin, sonar_callback, timeout=200000)

    time.sleep(0.1)


def time_of_car():
    if sonar_report<55:
        sonarValues.append(time.time())
    



def button_state():
    """"""
    output=False
    state=myBoard.analog_read(button)[0]
    if state>=720:
        output=True
        buttonValue.append(time.time())
    
    return output
def make_green(rspin,gspin):
    myBoard.pwm_write(gspin,255)
    myBoard.pwm_write(rspin,0)
def make_red(rspin,gspin):
   
    myBoard.pwm_write(rspin,255)
    myBoard.pwm_write(gspin,0)
def make_yellow():
    myBoard.pwm_write(rPin,255)
    myBoard.pwm_write(gPin,60)
def buzz_green():
    for _ in range (2):
        myBoard.pwm_write(buzzerPin,150)
        time.sleep(1)
        myBoard.pwm_write(buzzerPin,50)
        time.sleep(1)
    myBoard.pwm_write(buzzerPin,0)
def buzz_red():
    for _ in range (2):
        myBoard.pwm_write(buzzerPin,175)
        time.sleep(1)
        myBoard.pwm_write(buzzerPin,0)
        time.sleep(1)




def initial_state():
    """"2.1.1"""
    make_red(rPin,gPin)
    make_green(pedrPin,pedgPin)
    

def no_car_coming():
    if time.time()-sonarValues[-1]>=60 and sonarValues>60:
        plight_flash_red()
        initial_state()
    
def car_coming():
     
    if sonar_report()<40:

        time.sleep(1)
        plight_flash_red()
def plight_flash_red():
    """2.1.2"""
    make_red(pedrPin,pedgPin)
    for _ in range(16):
        make_red(pedrPin,pedgPin)
        myBoard.pwm_write(buzzerPin,255)
        time.sleep(.1)
        myBoard.pwm_write(pedrPin,0)
        myBoard.pwm_write(buzzerPin,0)
        time.sleep(.1)
    make_red(pedrPin,pedgPin)
    time.sleep(1)
    make_green(rPin,gPin)
    if time.time()-buttonValue[-1]<10:
        button_press()
    else:
        make_yellow()
        time.sleep(3)
        initial_state()
        buzz_green()

def button_press():
    
    time.sleep(1)
    make_yellow()
    time.sleep(3)
    make_red(rPin,gPin)
    time.sleep(3)
    initial_state()
    buzz_green()
    



# def make_colour():
#     myBoard.set_pin_mode_pwm_output(9)
#     myBoard.pwm_write(9,100)
#     myBoard.pwm_write(rPin,100)
#     myBoard.pwm_write(gPin,150)


def main():
    sonar_setup(myBoard, 13, 12)
    while True:
        try:
            
            initial_state()
            print(sonar_report())
            car_coming()
            print(myBoard.analog_read(button))
            no_car_coming()
            button_state()
        except KeyboardInterrupt:
            myBoard.shutdown()

main()

