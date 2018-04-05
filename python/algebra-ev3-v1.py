from ev3dev.ev3 import *
import time

# print("| = ev3.Device.connected: %s" % Device.connected)

'''

Robot =====>>>

>>>>|| Wall (Sensor)

	|
	v

Turn 180 degree

Go back to THE SAME SPOT

'''

'''

Two Side:
	Left: LargeMotor('outB')
	Right: LargeMotor('outD')
	
Back:
	MediumMotor('outA')

To run motor:
	run_to_rel_pos(position_sp=1100, speed_sp=900, stop_action="hold") # Big Motor One Cycle
	run_to_rel_pos(position_sp=-150, speed_sp=900, stop_action="hold") # Medium Motor 1.5 Cycle COUNTER-CLOCKWIse
	run_to_rel_pos(position_sp=150, speed_sp=900, stop_action="hold") # Medium Motor 1.5 Cycle

Current Method:
	start timer [a]
	at speed [b], run motor constantly (position_sp=100,loop; or, if can, run position_ap at a really high value, and stop it if sensor < 5cm.)
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

motorspeed = 500

i = 0

print('/ ====== [ Problem Set | Robot Python Program ]\n|\n|')
print('| -- [ Initializing... ]\n|')

mleft = LargeMotor('outB')
mright = LargeMotor('outD')

infsensor = InfraredSensor()

if mleft.connected == True and mright.connected == True and infsensor.connected == True:
	print('| -- Extended Devices Initiated Successfully.')
else:
	print('| -- One or more extended device(s) initiated with failure.\n| \ Status:\n    [\n      MotorLeft - %s;\n      MotorRight - %s;\n      InfraredSensor - %s.\n    ]' % ("Connected" if mleft.connected else "Not Connected", "Connected" if mright.connected else "Not Connected", "Connected" if infsensor.connected else "Not Connected"))
	raise IOError("Device not connected.")

print('| -- [ Initialized. ]')
print('| -- [ Contacting Extended Devices... ]')

startpoint = time.time()

mleft.run_forever(speed_sp=motorspeed)
mright.run_forever(speed_sp=motorspeed)

print('| -- [ Running... ]')

# === GO forward UNTIL Sensor reported data smaller than 5 cm === #

recenthistory = []

while True:
	val = infsensor.value
	recenthistory.append(val)
	if len(recenthistory) >= 5:
		print("| -- Recent Sensor Data: [%i, %i, %i, %i, %i]" % (recenthistory[0], recenthistory[1], recenthistory[2], recenthistory[3], recenthistory[4]))
		recenthistory = []
	if val < 10:
		mleft.stop(stop_action="hold")
		mright.stop(stop_action="hold")
		print('| -- [ Near to the Barrier (distance=%i); Stopping Motors... ]' % val)
		mleft.run_forever(speed_sp=0)
		mright.run_forever(speed_sp=0)
		break;

stoppoint = time.time()

timeduration = int((stoppoint - startpoint) * 1000) # time.time() returns in SECOND format; convert to MILISECOND format.

# === Backward === #

print('| -- [ Returning to Original Position... ]')

mleft.run_timed(time_sp=timeduration, speed_sp=-motorspeed, stop_action="hold")
mright.run_timed(time_sp=timeduration, speed_sp=-motorspeed, stop_action="hold")

mleft.wait_while('running')
mright.wait_while('running')

print('| -- [ Returned. ]')
print('\ ==== [ Operation Completed. ]')
