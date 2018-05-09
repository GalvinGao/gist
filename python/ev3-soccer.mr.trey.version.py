from ev3dev.ev3 import * 
import time
import random
 
motorLeft = LargeMotor('outB') 
motorRight = LargeMotor('outD')
mediumMotor = MediumMotor('outA') 
infSensor = InfraredSensor()
clrSensor = ColorSensor()

def moveForward():
    motorLeft.run_forever(speed_sp=-500)
    motorRight.run_forever(speed_sp=-500)

def stopMoving():
    motorLeft.stop(stop_action='hold')
    motorRight.stop(stop_action='hold')

def turnAround(rand=False):
    if(rand):
        twiddle=500*random.random()
    else:
        twiddle=0
    position = 1010+twiddle
    motorLeft.run_to_rel_pos(position_sp=position, speed_sp=-500)
    motorRight.run_to_rel_pos(position_sp=-position, speed_sp=-500)
    time.sleep(2.0)
    stopMoving()

def kick():
    turnAround()
    mediumMotor.run_forever(speed_sp=-500)
    motorLeft.run_to_rel_pos(position_sp=500, speed_sp=-500)
    motorRight.run_to_rel_pos(position_sp=500, speed_sp=-500)
    time.sleep(1.5)
    stopMoving()
    mediumMotor.stop()

def lookAtColor():
    motorLeft.run_to_rel_pos(position_sp=-500, speed_sp=-500)
    motorRight.run_to_rel_pos(position_sp=-500, speed_sp=-500)
    time.sleep(2.0)
    stopMoving()
    return clrSensor.value() 

try:
    while True:
        if int(infSensor.value()) < 22:
            stopMoving()
            color=lookAtColor()
            if color == 0:
                kick()
            else:
                turnAround(True)
            moveForward()     
        else:
            moveForward()
except KeyboardInterrupt:
    stopMoving()
    print('Robot Stopped')
