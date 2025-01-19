import RPi.GPIO as GPIO          
from time import sleep


# motor forwards-backwrds
in1 = 24
in2 = 23

# motor clockwise-anti
in3 = 21
in4 = 22

# speed of motor
en = 25 

# motordirection
temp1=1 


# GPIO Setup 
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(en)
print("\n")
print("The default speed & direction of motor1 is LOW & Forward.....")
print("r-run s-stop fr-forward br-backward l-low m-medium h-high e-exit")
print("\n")    
print("\n")
print("The default speed & direction of motor2 is LOW & Clockwise.....")
print("r-run s-stop f2-forward b2-backward l-low m-medium h-high e-exit")
print("\n")    

while(1):

    x=input()
    # motor1 forward-backward
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)    
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)  
         print("backward")
         x='z'

    # motor-stop 
    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)  
        x='z'

    # motor forward-right fr
    elif x=='fr':
        print("forwardright")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)      
        temp1=1
        x='z'

    # motor forward-left fl
    elif x=='fl':
        print("forwardleft")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)      
        temp1=1
        x='z'

    # motor backward-left bl
    elif x=='bl':
        print("backwardleft")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)      
        temp1=0
        x='z'

    # motor backward-right br
    elif x=='br':
        print("backwardright")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.LOW)      
        temp1=0
        x='z'

    # motor forward
    elif x=='f':
        print("forward1")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        GPIO.output(in3,GPIO.HIGH)
        GPIO.output(in4,GPIO.LOW)   
        temp1=1
        x='z'

    # motor backward
    elif x=='b':
        print("forward1")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        GPIO.output(in3,GPIO.LOW)
        GPIO.output(in4,GPIO.HIGH)   
        temp1=0
        x='z' 

    # # motor-1-forward
    # elif x=='f1':
    #     print("forward1")
    #     GPIO.output(in1,GPIO.HIGH)
    #     GPIO.output(in2,GPIO.LOW)
    #     temp1=1
    #     x='z'

    # # motor-2-forward
    # elif x=='f2':
    #     print("forward2")
    #     GPIO.output(in3,GPIO.HIGH)
    #     GPIO.output(in4,GPIO.LOW)
    #     temp1=1
    #     x='z'
        
    # motor-1-backward
    # elif x=='b1':
    #     print("backward")
    #     GPIO.output(in1,GPIO.LOW)
    #     GPIO.output(in2,GPIO.HIGH)
    #     temp1=0
    #     x='z'

    # motor-2-backward
    # elif x=='b2':
    #     print("backward")
    #     GPIO.output(in1,GPIO.LOW)
    #     GPIO.output(in2,GPIO.HIGH)
    #     temp1=0
    #     x='z'
    elif x=='l':
        print("low")
        p.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("medium")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("high")
        p.ChangeDutyCycle(75)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")