# This version of program is intended to press a button (1-8) and turn on the
# coresponding led from ledbar
import mraa
import time
# these pins command rows
row = [0, 1, 2, 3]

# these pins command columns. Pin 14 is not used anythere, is just a value
# used in order to stop column 4 from oscilating
column = [4, 5, 6, 7, 14]

# matrix who contains button values
# first group of 0-7 are the buttons who get called outside the ascensor
# second group of 0-7 are the buttons who get called inside the ascensor
matrix = [[0,1,2,3],[4,5,6,7],[0,1,2,3],[4,5,6,7]]

# initialise each row pin
for i in range(len(row)):
    row[i] = mraa.Gpio(row[i])
	
# initialise each column pin
for i in range(len(column)):
    column[i] = mraa.Gpio(column[i])

# set the direction of row pins
for i in range(len(row)):
    row[i].dir(mraa.DIR_IN)

# set the direction of column pins
for i in range(len(column)):
    column[i].dir(mraa.DIR_OUT)

# activate the pull up resistors for row pins
for i in range(len(row)):
    row[i].mode(mraa.MODE_PULLUP)

# pins who control the three shift registers in series : one for showing the current floor, one who shows desired floors
# and one for lighting up the seven segment display
dataPin = mraa.Gpio(10)
clockPin = mraa.Gpio(8)
latchPin = mraa.Gpio(9)

# pins who control shift register for stepper motor
dataPinMotor = mraa.Gpio(13)
clockPinMotor = mraa.Gpio(11)
latchPinMotor = mraa.Gpio(12)

# set directions for every pins
dataPin.dir(mraa.DIR_OUT)
clockPin.dir(mraa.DIR_OUT)
latchPin.dir(mraa.DIR_OUT)

dataPinMotor.dir(mraa.DIR_OUT)
clockPinMotor.dir(mraa.DIR_OUT)
latchPinMotor.dir(mraa.DIR_OUT)




# this variable is used to deactivate the button function if is kept pressed
oldval = [0, 0, 0, 0]

# this variable is used in order to break the loop loop when a button is pressed
enableRows = False

# this array is initialised with 50, because 50 is not a value used for leds
floor = [50,50,50,50,50,50,50,50]

# elevator gets Enabled every time when a button is pressed. When current floor reach desired floor,
# this variable gets disabled
elevatorDisable = True

# when program starts, current number of floors is 0. Value 16 means 0 light on second shift register
currentFloor = 16
desiredFloor = 0
lastFloor = 0

# every time when a button is pressed, number of floors is incremented.
# When the current floor reach desired floor, the numberOfFloors gets decremented by one.
numberOfFloors = 0

# because there are 2 x 8 bit shift registers who show current floor and desired floor, 
# the maximum number to count is 2^16
state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# the 8 bit shift register, need to have data on all outputs, but only 4 of them are used by motor
motorState = [0,0,0,0,0,0,0,0]

# motor steps are 0 initially
motorSteps = 0

# motor direction is set clockwise by default
motorDirection = True

# The number of steps left. 
# 4095 means one complete rotation while 2047 means one half rotation
motorStepsLeft = 2047  #4095

# The function which makes possible motor rotation in clockwise direction
# is written below. This function is described like this:
#     0 0 0 1
#     0 0 1 1
#     0 0 1 0
#     0 1 1 0
#     0 1 0 0
#     1 1 0 0
#     1 0 0 0
#     1 0 0 1
#     0 0 0 1 - Repeat all over again
def clockwise():
    if (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[0] = 1
		
    elif (motorState[3] == 0 and  motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 1):
        motorState[1] = 1
		
    elif (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 1
            and motorState[0] == 1):
        motorState[0] = 0
		
    elif (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 1 
            and motorState[0] == 0):
        motorState[2] = 1
		
    elif (motorState[3] == 0 and motorState[2] == 1 and motorState[1] == 1 
            and motorState[0] == 0):
        motorState[1] = 0
		
    elif (motorState[3] == 0 and motorState[2] == 1 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[3] = 1
		
    elif (motorState[3] == 1 and motorState[2] == 1 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[2] = 0
		
    elif (motorState[3] == 1 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[0] = 1
		
    elif (motorState[3] == 1 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 1):
        motorState[3] = 0
		

# The function which makes possible motor rotation in anticlockwise direction
# is written below. This function is described like this:
#	  1 0 0 1
#     1 0 0 0
#     1 1 0 0
#     0 1 0 0
#     0 1 1 0
#     0 0 1 0
#     0 0 1 1
#     0 0 0 1
#     1 0 0 1 - Repeat all over again
def anticlockwise():
    if (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[3] = 1
    elif (motorState[3] == 1 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[2] = 1
    elif (motorState[3] == 1 and motorState[2] == 1 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[3] = 0
    elif (motorState[3] == 0 and motorState[2] == 1 and motorState[1] == 0 
            and motorState[0] == 0):
        motorState[1] = 1
    elif (motorState[3] == 0 and motorState[2] == 1 and motorState[1] == 1 
            and motorState[0] == 0):
        motorState[2] = 0
    elif (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 1 
            and motorState[0] == 0):
        motorState[0] = 1
    elif (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 1 
            and motorState[0] == 1):
        motorState[1] = 0
    elif (motorState[3] == 0 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 1):
        motorState[3] = 1
    elif (motorState[3] == 1 and motorState[2] == 0 and motorState[1] == 0 
            and motorState[0] == 1):
        motorState[0] = 0

# This is the function who controls the motor.
# First is a while loop who runs until steps are > than 0 or < than 0,
# depending of the motor direction.
# Because motor has only four phases, I use only first eight outputs
# of shift register.
# Each time when a condition of clockwise() function is satisfied, 
# we are incrementing the motor steps. Each time when the value of
# motor steps reach 7, we are reseting it to 0 so it work into a loop.
# Also we are decrementing motorSteps each time until are 0.
# The same way work anticlockwise() function.
	
def motorControl(motorSteps, t0, motorStepsLeft,  motorDirection):
    while motorStepsLeft > 0:
        t1 = time.time()
        if t1-t0 > 0.0003:
            latchPinMotor.write(0)
            for i in range(8):
                if i < 4:
                    dataPinMotor.write(motorState[i])
                    clockPinMotor.write(0)
                    clockPinMotor.write(1)
            latchPinMotor.write(1)

            if motorDirection:
                motorSteps += 1
                clockwise()
            elif not motorDirection:
                motorSteps -= 1
                anticlockwise()
            if motorSteps > 7:
                motorSteps = 0
            elif motorSteps < 0:
                motorSteps = 7

            motorStepsLeft -= 1
            t0 = time.time()
			

# 1000 0001

# This function is used to update the current floor ledbar like this:
# 1 0 0 0 0 0 0 0
# 0 1 0 0 0 0 0 0
# 0 0 1 0 0 0 0 0
# 0 0 0 1 0 0 0 0
# 0 0 0 0 1 0 0 0
# 0 0 0 0 0 1 0 0
# 0 0 0 0 0 0 1 0
# 0 0 0 0 0 0 0 1
def floors(digit):
    for i in range(16):
        if i > 7:
            if digit == i:
                state[i] = 1
            else:
                state[i] = 0

# dState is the seven segment display state.
dState = [0,0,0,0,0,0,0,0]

# This is the sequence where based on digit, we light up the seven
# segment display.
def sevenSegmentDisplay(digit):
    if digit == 0:  # light up 0
        dState[0] = 1
        dState[1] = 1
        dState[2] = 1
        dState[3] = 1
        dState[4] = 1
        dState[5] = 1
        dState[6] = 0
    elif digit == 1:  # light up 1
        dState[0] = 0
        dState[1] = 1
        dState[2] = 1
        dState[3] = 0
        dState[4] = 0
        dState[5] = 0
        dState[6] = 0
    elif digit == 2:  # light up 2
        dState[0] = 1
        dState[1] = 1
        dState[2] = 0
        dState[3] = 1
        dState[4] = 1
        dState[5] = 0
        dState[6] = 1
    elif digit == 3:  # light up 3
        dState[0] = 1  
        dState[1] = 1
        dState[2] = 1
        dState[3] = 1
        dState[4] = 0
        dState[5] = 0
        dState[6] = 1
    elif digit == 4:  # light up 4
        dState[0] = 0
        dState[1] = 1
        dState[2] = 1
        dState[3] = 0
        dState[4] = 0
        dState[5] = 1
        dState[6] = 1
    elif digit == 5:  # light up 5
        dState[0] = 1
        dState[1] = 0
        dState[2] = 1
        dState[3] = 1
        dState[4] = 0
        dState[5] = 1
        dState[6] = 1
    elif digit == 6:  # light up 6
        dState[0] = 1
        dState[1] = 0
        dState[2] = 1
        dState[3] = 1
        dState[4] = 1
        dState[5] = 1
        dState[6] = 1
    elif digit == 7:  # light up 7
        dState[0] = 1
        dState[1] = 1
        dState[2] = 1
        dState[3] = 0
        dState[4] = 0
        dState[5] = 0
        dState[6] = 0

# counter who goes from 8 to 15 for count up floors
countUp = 8

# counter who goes from 15 to 8 for count down floors
countDown = 15

# counter who lets user to set a number of desired floors,
# it counts from 0 to 500
timer = 0

# each desired floor is stored in this array
desiredFloorsArray = [None]

t0 = time.time()

while True:

    t1 = time.time()
    # this sequence checks if number of desired floors is >= 0,
    # and each time when current floor equals desired floor, we
    # decrement numberOfFloors and enable the elevator.
    # When the current floor equals desired floor, we wait for one second
    if numberOfFloors >= 0:
        if elevatorDisable:
            if t1-t0 > 1:
                numberOfFloors -= 1
                elevatorDisable = False
                t0 = time.time()
     
        # This sequence executes each time when elevator is enabled, and if
        # desired floors > current floors. So, if current floor == 7 and we
        # press button 7 again, nothing happens.
        if not elevatorDisable and desiredFloor > currentFloor - 16:
            # each time we take the max value from array, it will solve:
            # If we press 7, 3 or 3, 7, elevator's target is to reach
            # floor 7, but also to stop at 3.

            desiredFloor = max(desiredFloorsArray)
            if t1-t0 > 0.0003:
                timer+=1 # at each 0.0003 seconds, timer gets incremented by 1
                if timer > 500:
                    motorStepsLeft = 2047

                    # the sequence used to control the shift register
                    # range 24 means that we have 
                    latchPin.write(0)
                    for j in range(24):
                        if j < 8:
                            sevenSegmentDisplay(countUp-8)
                            dataPin.write(dState[j-8])
                        elif j > 15:
                            if countUp == floor[j-16]:
                                dataPin.write(1)
                                elevatorDisable = True
                                currentFloor = j
                                timer = 0
                                countUp -= 1
                            elif countUp <= floor[j-16]:
                                floors(countUp)
                                dataPin.write(state[j-8]) 
                            else:
                                dataPin.write(0)
                        elif j < 16 and j == floor[j-8]:  
                            dataPin.write(1)
                        else:     
                            dataPin.write(0)
                        clockPin.write(0)
                        clockPin.write(1)
                    latchPin.write(1)
                
                    if countUp == 15:
                        countUp = 8
                    else:
                        countUp = countUp + 1

                    if not elevatorDisable:
                        motorControl(motorSteps, t0, motorStepsLeft,
                            motorDirection = True)
                    else:
                        motorStepsLeft = 0
                        desiredFloorsArray.remove(min(desiredFloorsArray))
                else:
                    latchPin.write(0)
                    for j in range(24):
                        if j < 8:
                            sevenSegmentDisplay(currentFloor-16)
                            dataPin.write(dState[j-8])
                        elif j == currentFloor:
                            dataPin.write(1)
                        elif j < 16 and j == floor[j-8]:
                            dataPin.write(1)
                        else:     
                            dataPin.write(0)
                        clockPin.write(0)
                        clockPin.write(1)
                    latchPin.write(1)
                t0 = time.time()
                countDown = currentFloor - 8
				
        elif not elevatorDisable and desiredFloor < currentFloor - 16:
            desiredFloor = min(desiredFloorsArray)
            if t1-t0 > 0.0003:
                timer += 1
                if timer > 500:
                    motorStepsLeft = 2047
                    latchPin.write(0)
                    for j in range(24):
                        if j < 8:
                            sevenSegmentDisplay(countDown-8)
                            dataPin.write(dState[j-8])
                        elif j > 15:
                            if countDown == floor[j-16]:
                                dataPin.write(1)
                                elevatorDisable = True
                                currentFloor = j
                                timer = 0
                                countDown += 1
                            elif countDown < floor[j-16]:
                                floors(countDown)
                                dataPin.write(state[j-8])
                            else:
                                dataPin.write(0)
                        elif j < 16 and j == floor[j-8]:
                            dataPin.write(1)
                        else:
                            dataPin.write(0)
                        clockPin.write(0)
                        clockPin.write(1)
                    latchPin.write(1)

                    if countDown == 8:
                        countDown  = 15
                    else:
                        countDown = countDown - 1 

                    if not elevatorDisable:
                        motorControl( motorSteps, t0, motorStepsLeft,
                                motorDirection = False)
                    else:
                        motorStepsLeft = 0
                        desiredFloorsArray.remove(max(desiredFloorsArray))
                else:
                    latchPin.write(0)
                    for j in range(24):
                        if j < 8:
                            sevenSegmentDisplay(currentFloor-16)
                            dataPin.write(dState[j-8])
                        elif j == currentFloor:
                            dataPin.write(1)
                        elif j < 16 and j == floor[j-8]:
                            dataPin.write(1)
                        else:
                            dataPin.write(0)
                        clockPin.write(0)
                        clockPin.write(1)
                    latchPin.write(1)

                t0 = time.time()
                countUp = currentFloor-8
        else:
            latchPin.write(0)
            for j in range(24):
                if j < 8:
                    sevenSegmentDisplay(currentFloor-16)
                    dataPin.write(dState[j-8])
                elif j == currentFloor:
                    dataPin.write(1)
                    floor[j-16] = currentFloor
                else:
                    dataPin.write(0)
                clockPin.write(0)
                clockPin.write(1) 
            latchPin.write(1)

			
    lastFloor = desiredFloor    
    for i in range(len(column)):
        column[i].write(0) 
        column[i-1].write(1) 
        for j in range(len(row)):
            if row[j].read() == 0 and oldval[j] == 1:
                oldval[j] = 0
                enableRows = True
                del floor[matrix[j][i]] #remove the value stored at index
                floor.insert(matrix[j][i], 8+matrix[j][i]) # add value at index
                elevatorDisable = False
                desiredFloor = matrix[j][i]
                desiredFloorsArray.insert(numberOfFloors, matrix[j][i])
                if lastFloor != desiredFloor:
                    numberOfFloors += 1
                else:
                    numberOfFloors = numberOfFloors
            elif row[j].read() == 1 and oldval[j] == 0:
                oldval[j] = 1
                enableRows = False
			print("A")
        if enableRows:
            break 
		