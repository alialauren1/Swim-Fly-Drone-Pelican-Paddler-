"""!
@file motor_driver.py
    This file is a class that implements a motor driver,
    setting the duty cycle for the motor.
    It allows for initialization of the chosen motor pins and timer.
  
@author Alia Wolken, Eduardo Santos, Andrew Jwaideh
@date   2024-March-15 
"""

import pyb
import time

class motordriver:
    """!
    This class implements a motor driver from our 405 kit. 
    @author Alia Wolken, Eduardo Santos, Andrew Jwaideh
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin: enable pin
        @param in1pin: motor connected to this pin
        @param in2pin: motor connected to this pin
        @para timer: timer being used
        """
        # print ("Creating a motor driver")
        en_pin = pyb.Pin(en_pin, pyb.Pin.OUT_PP)
        en_pin.value(1)
        self.in1pin = pyb.Pin(in1pin, pyb.Pin.OUT_PP) # allows variable to be used across functions
        self.in2pin = pyb.Pin(in2pin, pyb.Pin.OUT_PP)

        tim2 = pyb.Timer(timer, freq=20000)
        self.ch1 = tim2.channel(1, pyb.Timer.PWM, pin=self.in1pin) # control motor direction
        self.ch2 = tim2.channel(2, pyb.Timer.PWM, pin=self.in2pin)


    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        # print (f"Setting duty cycle to {level}")
        # print(level)
        # if level positive
        if level > 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(level)
            
            # print("pos")
        # if level negative, make level positive, then do switch level and 0
        elif level  == 0:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)
            #print("zero")
        else:
            evel_abs = abs(level)
            # print(level)
            self.ch1.pulse_width_percent(evel_abs)
            self.ch2.pulse_width_percent(0)
            #print("negative")
            
def loop_example():
    
    # initialize button and pins needed for it
    HOT_pin = pyb.Pin(pyb.Pin.board.PB10, pyb.Pin.OUT_PP)
    LOW_pin = pyb.Pin(pyb.Pin.board.PB10, pyb.Pin.OUT_PP)
    # HOT_pin.value(1) # make it high???
    
    # do while loop where if button high or if flag is high, run motor inside loop
    
    # do while loop where while the button is say high, run motor.
    # button will not be high until pressed
    
    print("in test loop")
    moe.set_duty_cycle(70) # + to close, - to open plunger (as in pull water in)
    time.sleep(1) # 46 for whole rack
    moe.set_duty_cycle(0)
    time.sleep(1)
            
if __name__ == '__main__':
               
   # moe = motordriver (pyb.Pin.board.PC1, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    moe = motordriver (pyb.Pin.board.PB10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)
    loop_example()
            
#     while True:    
#         moe.set_duty_cycle (50)
#         time.sleep(1)

    
    # Wait for a certain duration (e.g., 5 seconds)
    # pyb.delay(5000)  # 5000 milliseconds = 5 seconds
 