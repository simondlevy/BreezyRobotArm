#!/usr/bin/python3

'''
BreezyRobotArm class and example for Lynxmotion AL5

Copyright (C) Emily Boyes, Veronika Pogrebna, Simon D. Levy 2017

This program is part of BreezyRobotArm

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http:#www.gnu.org/licenses/>.
'''

import pyfirmata
from time import sleep

from breezyrobotarm import Joint, Arm

class LynxmotionAL5(object):

    def __init__(self, board, pins=(4,5,6,7,8), starts=(120,180,90,0,140)):
        self.base     = Joint(board, pins[0], starts[0])
        self.arm      = Arm(board, pins[1:4], starts[1:4])
        self.gripper  = Joint(board, pins[4], starts[4])
        self.starts = starts

    def returnToStart(self):
        self.setTargets(self.starts)
        while True:
            if self.atTargets():
                break
            self.stepToTargets()
        
    def setTargets(self, targets):
        self.base.setTarget(targets[0])
        self.arm.setTargets(targets[1:4])
        self.gripper.setTarget(targets[4])

    def atTargets(self):

        return self.base.atTarget() and self.arm.atTargets() and self.gripper.atTarget() 

    def stepToTargets(self, delayMsec=50):

        self.base.moveToTarget()
        self.arm.moveToTargets()
        self.gripper.moveToTarget()

        # Pause a bit to avoid jerky motion
        sleep(delayMsec/1000)

    def moveTo(self, targets):

        self.setTargets(targets)

        while True:

            if self.atTargets():
                break

            self.stepToTargets()


# ====================================================================

ARDUINO_PORT = '/dev/ttyACM0'

BASE_TARGET     = 150
SHOULDER_TARGET = 80
ELBOW_TARGET    = 140
WRIST_TARGET    = 145
GRIPPER_TARGET  = 0     # open

if __name__ == '__main__':

    # Connect to the Arduino via PyFirmata
    print('Connecting to Arduino ...')
    board = pyfirmata.Arduino(ARDUINO_PORT)
    
    # start an iterator thread so serial buffer doesn't overflow
    iter8 = pyfirmata.util.Iterator(board)
    iter8.start()

    # set up arm
    al5 = LynxmotionAL5(board)

    print('Moving to target')
    al5.moveTo((BASE_TARGET, SHOULDER_TARGET, ELBOW_TARGET, WRIST_TARGET, GRIPPER_TARGET))

    # return arm to starting position
    sleep(1)
    print('Returning to start')
    al5.returnToStart()

