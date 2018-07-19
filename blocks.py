#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:51:35 2018

@author: elliotmoore
"""

"""
blocks class
as well as noble class
as well as Welsh
as well as norse
as well as wallace
as well as edward
as well as king
"""

import board
import blocks_occupied
class Block(object):
    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength, allegiance, location, has_cross, type_men = None):
        """
        name is name of object
        movement_points is movement points
        attack_letter is A, B, or C
        attack_number is the number after the A or B or C
        attack_strength1 is weakest attack strength or 0 
        attack_strength4 is strongest attack strength
        current_strength is current strength
        location is a Region object
        type_men is usually archers,knights, or infantry
        """
        self.name = name
        self.movement_points = movement_points
        self.attack_letter = attack_letter
        self.attack_number = attack_number
        self.attack_strength = initial_attack_strength
        self.current_strength = initial_attack_strength
        self.location = location
        self.allegiance = allegiance
        self.has_cross = has_cross
        if type_men != None:
            self.type = type_men
    def get_hurt(self, damage):
        """
        returns False if block is dead
        otherwise returns True and damages block
        """
        if self.current_strength == 1:
            return False
        else:
            self.current_strength -=1
            return True
    def heal(self, health_points):
        """
        returns False if cannot heal by that many points
        otherwise returns True and heals block
        """
        
        if self.current_strength + health_points > self.attack_strength:
            return False
        else:
            self.current_strength = self.attack_strength + health_points
            return True
    def move(self, region, block):
        """
        supposed to move block to a adjacent location and take away a movement point
        """
        pass

class Edward(Block):
    """
    english king block
    """

    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross):
        super(Edward, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)

class Wallace(Block):
    """
    wallace block
    """
    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross):
        super(Wallace, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)

class ScottishKing(Block):
    """
    Scottish King
    """
    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross):
        super(ScottishKing, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)


class Noble(Block):
    """
    adds extra attribute home_location on top of Block
    """
    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength,\
                 allegiance, location, has_cross, home_location, loyalty):
        super(Noble, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)
        self.home_location = home_location
        self.loyalty = loyalty
    def go_home(self):
        self.location = self.home_location
    def change_allegiance(self, allegiance = None):
        """
        if no allegiance passed, changes 
        allegiance is allegiance to change to
        whether it is changed or not
        """
        if self.has_cross:
            raise Exception("Moray can't change sides")
        if allegiance == None:
            if self.allegiance == 'SCOTLAND':
                self.allegiance = 'ENGLAND'
            else:
                self.allegiance == 'SCOTLAND'
        self.allegiance = allegiance


class Norse(Block):
    """
    norse block
    """
    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength,\
                 allegiance, location, has_cross):
        super(Norse, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength,\
                         allegiance, location, has_cross)
class Celtic(Block):
    """
    celtic block
    """
    def __init__(self, name, movement_points, attack_letter, attack_number, initial_attack_strength,\
                 allegiance, location, has_cross, type_men):
        super(Celtic, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength,\
                         allegiance, location, has_cross, type_men)
