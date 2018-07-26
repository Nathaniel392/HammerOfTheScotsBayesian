#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:05:44 2018

@author: amylvaganam
"""

######### temporary set of functions for temporary gameplay

"""
HOW TO UTILIZE:
    
deck = Deck()
deck.shuffle()
computer_hand = list()
for i in range(5):
    computer_hand.append(deck.deal())
   
    
print(computer_hand)
card = cardplay.random_card(computer_hand)
print(card)

card = cardplay.dumb_go_first(computer_hand)
print(card)

card = cardplay.dumb_go_second(computer_hand)
print(card)
"""

import random
    
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
        if get_card_val(card) < min_val:
            min_val = get_card_val(card)
            ret_card = card
    return ret_card


def dumb_go_first(computer_hand): # plays highest card
    
    max_val = 0 #initialize an initial "max" val 
    
    for card in computer_hand:
        if get_card_val(card) > max_val:
                max_val = get_card_val(card)
                ret_card = card
                
    return ret_card


def random_card(computer_hand): #return random card in computer deck
    random_index = random.randint(0,len(computer_hand)-1)
    return computer_hand[random_index]

def compare_cards(opp_card, computer_card, computer_role):
    
    """
    takes the opponent card, computer card, and computer allegiance (england/scotland)
    compares cards for which side plays their turn first
    returns true for computer going first, false for opponent first
    """
    
    if get_card_val(opp_card) > get_card_val(computer_card):
        return False
    elif get_card_val(opp_card) > get_card_val(computer_card):
        return True
    elif get_card_val(opp_card) == get_card_val(computer_card):
        if computer_role.lower() == 'england':
            return True
        elif computer_role.lower() == 'scotland':
            return False
        
