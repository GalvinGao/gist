from ev3dev.ev3 import *
import time

lcd = Screen()

lcd.draw.text((5, 5), 'Robot Problem Set')
lcd.draw.text((5, 18), '  v0.2-alpha')
# Jump one line
lcd.draw.text((5, 34), 'Go Go Go, my EV3!')
# Jump one line
lcd.draw.text((5, 52), 'Oh yes! Rock it!!')
lcd.update()

#time.sleep(3)  # Let the text long enough to be seen on the screen

# print('| = ev3.Device.connected: %s' % Device.connected)

'''

Robot =====>|| Wall (Sensor)

    |
    v

Turn 180 degrees; THEN:

Go back to THE SAME SPOT

'''

'''

Two Side:
    Left: LargeMotor('outB')
    Right: LargeMotor('outD')
    
Back:
    MediumMotor('outA')

To run motor:
    run_to_rel_pos(position_sp=1100, speed_sp=900, stop_action='hold') # Big Motor One Cycle
    run_to_rel_pos(position_sp=-150, speed_sp=900, stop_action='hold') # Medium Motor 1.5 Cycle COUNTER-CLOCKWIse
    run_to_rel_pos(position_sp=150, speed_sp=900, stop_action='hold') # Medium Motor 1.5 Cycle
    
Motor Data:
    Big Motor, 1 Cycle: 1100 ticks, 24cm.

Current Method:
    start timer [a]
    at speed [b], run motor constantly (position_sp=100, loop; or, if can:
                                        run position_ap at a really high value, and stop it if sensor < 5cm.)
    if sensor < 5cm:
        stop motor;
        stop timer;
        break loop;
    then:
        make the robot turn 180 degrees,
        run motor at speed before ([b]), and time_sp=100, with the run loop times counted before. -------:::::
            mm.run_timed(time_sp=TIMER_A_RESULT, speed_sp=[b])
    done.
'''

# ===== Config ===== #

# Speed of the motor
motorSpeedConstant = -500

# Diameter of the route should be turn 180 degrees.
# Unit: centimeter (cm)
routeDiameter = 17

# When the caterpillar goes one cycle, how long does it go?
# >>> Unit: centimeter (cm)
distancePerCycle = routeDiameter * 3.14159

# When the caterpillar goes one cycle, how long does it go?
# >>> Unit: ticks (module-specified unit)
distanceUnitPerCycle = 1100

# Distance of caterpillar moved in 1 centimeter
# 1cm = ?robot distance
# tick/centimeter
ratioTickCentimeter = distanceUnitPerCycle / distancePerCycle

# The distance each motor should move.
# To alternate, a half circle.
# Unit: ticks (module-specified unit)
shouldMoveDistance = ratioTickCentimeter * distancePerCycle / 2


# ===== Main Thread ===== #

print('/ ====== [ Problem Set | Python Robot Program ]\n|')
print('| -- [ Initializing... ]\n|')

motorLeft = LargeMotor('outB')
motorRight = LargeMotor('outD')

infSensor = InfraredSensor()

notConnectedNotice = '''| -- One or more extended device(s) initiated with failure.
| \ Status:
    [
        MotorLeft - %s;
        MotorRight - %s;
        InfraredSensor - %s.
    ]'''

'''
To convert a connection status (boolean) into human readable string.

@param boolean status

@return string humanReadableText
'''


def connection_test(status):
    return 'Connected' if status else 'Not Connected'


'''
Check if all extended devices are connected correctly
'''

if motorLeft.connected is True and motorRight.connected is True and infSensor.connected is True:
    print('| -- Extended Devices Initiated Successfully.')
else:
    assert isinstance(motorLeft.connected, bool)
    assert isinstance(motorRight.connected, bool)
    assert isinstance(infSensor.connected, bool)
    print(notConnectedNotice % (
        connection_test(motorLeft.connected),
        connection_test(motorRight.connected),
        connection_test(infSensor.connected)
    ))
    raise Exception('Device not connected.')


print('| -- [ Initialized. ]')
print('| -- [ Contacting Extended Devices... ]')

startPoint = time.time()

'''
Let two motors synchronously go forward
'''

motorLeft.run_forever(speed_sp=motorSpeedConstant)
motorRight.run_forever(speed_sp=motorSpeedConstant)

print('| -- [ Running... ]')

# === GO forward UNTIL Sensor reported data smaller than 10 cm === #

recentHistory = []

while True:
    sensorData = int(infSensor.value())
    recentHistory.append(sensorData)
    if len(recentHistory) >= 5:
        print('| -- Recent Sensor Data: [%i, %i, %i, %i, %i]' % (
            recentHistory[0], recentHistory[1], recentHistory[2], recentHistory[3], recentHistory[4])
        )
        recentHistory = []
    if sensorData < 30:
        print('| -- [ Near to the Barrier (distance=%i); Stopping Motors... ]' % sensorData)
        # $ Sound.speak('Oh! A wall!')
        # Stop the motor with generic method
        motorLeft.stop(stop_action='hold')
        motorRight.stop(stop_action='hold')
        # Double confirmation for stopping the motor
        # Ref: https://sites.google.com/site/ev3python/learn_ev3_python/using-motors [Section: 'Stopping the Motors']
        motorLeft.run_forever(speed_sp=0)
        motorRight.run_forever(speed_sp=0)
        break
    #time.sleep(0.1)  # Loop too fast might cause program to lag and may drain your battery.

stopPoint = time.time()

timeDuration = int((stopPoint - startPoint) * 1000)  # time.time() returns in SECOND; convert it to MILISECOND

time.sleep(1)

# === Turn 180 degrees === #
print('| -- [ Turning 180 ]')

motorLeft.run_to_rel_pos(position_sp=1000, speed_sp=motorSpeedConstant, stop_action='hold')
motorRight.run_to_rel_pos(position_sp=-1000, speed_sp=motorSpeedConstant, stop_action='hold')

motorLeft.wait_while('running')
motorRight.wait_while('running')

motorLeft.stop(stop_action='hold')
#motorRight.stop(stop_action='hold')

time.sleep(1)

# === Reset position === #

print('| -- [ Returning to Original Position... ]')

motorLeft.run_timed(time_sp=timeDuration, speed_sp=motorSpeedConstant, stop_action='hold')
motorRight.run_timed(time_sp=timeDuration, speed_sp=motorSpeedConstant, stop_action='hold')

motorLeft.wait_while('running')
motorRight.wait_while('running')

print('| -- [ Returned. ]')
print('\ ==== [ Operation Completed. ]')

