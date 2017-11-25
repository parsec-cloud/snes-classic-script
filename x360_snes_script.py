import RPi.GPIO as GPIO
import math
import xbox

GPIO_SNES_DOWN  	= 23
GPIO_SNES_RIGHT    	= 22
GPIO_SNES_UP		= 27
GPIO_SNES_LEFT   	= 17
GPIO_SNES_B		= 24
GPIO_SNES_A		= 25
GPIO_SNES_X		= 04
GPIO_SNES_Y		= 18
GPIO_SNES_BACK		= 20
GPIO_SNES_START		= 21
GPIO_SNES_L_SH		= 12
GPIO_SNES_R_SH  	= 16

GPIO_SERVO_PIN 	= 010
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO.setup(GPIO_SNES_DOWN, GPIO.OUT)
GPIO.setup(GPIO_SNES_RIGHT, GPIO.OUT)
GPIO.setup(GPIO_SNES_UP, GPIO.OUT)
GPIO.setup(GPIO_SNES_LEFT, GPIO.OUT)
GPIO.setup(GPIO_SNES_B, GPIO.OUT)
GPIO.setup(GPIO_SNES_A, GPIO.OUT) 
GPIO.setup(GPIO_SNES_X, GPIO.OUT) 
GPIO.setup(GPIO_SNES_Y, GPIO.OUT) 
GPIO.setup(GPIO_SNES_BACK, GPIO.OUT)
GPIO.setup(GPIO_SNES_START, GPIO.OUT)
GPIO.setup(GPIO_SERVO_PIN, GPIO.OUT)
GPIO.setup(GPIO_SNES_L_SH, GPIO.OUT)
GPIO.setup(GPIO_SNES_R_SH, GPIO.OUT)
 
def updateServo(pwm, angle):
    duty = float(angle) / 10.0 + 2.5
    pwm.ChangeDutyCycle(duty)
 
def angleFromCoords(x,y):
    angle = 0.0
    if x==0.0 and y==0.0:
        angle = 90.0
    elif x>=0.0 and y>=0.0:
        # first quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else 90.0
    elif x<0.0 and y>=0.0:
        # second quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x<0.0 and y<0.0:
        # third quadrant
        angle = math.degrees(math.atan(y/x))
        angle += 180.0
    elif x>=0.0 and y<0.0:
        # third quadrant
        angle = math.degrees(math.atan(y/x)) if x!=0.0 else -90.0
        angle += 360.0
    return angle
 
if __name__ == '__main__':
    joy = xbox.Joystick()
    pwm = GPIO.PWM(GPIO_SERVO_PIN, 100)
    pwm.start(5)
    
    while not joy.Guide():
        
        # SNES
        snes_button_down  	= GPIO.LOW if joy.dpadDown()   	else GPIO.HIGH
        snes_button_right    	= GPIO.LOW if joy.dpadRight()  	else GPIO.HIGH
        snes_button_up 		= GPIO.LOW if joy.dpadUp()     	else GPIO.HIGH
        snes_button_left   	= GPIO.LOW if joy.dpadLeft()   	else GPIO.HIGH	
	snes_button_b	 	= GPIO.LOW if joy.B()          	else GPIO.HIGH
	snes_button_a	 	= GPIO.LOW if joy.A()          	else GPIO.HIGH
	snes_button_x	 	= GPIO.LOW if joy.X()          	else GPIO.HIGH
	snes_button_y	 	= GPIO.LOW if joy.Y()		else GPIO.HIGH
	snes_button_start 	= GPIO.LOW if joy.Start()	else GPIO.HIGH
	snes_button_back	= GPIO.LOW if joy.Back()	else GPIO.HIGH
	snes_button_l_sh	= GPIO.LOW if joy.leftBumper()	else GPIO.HIGH
	snes_button_r_sh	= GPIO.LOW if joy.rightBumper() else GPIO.HIGH
            
        GPIO.output(GPIO_SNES_DOWN, snes_button_down)
        GPIO.output(GPIO_SNES_RIGHT, snes_button_right)
        GPIO.output(GPIO_SNES_UP, snes_button_up)
        GPIO.output(GPIO_SNES_LEFT, snes_button_left)
	GPIO.output(GPIO_SNES_B, snes_button_b)
	GPIO.output(GPIO_SNES_A, snes_button_a)
	GPIO.output(GPIO_SNES_X, snes_button_x)
	GPIO.output(GPIO_SNES_Y, snes_button_y)
	GPIO.output(GPIO_SNES_START, snes_button_start)
	GPIO.output(GPIO_SNES_BACK, snes_button_back)
	GPIO.output(GPIO_SNES_L_SH, snes_button_l_sh)
	GPIO.output(GPIO_SNES_R_SH, snes_button_r_sh)

        
        # Servo
        x, y = joy.leftStick()
        angle = angleFromCoords(x,y)
        if angle > 180 and angle < 270:
            angle = 180
        elif angle >= 270:
            angle = 0
        updateServo(pwm, angle)
        
    
    joy.close()
    pwm.stop()
