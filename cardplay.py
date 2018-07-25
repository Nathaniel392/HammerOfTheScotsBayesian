#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:05:44 2018

@author: amylvaganam
"""

# temporary class for temporary gameplay

import random

class Cardplay( object ):
    
    #ultimately: return card that the computer decides to play
    
    def order(): #returns randomly for now whether play one or two goes first
        
        if random.randint(0,2) == 1:
            return 1
        return 2
    
    def get_card_val(card):
        

        if card == '1':
            return 1
        if card == '2':
            return 2
        if card == '3':
            return 3
        else:
            return 4
    
    def dumb_go_second(computer_hand): #plays lowest card
        
        min_val = 50 #initialize an initial "min" val 
        
        for card in computer_hand:
            if card.get_card_val < min_val:
                min_val = card.get_card_val
                ret_card = card
        return ret_card
    
    
    def dumb_go_first(computer_hand): # plays highest card
        
        max_val = 0 #initialize an initial "max" val 
        
        for card in computer_hand:
            if card.get_card_val > max_val and len(computer_hand) != 1:
                if card.get_card_val != 4: #non-event card
                    max_val = card.get_card_val
                    ret_card = card
            else: #last card
                max_val = card.get_card_val
                ret_card = card
                    
        return ret_card
    
    
    def random_card(computer_hand): #return random card in computer deck
        if len(computer_hand) != 0:
            random_index = random.randint(0,len(computer_hand)-1)
            return computer_hand[random_index]
        return computer_hand[0]