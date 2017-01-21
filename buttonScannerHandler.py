import time

from gpio_96boards import GPIO

GPIO_LEFT_MOTOR_FWD = GPIO.gpio_id('GPIO_A') #pin 23
GPIO_LEFT_MOTOR_BWD = GPIO.gpio_id('GPIO_B')
GPIO_RIGHT_MOTOR_FWD = GPIO.gpio_id('GPIO_C')
GPIO_RIGHT_MOTOR_BWD = GPIO.gpio_id('GPIO_D')

pins = (
    (GPIO_LEFT_MOTOR_FWD, 'out'),
    #(GPIO_LEFT_MOTOR_BWD, 'out'),
    #(GPIO_RIGHT_MOTOR_FWD, 'out'),
    #(GPIO_RIGHT_MOTOR_BWD, 'out')
)

PAUSE = "pause"
DRIVE_FORWARD = "forward"
DRIVE_BACKWARD = "backward"
TURN_RIGHT = "right"
TURN_LEFT = "left"
END = "end"

lastPressed = PAUSE #start not moving

LOW_TIME = 2 #2 millis off
HIGH_TIME = 1 #1 millis on

LOW = True #starts low. This becomes true when the PWM is supposed to be in the High state

current_milli_time = lambda: int(round(time.time() * 1000))

nowTime = current_milli_time()
lastTime = nowTime

gpio = GPIO(pins)

while(True): #lastPressed != END):
    nowTime = current_milli_time()
    #if(lastPressed == PAUSE):
        # do nothing. Wait for next drive or turn button to be pressed
    #elif(lastPressed == DRIVE_FORWARD):
        # PWM for both motors
    #elif(lastPressed == DRIVE_BACKWARD):
        # PWM for both motors
    #elif(lastPressed == TURN_RIGHT):
        # PWM for left motor
    if(not LOW):
        gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.HIGH)
        if(nowTime - lastTime > HIGH_TIME):
            lastTime = current_milli_time()
            LOW = True

    else:
        gpio.digital_write(GPIO_LEFT_MOTOR_FWD, GPIO.LOW)
        if(nowTime - lastTime > LOW_TIME):
            lastTime = current_milli_time()
            LOW = False

    #elif(lastPressed == TURN_LEFT):
        #PWM for right motor
    #else:
        #stdout error
    #lastPressed = request.form['submit'] #update the value of the last pressed button



