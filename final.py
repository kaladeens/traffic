# Traffic Light System, created to ensure safe travelling for passengers and the vehicles on the road. It will run and react to the users input and the set functions.
# Created By : Sam, James, Will, Sebastian, Liam
# Created Date: 23/05/2022 ..etc
# version ='1.6'

import time 
from pymata4 import pymata4
myBoard=pymata4.Pymata4()

#Some Variables 
distanceCm = 2


#lists
store = [0]
digitalOutputs = [3]
digitalInputs = []
sonarValues=[time.time()]
buttonValue=[time.time()]


#pins
gPin=6
rPin=5
buzzerPin=3
pedgPin=11
pedrPin=10
button=1

for pin in digitalOutputs:
    myBoard.set_pin_mode_digital_output(pin)
for pin in digitalInputs:
    myBoard.set_pin_mode_digital_input(pin)

myBoard.set_pin_mode_pwm_output(pedrPin)
myBoard.set_pin_mode_pwm_output(pedgPin)
myBoard.set_pin_mode_pwm_output(gPin)
myBoard.set_pin_mode_pwm_output(rPin)
myBoard.set_pin_mode_pwm_output(buzzerPin)
myBoard.set_pin_mode_analog_input(button)


#functions
def sonar_callback(data):
    """helps to initialise the ultrasonic sysem
    """
    value = data[distanceCm]
    store[0] = value

def heartbeat_signal(a):
    myBoard.digital_write(3,a)

def heartbeat():
    heartbeat_signal(1)
    time.sleep(.01)
    heartbeat_signal(0)
    time.sleep(.01)


def sonar_report():
    heartbeat()
    """returns the value of the ultrasonic sensor at the current time
    """
    return store[0]


def sonar_setup(myBoard, triggerPin, echoPin):
    heartbeat()
    """initialises the sonar system
    """
    myBoard.set_pin_mode_sonar(triggerPin, echoPin, sonar_callback, timeout=200000)

    time.sleep(0.1)


def time_of_car():
    """records the time of the recording of a vehicle approaching and stores it in list."""
    heartbeat()
    if sonar_report()<55:
        sonarValues.append(time.time())
    

def button_state():
    heartbeat()
    """checks if the button has been pressed and records when this occurs
    no inputs and returns True if the button is being pressed else is false"""
    output=False
    state=myBoard.analog_read(button)[0]
    if state>800:
        output=True
        buttonValue.append(myBoard.analog_read(button)[1])
    heartbeat()
    return output


def make_green(rspin,gspin):
    heartbeat()
    """make the desired rgb green
    input a red pin and green pin to make that rgb green, returns nothing"""
    myBoard.pwm_write(gspin,255)
    myBoard.pwm_write(rspin,0)
    heartbeat()


def make_red(rspin,gspin):
    heartbeat()
    """make the desired rgb red
    input a red pin and green pin to make that rgb red, returns nothing
    """
    myBoard.pwm_write(rspin,255)
    myBoard.pwm_write(gspin,0)
    heartbeat()


def make_yellow():
    heartbeat()
    """make the traffic light yellow
    no inputs or return values"""
    myBoard.pwm_write(rPin,255)
    myBoard.pwm_write(gPin,40)
    heartbeat()


def buzz_green():
    heartbeat()
    """Create a unique sound for when the pedestrian light turns green
    no input or returns"""
    for _ in range (2):
        myBoard.pwm_write(buzzerPin,150)
        time.sleep(.2)
        myBoard.pwm_write(buzzerPin,50)
        time.sleep(.2)
    myBoard.pwm_write(buzzerPin,0)
    heartbeat()


def buzz_red():
    heartbeat()
    """Create a unique sound for when the pedestrian light turns red
    no input or returns"""
    for _ in range (2):
        myBoard.pwm_write(buzzerPin,175)
        time.sleep(.2)
        myBoard.pwm_write(buzzerPin,0)
        time.sleep(.2)
    heartbeat()


def initial_state():
    heartbeat()
    """"Runs the initial state of traffic light being red and ped light green
    returns and input are nothing"""
    make_red(rPin,gPin)
    make_green(pedrPin,pedgPin)
    

def no_car_coming():
    heartbeat()
    """Checks if a car has been detected in last 60 seconds and if not goes through the ped light flashing sequence
    """
    if time.time()-sonarValues[-1]>=60 :
        plight_flash_red()
        sonarValues.append(time.time())
        
        
def car_coming():
    heartbeat()
    """Checks if a car has been detected and if it has it goes through the ped light flashing sequence
    """
    if sonar_report()<50 and sonar_report()!=0:
        time.sleep(1)
        plight_flash_red()
        time_of_car()

        
def plight_flash_red():
    heartbeat()
    """Makes the pedestrian light red then flashes it for 3 seconds at 1Hz then 
    turns red, this is followed by the traffic lights turning green 
    then yellow befor cycling back to initial state
    """
    
    for _ in range(16):
        make_red(pedrPin,pedgPin)
        myBoard.pwm_write(buzzerPin,255)
        time.sleep(.1)
        myBoard.pwm_write(pedrPin,0)
        myBoard.pwm_write(buzzerPin,0)
        time.sleep(.1)
    make_red(pedrPin,pedgPin)
    buzz_red()
    time.sleep(1)
    t1=time.time()
    make_green(rPin,gPin)
    button_state()
    if time.time()-buttonValue[-1]<10:
        button_press()
    t2=time.time()
    while t2-t1<=10:
        button_state()
        if time.time()-buttonValue[-1]<2 or button_state()==True:
            button_press()
            return 
        else:
            t2=time.time()
    else:
        make_yellow()
        time.sleep(3)
        initial_state()
        buzz_green()

def button_press():
    heartbeat()
    """The lights sequence for when the pedestrian light has been pressed
    """
    
    make_yellow()
    time.sleep(3)
    make_red(rPin,gPin)
    time.sleep(3)
    initial_state()
    buzz_green()
    



def main():
    heartbeat()
    """Code to run the traffic lights system indefinately"""
    sonar_setup(myBoard, 13, 12)
    while True:
        try:
            
            initial_state()
            heartbeat()
            time_of_car()
            button_state()
            car_coming()
            button_state()
            heartbeat()
            no_car_coming()
        except KeyboardInterrupt:
            menu()
        


def logs ():
    initial_state ()
    print ("Pedstrian Light: Green\n")
    print ("Traffic Light: Red")


def menu():
    print ("\n\n\n\n\n\n")
    print("Traffic Light System")
    print("--------------------\n")
    print ("1: Live Logs")
    print ("2: Admin Settings")
    print ("3: Triggers ")
    print ("4: Run\n")

    while True:
        try:
            pick = int(input("Option: "))
            if pick == 1 or pick == 2 or pick == 3 or pick == 4:
                break;
            else:
                print("Error: Invalid option. Please try again.")
        except ValueError:
            print("Error: Only numbers are accepted.")
    if pick == 1:
        logs()
    elif pick == 2:
        login()
    elif pick == 3:
        triggers()
    elif pick == 4:
        main ()

def car_trigger():
    time.sleep(1)
    for _ in range(16):
        make_red(pedrPin,pedgPin)
        myBoard.pwm_write(buzzerPin,255)
        time.sleep(.1)
        myBoard.pwm_write(pedrPin,0)
        myBoard.pwm_write(buzzerPin,0)
        time.sleep(.1)
    make_red(pedrPin,pedgPin)
    buzz_red()
    time.sleep(1)
    t1=time.time()
    make_green(rPin,gPin)
    
    time.sleep(10)
    
    make_yellow()
    time.sleep(3)
    initial_state()
    buzz_green()
  



def triggers ():
    print ("Digital Triggers")
    print ("-----------------\n\n\n")
    print ("1: Trigger Car")
    print ("2: Trigger Pedestrian\n")
    print ("0: Go back")
    while True:
        try:
            pick = int(input("Option: "))
            if pick == 1 or pick == 2 or pick ==0:
                break;
            else:
                print("Error: Invalid option. Please try again.")
        except ValueError:
            print("Error: Only numbers are accepted.")
    if pick == 1:
        car_trigger()
    elif pick == 2:
        button_press()
    elif pick == 0:
        menu ()


def login():
    timer = 3 #three attempts at PIN before timeout starts
    while True: 
        pinNum = input ("Enter Pin: ")
        if pinNum == '1234':
            print ("PIN accepted\n")
            admin ()

        else:
            print ("Incorrect PIN. Please try again\n")
            timer -= 1 
            if timer <= 0:
                print ("PIN failed too many times. Timeout (2 Minutes)")
                time.sleep (120)
                login ()



def reset ():
    print ("\n\n\n\n\n\n\n\n\n")
    print ("Values Reset")
    radius.pop ()
    radius.pop ()
    radius.append("___")
    radius.append("___")
    menu ()

radius =["___", "___"]

def detectRadius():
    print ("\n\n\n")
    print (f"Current Parameters (cm): {radius}\n\n\n\n")
    print ("Change Current Parameters: ")
    while True:
        try:
            num1 = int(input("From: ")) 
            num2 = int(input("To: "))
            if num1 >= 5 and num1 <= 60 and num2 <= 60 and num2 > num1:
                print (f"Current Detection Radius (cm): [{num1},{num2}]\n\n")
                radius.pop ()
                radius.pop ()
                radius.append (num1)
                radius.append (num2)
                print ("0 : Go back\n")
                pick = int(input("Option:"))
                if pick == 0:
                    menu ()
                

                break;
            else:
                print ("\n\n\n\n\n\n\n")
                print("Entered Values Fall Outside of Paramater Range")
                admin ()
        except ValueError:
            print("Error: Only numbers are accepted.")
            if pick == 0:
                menu ()
    print ("Change Current Parameters: ")

     
    


def admin ():
    print ("\n\n\n\n\n")
    print("Admin Parameters")
    print("------------------\n")
    print ("1: Force Initial State")
    print ("2: Change Detection Radius")
    print ("3: Reset all values\n")
    print ("0: Go Back")

    while True:
        try:
            pick = int(input("Option: "))
            if pick == 1 or pick == 2 or pick == 3 or pick == 0:
                break;
            else:
                print("Error: Invalid option. Please try again.")
        except ValueError:
            print("Error: Only numbers are accepted.")
    if pick == 1:
        initial_state()
    elif pick == 2:
        detectRadius ()
    elif pick == 3:
        reset()
    elif pick == 0:
        menu ()
    elif pick == ():
        menu ()



# main()

