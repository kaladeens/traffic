
import time 
from pymata4 import pymata4
myBoard=pymata4.Pymata4()
gpin=6
rpin=5
buzzerpin=3
pedgpin=11
pedrpin=10
button=1
myBoard.set_pin_mode_pwm_output(pedrpin)
myBoard.set_pin_mode_pwm_output(pedgpin)
myBoard.set_pin_mode_pwm_output(gpin)
myBoard.set_pin_mode_pwm_output(rpin)
myBoard.set_pin_mode_pwm_output(buzzerpin)
myBoard.set_pin_mode_digital_input_pullup(button)


def button_state():
    output=False
    State=myBoard.digital_read(button)[0]
    if State==0:
        output=True
    return output
def make_green(rspin,gspin):
    myBoard.pwm_write(gspin,255)
    myBoard.pwm_write(rspin,0)
def make_red(rspin,gspin):
   
    myBoard.pwm_write(rspin,255)
    myBoard.pwm_write(gspin,0)
def make_yellow():
    myBoard.pwm_write(rpin,255)
    myBoard.pwm_write(gpin,60)
def buzz_green():
    for _ in range (2):
        myBoard.pwm_write(buzzerpin,150)
        time.sleep(1)
        myBoard.pwm_write(buzzerpin,50)
        time.sleep(1)
    myBoard.pwm_write(buzzerpin,0)
def buzz_red():
    for _ in range (2):
        myBoard.pwm_write(buzzerpin,175)
        time.sleep(1)
        myBoard.pwm_write(buzzerpin,0)
        time.sleep(1)
# def check_pstate():
#     myBoard.set_pin_mode_digital_input_pullup(pedgpin)
#     State=myBoard.digital_read(pedgpin)[0]
#     if State==1:
#         output=True
#     else:
#         output=False
#     myBoard.set_pin_mode_digital_output(pedgpin)
#     return output    



def initial_state():
    """"2.1.1"""
    make_red(rpin,gpin)
    make_green(pedrpin,pedgpin)
    

def no_car_coming():
    #if no car in 1 min
    
        plight_flash_red()
        initial_state()

def car_coming():
     
    # if car coming and tlight not green
        time.sleep(1)
        plight_flash_red()
def plight_flash_red():
    """2.1.2"""
    make_red(pedrpin,pedgpin)
    for _ in range(16):
        make_red(pedrpin,pedgpin)
        myBoard.pwm_write(buzzerpin,255)
        time.sleep(.1)
        myBoard.pwm_write(pedrpin,0)
        myBoard.pwm_write(buzzerpin,0)
        time.sleep(.1)
    make_red(pedrpin,pedgpin)
    buzz_red()
    time.sleep(1)
    make_green(rpin,gpin)
    time.sleep(10)
    make_yellow()
    time.sleep(3)
    initial_state()
    buzz_green()

def button_press():
    # if button_state() and if ped light is red i tried check_pstate()==True:
        time.sleep(1)
        make_yellow()
        time.sleep(3)
        make_red(rpin,gpin)
        time.sleep(3)
        initial_state()
        buzz_green()
    



def make_colour():
    myBoard.set_pin_mode_pwm_output(9)
    myBoard.pwm_write(9,100)
    myBoard.pwm_write(rpin,100)
    myBoard.pwm_write(gpin,150)


def main():
    while True:
        try:
            
            initial_state()
            car_coming()
            button_press()
            no_car_coming()
            
        except KeyboardInterrupt:
            myBoard.shutdown()
