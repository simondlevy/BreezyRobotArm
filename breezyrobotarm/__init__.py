'''
Robot Arm classes

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

class Joint(object):
    '''
    A class for controlling a single joint using a servo motor.
    '''

    def __init__(self, board, pin, start):
        '''
        Creates a new Joint object.
        board - a PyFirmata Board object
        pin   - Arduino pin to which the servo is connected
        start - initial servo angle (0 - 180 degrees)
        '''

        self.servo = board.get_pin('d:%d:s' % pin)
        self.angle = start
        self.servo.write(self.angle)

        self.target = None
        self.stepsize = None

    def setTarget(self, target):
        '''
        Sets the target angle in degrees for the joint.  Also sets the step size, determined as 2 degrees
        if the target is more than 100 degrees from the joint's current angle, 1 degree otherwise. 
        '''
        self.target = target

        # XXX need a better formula for step size, probably incorporating time
        self.stepsize = 2 if abs(target-self.angle) > 100 else 1

    def atTarget(self):
        '''
        Returns True if the joint has reached the target specified by Joint.setTarget(), false otherwise.
        '''
        return int(self.angle) >= int(self.target)

    def moveToTarget(self):
        '''
        Moves the joint toward the target specified by Joint.setTarget().
        '''
        self.angle += self.stepsize * (-1 if self.target-self.angle < 0 else +1)
        self.servo.write(self.angle)

class Arm(object):

    def __init__(self, board, pins, startAngles):
        '''
        Creates a multi-jointed robot arm.  
        board       - a PyFirmata Board object
        pins        - Arduino pins to which the arm's servos are connected
        startAngles - initial servo angles (0 - 180 degrees)
        '''
        self.joints = [Joint(board, pins[k], startAngles[k]) for k in range(len(pins))]

    def setTargets(self, targets):
        '''
        Sets the target angles in degrees for the arm's joints.  Also sets the step sizes, determined as 2 degrees
        if the target is more than 100 degrees from the joint's current angle, 1 degree otherwise. 
        '''
        for joint,target in zip(self.joints,targets):
            joint.setTarget(target)

    def atTargets(self):
        '''
        Returns True if the arm's joints have reached the targets specified by Arm.setTargets(), false otherwise.
        '''
        return all(joint.atTarget() for joint in self.joints)

    def moveToTargets(self):
        '''
        Moves the arm's joints toward the targets specified by Arm.setTargets().
        '''
        for joint in self.joints:
            joint.moveToTarget()
