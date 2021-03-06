#!/usr/bin/python
import time
import Queue
global requestQueue

from gpio_96boards import GPIO



#This code provides PWM for two (Left and Right) motors with forward and backward capability provided by an H bridge

def buttonScannerHandler(q):
    #Pin Declarations
    GPIO_LEFT_MOTOR_FWD = GPIO.gpio_id('GPIO_A') #pin 23
    GPIO_LEFT_MOTOR_BWD = GPIO.gpio_id('GPIO_B') #pin 24
    GPIO_RIGHT_MOTOR_FWD = GPIO.gpio_id('GPIO_C') #pin 25
    GPIO_RIGHT_MOTOR_BWD = GPIO.gpio_id('GPIO_D') #pin 26

    pins = (
        (GPIO_LEFT_MOTOR_FWD, 'out'),
        (GPIO_LEFT_MOTOR_BWD, 'out'),
        (GPIO_RIGHT_MOTOR_FWD, 'out'),
        (GPIO_RIGHT_MOTOR_BWD, 'out'),
    )


    #String constants
    PAUSE = "pause"
    DRIVE_FORWARD = "forward"
    DRIVE_BACKWARD = "backward"
    TURN_RIGHT = "right"
    TURN_LEFT = "left"
    END = "end"

    #Variable to keep track of the last command
    lastPressed = PAUSE #start not moving ###############################Change this to test different input states

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
    #if __name__ == '__main__':
        #import argparse

        #parser = argparse.ArgumentParser(
            #description='PWM on GPIO A (pin 23)')
        #args = parser.parse_args()

    #Use GPIO(pins) as gpio for the code in this scope
    with GPIO(pins) as gpio:
        #While time passed is less than run time
        while (nowTime - startTime < RUN_TIME):  # lastPressed != END):
            nowTime = current_milli_time()
            if(lastPressed == PAUSE):
                gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.LOW)
                gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.LOW)
                gpio.digital_write(GPIO_LEFT_MOTOR_BWD, GPIO.LOW)
                gpio.digital_write(GPIO_RIGHT_MOTOR_BWD, GPIO.LOW)
                LOW = True
                lastTime = nowTime
                # do nothing. Wait for next drive or turn button to be pressed
            elif(lastPressed == DRIVE_FORWARD):
                # If state is high, set pins high. Check if enough time has passed.
                if (not LOW):
                    gpio.digital_write(GPIO_LEFT_MOTOR_BWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_BWD, GPIO.LOW)
                    gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.HIGH)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.HIGH)
                    if (nowTime - lastTime > HIGH_TIME):
                        lastTime = current_milli_time()
                        LOW = True
                # Else, set pins low. Check if enough time has passed. If yes, set state to High.
                else:
                    gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.LOW)
                    if (nowTime - lastTime > LOW_TIME):
                        lastTime = current_milli_time()
                        LOW = False
            elif(lastPressed == DRIVE_BACKWARD):
                # If state is high, set pins high. Check if enough time has passed.
                if (not LOW):
                    gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.LOW)
                    gpio.digital_write(GPIO_LEFT_MOTOR_BWD, GPIO.HIGH)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_BWD, GPIO.HIGH)
                    if (nowTime - lastTime > HIGH_TIME):
                        lastTime = current_milli_time()
                        LOW = True
                # Else, set pins low. Check if enough time has passed. If yes, set state to High.
                else:
                    gpio.digital_write(GPIO_LEFT_MOTOR_BWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_BWD, GPIO.LOW)
                    if (nowTime - lastTime > LOW_TIME):
                        lastTime = current_milli_time()
                        LOW = False
            elif(lastPressed == TURN_RIGHT):
                # PWM for left motor
                #If state is high, set pin high. Check if enough time has passed.
                if (not LOW):
                    gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.LOW)
                    gpio.digital_write(GPIO_LEFT_MOTOR_BWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_BWD, GPIO.LOW)
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

            elif(lastPressed == TURN_LEFT):
                # PWM for right motor
                # If state is high, set pin high. Check if enough time has passed.
                if (not LOW):
                    gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.LOW)
                    gpio.digital_write(GPIO_LEFT_MOTOR_BWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_BWD, GPIO.LOW)
                    gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.HIGH)
                    if (nowTime - lastTime > HIGH_TIME):
                        lastTime = current_milli_time()
                        LOW = True
                # Else, set pin low. Check if enough time has passed. If yes, set state to High.
                else:
                    gpio.digital_write(GPIO_RIGHT_MOTOR_FWD, GPIO.LOW)
                    if (nowTime - lastTime > LOW_TIME):
                        lastTime = current_milli_time()
                        LOW = False
            else:
                print("ButtonScannerHandler not in if statement")

            #try:
                #lastPressed = q.get() #request.form['submit'] #update the value of the last pressed button
            #except Queue.Empty:
                #do nothing
            if not q.empty():
                lastPressed = q.get()


