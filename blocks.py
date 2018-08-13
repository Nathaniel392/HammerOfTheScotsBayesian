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
        has_cross = False, type_men = None, blockID = None, allegiance = None):
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
        self.allegiance = allegiance
        self.has_cross = has_cross
        self.blockID = blockID
        
        
        self.type = type_men

    def get_hurt(self, damage):
        """
        returns False if block is dead
        otherwise returns True and damages block
        """
        if self.current_strength == 0:
            return False
        else:
            self.current_strength -= damage
            if self.current_strength < 0:
                self.current_strength = 0
            return True
          
    
    def heal_until_full(self, health_points = 1):
        """
        heals block until full
        """
        self.current_strength += health_points
        if self.current_strength > self.attack_strength:
            self.current_strength = self.attack_strength
        return health_points

    def __str__(self):
        '''
        Returns a string representing the block
        '''
        output = '-'*20 + '\n'

        output += self.name + ' - '
        if type(self) == Noble:
            output += self.loyalty
        else:
            output += self.type

        if self.has_cross:
            output += ' - †'
        output += '\n'

        output += '\tMoves:' + str(self.movement_points) + '\n'
        output += '\tStrength:' + str(self.current_strength) + '/' + str(self.attack_strength) + '\n'
        output += '\tCombat:' + str(self.attack_letter) + str(self.attack_number) + '\n'
        output += '\tAllegiance:' + str(self.allegiance) + '\n'
        output += '-'*20
        return output
      
    def __repr__(self):
        '''
        Returns a terminal representation of the block - same as __str__
        '''
        output = str(self)
        return output

    def __eq__(self,other):
        if type(self) == type(other):
            return self.name == other.name
        else:
            return False


      
    def is_dead(self):
        return self.current_strength <= 0
 

class Noble(Block):
    """
    adds extra attribute home_location on top of Block
    """
    
    def __init__(self, name = None, movement_points = None, attack_letter = None, attack_number = None, max_attack_strength = None,\
                 has_cross = None, blockID = None, home_location = None, loyalty = None, allegiance = None):

        super(Noble, self).__init__(name, movement_points, attack_letter, attack_number, max_attack_strength, \
                 has_cross, blockID, allegiance)

        self.home_location = home_location
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
                    
                elif self.allegiance == 'ENGLAND':

                    self.allegiance = 'SCOTLAND'

                    
            else:
                
                self.allegiance = allegiance   
        if self.current_strength == 0:
                self.current_strength = 1
        


    def b2_to_b3(self, change = None):
        if change == None:
            if self.attack_number == 3:
                self.attack_number = 2
            else:
                self.attack_number = 3
        else:
            self.attack_number = change
            
