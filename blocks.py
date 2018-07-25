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


class Block(object):
    def __init__(self, name = None, movement_points = None, attack_letter = None , attack_number = None, initial_attack_strength = None, \
        allegiance = None, location = None, has_cross = False, type_men = None, block_ID = None):
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
        self.blockID = blockID
        
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
            self.current_strength -= 1
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
 

class Noble(Block):
    """
    adds extra attribute home_location on top of Block
    """
    
    def __init__(self, name = None, movement_points = None, attack_letter = None, attack_number = None, max_attack_strength = None,\
                 has_cross = None, block_ID = None, home_location = None, loyalty = None, allegiance = None):

        super(Noble, self).__init__(name, movement_points, attack_letter, attack_number, max_attack_strength, \
                 has_cross, block_ID, allegiance)

        #self.home_location = home_location
        self.loyalty = loyalty
       
    #def go_home(self):
        #self.location = self.home_location
        
    def change_allegiance(self, allegiance = None):
        """
        No parameter: flips noble's alliegance
        Parameter ('SCOTLAND' or 'ENGLAND'): sets alliegance to that side
        """
        if self.has_cross:
            raise Exception('Moray can\'t change sides')
        else:
            if allegiance == None:
                if self.allegiance == 'SCOTLAND':
                    self.allegiance = 'ENGLAND'
                    print('changed from SCOTLAND to ENGLAND')
                else:
                    self.allegiance == 'SCOTLAND'
                    print('changed from ENGLAND to SCOTLAND')
            else:
                self.allegiance = allegiance

    def home_territory(self):
        """
        changes dude from B2 to B3 and back
        """
        if self.attack_number == 2:
            self.attack_number = 3
        else:
            self.attack_number = 2