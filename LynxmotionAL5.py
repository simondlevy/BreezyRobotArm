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
import time

from breezyrobotarm import Joint, Arm

class LynxmotionAL5(object):

    def __init__(self, board, pins=(4,5,6,7,8), startAngles=(120,180,90,0,140)):
        '''
        Creates a LynxmotionAL5 object, containing a base joint; a planar arm 
        (shoulder joint, elbow joint, wrist joint); and a gripper Joint.
        board       - a PyFirmata Board object
        pins        - Arduino pins to which the arm's servos are connected
        startAngles - initial servo angles (0 - 180 degrees)
        Pins and angles should be specified in the order: base, shoulder, elbow, wrist, gripper
        '''
        self.base     = Joint(board, pins[0], startAngles[0])
        self.arm      = Arm(board, pins[1:4], startAngles[1:4])
        self.gripper  = Joint(board, pins[4], startAngles[4])
        self.startAngles = startAngles

    def returnToStart(self):
        '''
        Returns the arm gently to its starting pose.
        '''
        self.moveTo(self.startAngles)
        
    def setTargets(self, targets):
        '''
        Sets the target angles (specified as a tuple of values 0-180) in the order: 
        base, shoulder, eblow, wrist, gripper.
        '''
        self.base.setTarget(targets[0])
        self.arm.setTargets(targets[1:4])
        self.gripper.setTarget(targets[4])

    def atTargets(self):
        '''
        Returns True if the arm's joints have reached the targets specified by LynxmotionAL5.setTargets(), 
        false otherwise.
        '''
        return self.base.atTarget() and self.arm.atTargets() and self.gripper.atTarget() 

    def stepToTargets(self):
        '''
        Move the the arm's joints one step toward the targets specified by LynxmotionAL5.setTargets().
        '''
        self.base.moveToTarget()
        self.arm.moveToTargets()
        self.gripper.moveToTarget()

    def moveTo(self, targets, delayMsec=50):
        '''
        Moves the arm's joints to smoothly to the targets specified by LynxmotionAL5.setTargets().
        delayMsec - milliseconds to pause between steps
        '''
        self.setTargets(targets)

        while True:

            if self.atTargets():
                break

            self.stepToTargets()

            time.sleep(delayMsec/1000)

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
    time.sleep(1)
    print('Returning to start')
    al5.returnToStart()

