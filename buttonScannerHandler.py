#!/usr/bin/python
import time

from gpio_96boards import GPIO

#This code is a 1:2 PWM of GPIO_A aka pin 23


#Pin Declarations
GPIO_LEFT_MOTOR_FWD = GPIO.gpio_id('GPIO_A') #pin 23
#GPIO_LEFT_MOTOR_BWD = GPIO.gpio_id('GPIO_B')
#GPIO_RIGHT_MOTOR_FWD = GPIO.gpio_id('GPIO_C')
#GPIO_RIGHT_MOTOR_BWD = GPIO.gpio_id('GPIO_D')

pins = (
    (GPIO_LEFT_MOTOR_FWD, 'out'),
    #(GPIO_LEFT_MOTOR_BWD, 'out'),
    #(GPIO_RIGHT_MOTOR_FWD, 'out'),
    #(GPIO_RIGHT_MOTOR_BWD, 'out')
)


#String constants
PAUSE = "pause"
DRIVE_FORWARD = "forward"
DRIVE_BACKWARD = "backward"
TURN_RIGHT = "right"
TURN_LEFT = "left"
END = "end"

#Variable to keep track of the last command
lastPressed = PAUSE #start not moving

#PWM low and high time constants. Also how long the code should run for
LOW_TIME = 2 #2 millis off
HIGH_TIME = 1 #1 millis on
RUN_TIME = 25000 #25 sec

#Keeps track of what state the pin should be in
LOW = True #starts low. This becomes true when the PWM is supposed to be in the High state

#Method gets the current time in millis
current_milli_time = lambda: int(round(time.time() * 1000))

#Initialize start times
startTime = current_milli_time()
nowTime = startTime
lastTime = nowTime

#Main
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='PWM on GPIO A (pin 23)')
    args = parser.parse_args()

    #Use GPIO(pins) as gpio for the code in this scope
    with GPIO(pins) as gpio:
        #While time passed is less than run time
        while (nowTime - startTime < RUN_TIME):  # lastPressed != END):
            nowTime = current_milli_time()
            # if(lastPressed == PAUSE):
            # do nothing. Wait for next drive or turn button to be pressed
            # elif(lastPressed == DRIVE_FORWARD):
            # PWM for both motors
            # elif(lastPressed == DRIVE_BACKWARD):
            # PWM for both motors
            # elif(lastPressed == TURN_RIGHT):
            # PWM for left motor

            #If state is high, set pin high. Check if enough time has passed.
            if (not LOW):
                gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.HIGH)
                if (nowTime - lastTime > HIGH_TIME):
                    lastTime = current_milli_time()
                    LOW = True
            #Else, set pin low. Check if enough time has passed. If yes, set state to High.
            else:
                gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.LOW)
                if (nowTime - lastTime > LOW_TIME):
                    lastTime = current_milli_time()
                    LOW = False

                    # elif(lastPressed == TURN_LEFT):
                    # PWM for right motor
                    # else:
                    # stdout error
                    # lastPressed = request.form['submit'] #update the value of the last pressed button

