#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:05:44 2018
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
import board
    
#ultimately: return card that the computer decides to play


def pick_random_region(board, role):
    '''
    Picks a random region that the computer controls, returns its regionID.
    role:  'ENGLAND' or 'SCOTLAND'
    '''
    friendly_regions = board.get_controlled_regions(role)

    num_regions = len(friendly_regions)
    rand_selection = random.randint(num_regions)
    selected_region = friendly_regions[rand_selection]

    return selected_region

     
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

def one_execution(position):
    pass
def two_execution(position):
    pass
def three_execution(position):
    pass

def sea_execution(board, position):
        
        if position == 'comp':
            pass
            
        elif position == 'opp':
            
            valid_block = False
            
            while valid_block == False:    
                block_name = input("which block would you like to move?\n>")
                if combat.find_location(board, block_name).coast : #is on the coast
                    print('yes, ' + block_name + ' is on the coast')
                    valid_block = True
                else:
                    block_name = input("Invalid block. Please re-enter.\n>")

    
def her_execution(position, board):
    '''
    
    '''


def vic_execution(position):
    pass
def pil_execution(position):
    pass
def tru_execution(position):
    pass

def resolve_card(board, which_side, card, role):
    
    """
    Takes in a string that lists side (comp/opp), the card for that side, and the role (ENGLAND/SCOTLAND)
    based on string value of card, calls a function to execute the card itself
    
    """
    if card == '1':
        one_execution(board, which_side)
    elif card == '2':
        two_execution(board, which_side)
    elif card == '3':
        three_execution(board, which_side)
    elif card == 'SEA':
        sea_execution(board, which_side)
    elif card == 'HER':
        her_execution(board, which_side)
    elif card == 'VIC':
        vic_execution(board, which_side)
    elif card == 'PIL':
        pil_execution(board, which_side)
    elif card == 'TRU':
        tru_execution(board, which_side)
        
            
def compare_cards(board, opp_card, comp_card, comp_role):
    """
    takes the opponent card, computer card, and computer allegiance (ENGLAND/SCOTLAND)
    compares cards for which side plays their turn first
    returns True for computer going first, False for opponent first
    """
    
    year_ends_early = False
    
    if comp_role.lower() == 'SCOTLAND':
        opp_role = 'ENGLAND'
    elif comp_role.lower() == 'ENGLAND':
        opp_role = 'SCOTLAND'
    
    if get_card_val(opp_card) > get_card_val(comp_card):
        who_goes_first = False
    elif get_card_val(opp_card) > get_card_val(comp_card):
        who_goes_first = True
    elif get_card_val(opp_card) == get_card_val(comp_card):
        if comp_role.lower() == 'ENGLAND':
            who_goes_first = True
        elif comp_role.lower() == 'SCOTLAND':
            who_goes_first = False
        if get_card_val(opp_card) == 4 and get_card_val(comp_card) == 4:
            year_ends_early = True
        
        
    if who_goes_first: #if computer goes first
        resolve_card(board, 'comp', comp_card, comp_role)
        resolve_card(board, 'opp', opp_card, opp_role)
        
    elif not who_goes_first: #if opponent goes first
        resolve_card(board, 'opp', opp_card, opp_role)
        resolve_card(board, 'comp', comp_card, comp_role)
        
    return who_goes_first, year_ends_early
