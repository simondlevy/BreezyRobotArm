#!/usr/bin/python3

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
