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
import random

class Block(object):
    def __init__(self, name = None, movement_points = None, attack_letter = None , attack_number = None, initial_attack_strength = None, \
        allegiance = None, location = None, has_cross = False, type_men = None):
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
        if self.current_strength == 0:
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
    def __repr__(self):
        """
        prints name
        """
        return('name: ' + str(self.name))
    def __len__(self):
        return 1
    def is_dead(self):
        return self.current_strength == 0
      
class Edward(Block):
    """
    english king block
    """

    def __init__(self, name = "EDWARD", movement_points = 3, attack_letter = 'B', attack_number = 4, initial_attack_strength = 4, \
                 allegiance = 'ENGLAND', location = 23, has_cross = True):
        super(Edward, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)
class Edward2(Block):
    """
    english king block in bruce
    """
    def __init__(self, name = "EDWARD", movement_points = 3, attack_letter = 'B', attack_number = 4, initial_attack_strength = 4, \
                 allegiance = 'ENGLAND', location = 23, has_cross = True):
        super(Edward2, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)

class Wallace(Block):
    """
    wallace block
    """
    def __init__(self, name = "WALLACE", movement_points = 3, attack_letter = 'A', attack_number = 3, initial_attack_strength = 4, \
                 allegiance = 'SCOTLAND', location = 11, has_cross = True):
        super(Wallace, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)

class ScottishKing(Block):
    """
    Scottish King
    """
    def __init__(self, name = "KING", movement_points = 3, attack_letter = 'A', attack_number = 3, initial_attack_strength = 4, \
                 allegiance = 'SCOTLAND', location = 23, has_cross = True):
        super(ScottishKing, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength, \
                 allegiance, location, has_cross)


class Noble(Block):
    """
    adds extra attribute home_location on top of Block
    """
    def __init__(self, name = None, movement_points = None, attack_letter = None, attack_number = None, initial_attack_strength = None,\
                 allegiance = None, location = None, has_cross = False, home_location = None, loyalty = None):
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
            pass
        else:
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
    def __init__(self, name = None, movement_points = None, attack_letter = None, attack_number = None, initial_attack_strength = None,\
                 allegiance = None, location = None, has_cross = False, type_men = None):
        super(Celtic, self).__init__(name, movement_points, attack_letter, attack_number, initial_attack_strength,\
                         allegiance, location, has_cross, type_men)
    def check_loyalty(self):
        """
        returns true if loyal
        returns false if not and takes out all strength
        """
        if random.randint(0,2) == 0:
            self.current_strength = 0
           
            return False
        else:
            return True
