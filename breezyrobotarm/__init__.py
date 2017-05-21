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

import numpy as np
import pyfirmata
from time import sleep

class Joint(object):

    def __init__(self, board, pin, start):

        self.servo = board.get_pin('d:%d:s' % pin)
        self.angle = start
        self.servo.write(self.angle)

        self.target = None
        self.stepsize = None

    def setTarget(self, target):
        self.target = target
        self.stepsize = 2 if abs(target-self.angle) > 100 else 1

    def atTarget(self):
        return int(self.angle) >= int(self.target)

    def moveToTarget(self):
        self.angle += self.stepsize*np.sign(self.target-self.angle) 
        self.servo.write(self.angle)

class Arm(object):

    def __init__(self, board, pins, starts):
        self.joints = [Joint(board, pins[k], starts[k]) for k in range(len(pins))]

    def setTargets(self, targets):
        for joint,target in zip(self.joints,targets):
            joint.setTarget(target)

    def atTargets(self):
        return all(joint.atTarget() for joint in self.joints)

    def moveToTargets(self):
        for joint in self.joints:
            joint.moveToTarget()
