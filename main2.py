#Developed by Hiep Ban - 15 May 2025

from machine import Pin
from servo import Servo
import time

Button1 = Pin(10,Pin.IN,Pin.PULL_UP)
Button2 = Pin(11,Pin.IN,Pin.PULL_UP)
Button3 = Pin(12,Pin.IN,Pin.PULL_UP)
base_servo = Servo(pin=13)
arm1_servo = Servo(pin=14)
arm2_servo = Servo(pin=15)

ServoMoveArr = [base_servo.move, arm1_servo.move, arm2_servo.move] #array of functions that move the servos
ServoAngleArr = [0, 90, 90] #array of angles of servo base, arm 1, and arm 2

def resetPos(): #reset to default position
    ServoMoveArr[0](0)
    ServoMoveArr[1](90)
    ServoMoveArr[2](90)
    
resetPos()

def RecordMove(): #record movement with number as input
    resetPos()
    array = [0] * 50
    MoveCount = int(0) #count the number of moves made
    jump = int(0) #index 0, 2, 4 will be servo number, index 1, 3, 5 will be angle
    
    while True: #record each movement stage
        array[0+jump] = int(input('Servo: ')) #select servo
        if array[0+jump] == 4: break
            
        while True:
            if Button1.value() == 0: #check if movement recording is done
                break
            elif Button2.value() == 0: #press button to move servo -2 degree
                ServoAngleArr[array[0+jump]-1] -= 2 #angle array is update
                ServoMoveArr[array[0+jump]-1](ServoAngleArr[array[0+jump]-1]) #servo move function array is updated
            elif Button3.value() == 0: #press button to move servo +2 degree
                ServoAngleArr[array[0+jump]-1] += 2
                ServoMoveArr[array[0+jump]-1](ServoAngleArr[array[0+jump]-1])
            
            if ServoAngleArr[array[0+jump]-1] < 0: ServoAngleArr[array[0+jump]-1] = 0
            if ServoAngleArr[array[0+jump]-1] > 180: ServoAngleArr[array[0+jump]-1] = 180 #prevent angle from going < 0 or > 180
            
            array[1+jump] = ServoAngleArr[array[0+jump]-1] #make the array record the current angle
            time.sleep(0.02)
            
        jump += 2
        MoveCount += 1
    return array, MoveCount
    
def PlayMove(arr_input, MoveStage): #play movement
    jump = int(0)
    
    for i in range(MoveStage): #play the servo consequentially
        ServoMoveArr[arr_input[0+jump]-1](arr_input[1+jump])
        jump += 2
        time.sleep(1)
     
while True:
    checkFunc = input('Record or Replay?: ')
    if checkFunc == 'record':
        array, MoveCount = RecordMove()
    if checkFunc == 'replay':
        resetPos()
        ReplayNumb = int(input('How many times? '))
        time.sleep(0.5)
        print('Replaying...')
        for i in range(ReplayNumb):
            PlayMove(array, MoveCount)
            time.sleep(0.5)
        print('Replaying Complete')