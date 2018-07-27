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
import dice
    
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
    """
    receives a card
    returns 1, 2, or 3 for card values or 4 for event cards
    """

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


def random_card(computer_hand):
    """
    receives computer_hand
    returns a random card from computer hand
    """
    
    if len(computer_hand) != 1:
        random_index = random.randint(0,len(computer_hand)-1)
    else:
        random_index = 0
    return computer_hand[random_index]


def one_execution(board, position, role):
    '''
    This function takes three parameters, a board object, a string
    position which is whether the computer or opponent is playing, and role
    that the player is playing (england or scotland). Then the function
    executes a 1 move card.
    '''
    if position == 'opp':
        region_name = ''
        focus_region = ''
        while focus_region not in board.get_controlled_regions(role):
            region_name = input("Which region would you like to focus your movement?\n>")
            focus_region = board.regions[board.regionID_dict[region_name.upper()]]
            #Check to see if all the blocks are pinned or not
            if focus_region.is_contested and len(focus_region.combat_dict['Attackers'] > len(focus_region.combat_dict['Defenders'])):
                print('All of the blocks in that region are pinned!')
                region_name = ''
            #Check to see if the region is friendly
            if focus_region not in board.get_controlled_regions(role):
                print('That region is not friendly!')
                region_name = ''

        #Set the moveable block count
        if focus_region.is_contested:
            moveable_count = len(focus_region.combat_dict['Attackers']) > len(focus_region.combat_dict['Defenders'])

        else:
            moveable_count = len(focus_region.blocks_present)

        
        #Start moving specific blocks with user input
        for i in range(moveable_count):

            check_lst = list()
            #Go through blocks in focus region and put their names in a list
            for block in focus_region:
                check_lst.append(block.name.lower())
            block_name = ''
            block = ""
            end_region_name = ''
            end_region = ''
            #Get user input as to which block they want to move
            while block_name not in check_lst:
                    #Input block name
                    block_name = input("Which block would you like to move from " + focus_region.name + "?\n>")
                    #Get block object
                    block = find_block(block_name.lower(), board.blocks)
                    #Make sure block is in region
                    if block_name not in check_lst:
                        print("That block in not in the focus region!")
                    #Make sure block has not already been moved this turn
                    if block.name in blocks_moved:
                        print("You have already moved that block this turn!")
                        block_name = ''
            #Figure out where user wants to move block to
            while end_region not in board.get_controlled_regions(role):
                end_region_name = input("What region would you like to move to?\n>")
                #Make sure that the region name is actually a region name
                if end_region_name.upper() in board.regionID_dict:
                    #Get the region object from the region name
                    end_region = board.regions[regionID_dict[end_region_name.upper()]]
                    #Make sure that the move is a valid move
                    if not board.check_path(block_choice.movement_points, focus_region.regionID, end_region.regionID):
                        print('That is an invalid move')
                        end_region = ''
            #Move the block to its location
            current_board.move_block(block, focus_region.regionID, end_region.regionID)
            #Add the block to the moved blocks list
            blocks_moved.append(block.name)
            print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':

        
        #Get a random starting region
        start_regions = current_board.get_controlled_regions(role)
        rand_startID = random.randint(0, len(start_regions))
        start_region = start_regions[rand_startID]
        #Loop through blocks in random region
        for block in start_region:
            #50% chance that the computer will move block
            if random.randint(0,2) == 0:
                while flag:
                    #Get random region to move the block to
                    end_ID = random.randint(0,23)
                    if end_ID != start_region.regionID:
                        flag = False
                #Make sure that the move to random region is legal
                while not board.check_path(block, block.movement_points, start_region.regionID, end_ID):
                    flag = True
                    while flag:
                        #Get new random region
                        end_ID = random.randint(0,23)
                        if end_ID != start_region.regionID:
                            flag = False
                #Move block
                board.move_block(block, start_region.regionID, end_ID)
                print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)







def two_execution(position):
    '''
    This function takes three parameters, a board object, a string
    position which is whether the computer or opponent is playing, and role
    that the player is playing (england or scotland). Then the function
    executes a 2 move card.
    '''
    if position == 'opp':
        for j in range(2):
            blocks_moved = list()
            region_name = ''
            focus_region = ''
            while focus_region not in board.get_controlled_regions(role):
                region_name = input("Which region would you like to focus your movement?\n>")
                focus_region = board.regions[board.regionID_dict[region_name.upper()]]
                #Check to see if all the blocks are pinned or not
                if focus_region.is_contested and len(focus_region.combat_dict['Attackers'] > len(focus_region.combat_dict['Defenders'])):
                    print('All of the blocks in that region are pinned!')
                    region_name = ''
                if focus_region not in board.get_controlled_regions(role):
                    print('That region is not friendly!')
                    region_name = ''

            if focus_region.is_contested:
                moveable_count = len(focus_region.combat_dict['Attackers']) > len(focus_region.combat_dict['Defenders'])

            else:
                moveable_count = len(focus_region.blocks_present)

            

            for i in range(moveable_count):

                check_lst = list()
                for block in focus_region:
                    check_lst.append(block.name.lower())

                block_name = ""
                block = ''
                end_region_name = ''
                end_region = ''
                while block_name not in check_lst:
                    block_name = input("Which block would you like to move from " + focus_region.name + "?\n>")
                    block = find_block(block_name.lower(), board.blocks)
                    if block_name not in check_lst:
                        print("That block in not in the focus region!")
                    if block.name in blocks_moved:
                        print("You have already moved that block this turn!")
                        block_name = ''

                while end_region not in board.get_controlled_regions(role):
                    end_region_name = input("What region would you like to move to?\n>")

                    if end_region_name.upper() in board.regionID_dict:
                        end_region = board.regions[regionID_dict[end_region_name.upper()]]
                        if not board.check_path(block_choice.movement_points, focus_region.regionID, end_region.regionID):
                            print('That is an invalid move')
                            end_region = ''

                current_board.move_block(block, focus_region.regionID, end_region.regionID)
                blocks_moved.append(block.name)
                print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':
        #Get a random starting region
        
        moved_blocks = list()
        for i in range(2):
            start_regions = current_board.get_controlled_regions(role)
            rand_startID = random.randint(0, len(start_regions))
            start_region = start_regions[rand_startID]
        
            for block in start_region:
                if block not in moved_blocks:
                    if random.randint(0,2) == 0:
                        while flag:
                            end_ID = random.randint(0,23)
                            if end_ID != start_region.regionID:
                                flag = False
                        while not board.check_path(block, block.movement_points, start_region.regionID, end_ID):
                            flag = True
                            while flag:
                                end_ID = random.randint(0,23)
                                if end_ID != start_region.regionID:
                                    flag = False
                        board.move_block(block, start_region.regionID, end_ID)
                        moved_blocks.append(block)
                        print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)


def three_execution(position):
    '''
    This function takes three parameters, a board object, a string
    position which is whether the computer or opponent is playing, and role
    that the player is playing (england or scotland). Then the function
    executes a 3 move card.
    '''
    if position == 'opp':
        for j in range(3):
            blocks_moved = list()
            region_name = ''
            focus_region = ''
            while focus_region not in board.get_controlled_regions(role):
                region_name = input("Which region would you like to focus your movement?\n>")
                focus_region = board.regions[board.regionID_dict[region_name.upper()]]
                #Check to see if all the blocks are pinned or not
                if focus_region.is_contested and len(focus_region.combat_dict['Attackers'] > len(focus_region.combat_dict['Defenders'])):
                    print('All of the blocks in that region are pinned!')
                    region_name = ''
                if focus_region not in board.get_controlled_regions(role):
                    print('That region is not friendly!')
                    region_name = ''

            if focus_region.is_contested:
                moveable_count = len(focus_region.combat_dict['Attackers']) > len(focus_region.combat_dict['Defenders'])

            else:
                moveable_count = len(focus_region.blocks_present)

            

            for i in range(moveable_count):

                check_lst = list()
                for block in focus_region:
                    check_lst.append(block.name.lower())

                block_name = ""
                block = ''
                end_region_name = ''
                end_region = ''
                while block_name not in check_lst:
                    block_name = input("Which block would you like to move from " + focus_region.name + "?\n>")
                    block = find_block(block_name.lower(), board.blocks)
                    if block_name not in check_lst:
                        print("That block in not in the focus region!")
                    if block.name in blocks_moved:
                        print("You have already moved that block this turn!")
                        block_name = ''

                while end_region not in board.get_controlled_regions(role):
                    end_region_name = input("What region would you like to move to?\n>")

                    if end_region_name.upper() in board.regionID_dict:
                        end_region = board.regions[regionID_dict[end_region_name.upper()]]
                        if not board.check_path(block_choice.movement_points, focus_region.regionID, end_region.regionID):
                            print('That is an invalid move')
                            end_region = ''

                current_board.move_block(block, focus_region.regionID, end_region.regionID)
                blocks_moved.append(block.name)
                print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':
        #Get a random starting region
        moved_blocks = list()
        for i in range(3):
            start_regions = current_board.get_controlled_regions(role)
            rand_startID = random.randint(0, len(start_regions))
            start_region = start_regions[rand_startID]

            for block in start_region:
                if block not in moved_blocks:
                    if random.randint(0,2) == 0:
                        while flag:
                            end_ID = random.randint(0,23)
                            if end_ID != start_region.regionID:
                                flag = False
                        while not board.check_path(block, block.movement_points, start_region.regionID, end_ID):
                            flag = True
                            while flag:
                                end_ID = random.randint(0,23)
                                if end_ID != start_region.regionID:
                                    flag = False
                        board.move_block(block, start_region.regionID, end_ID)
                        moved_blocks.append(block)
                        print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)

def sea_execution(board, position, role):
    """
    Receives current board, opp/comp, and scotland/england
    For computer:
        Finds a block in a friendly, coastal region and moves to a randomized friendly, coastal region
    For human:
        Receives input name of block, loops until valid block (in friendly, coastal territory)
        Receives input name of region, loops until valid region (friendly, coastal territory that block is not already in)
        
    Prints executed action
    """
        
    if position == 'comp':
            #temporary for dumb AI
            #loops through list of blocks until it finds one it owns that's in a friendly region
            #continually chooses random friendly region until it finds coastal friendly region
                    
        for block in board.blocks:
            # if block in coastal, friendly region
            coastal = False
            friendly = False
            
            if combat.find_location(board, block.name).coast:
                coastal = True
                
            if combat.find_location(board, block.name) in board.get_controlled_regions(role):
                friendly = True
            
            if coastal and friendly:
                chosen_block = block
            
        region_found = False
        
        while not region_found:
            
            regio = pick_random_region(board, role)
            not_same = False
            coastal = False
            friendly = False
            
            if combat.find_location(board, chosen_block) != board.regions(board.regionID_dict[regio.name.upper()]):
                not_same = True
                
            if regio.coast:
                coastal = True
                
            if regio in board.get_controlled_regions(role):
                friendly = True
                
            if not_same and coastal and friendly:
                end_region = regio
                region_found = True

                    
        board.add_to_location(board, chosen_block, end_region)
                
        print(chosen_block.name + ' was moved from ' + combat.find_location(board, chosen_block.name).name + ' to ' + end_region.name)
            
        
    elif position == 'opp':
            
        valid_block = False # true if block is in a coastal, friendly region
            
        while valid_block == False:    
            block_name = input('Which block would you like to move?\n>')
            # is on the coast and in friendly territory (ie player owns block)
            if combat.find_location(board, block_name).coast and combat.find_location(board, block_name) in board.get_controlled_regions(role): 
                valid_block = True
                chosen_block = board.get_block(block_name, combat.find_location(board, block_name))
            else:
                print('Invalid block.')
                    
        valid_end_region = False # true if ending location for block is coastal and friendly
        
        while valid_end_region == False:    
            region_name = input('Where would you like to move ' + block_name + '?\n>')
            # if it's not the same as the starting region, it's coastal, and it's friendly
            if combat.find_location(board, block_name) != board.regions(board.regionID_dict[region_name.upper()]) and board.regions(board.regionID_dict[region_name.upper()]).coast and combat.find_location(board, block_name) in board.get_controlled_regions(role):
                valid_end_region = True
                
            else:
                print('Invalid region.')
                
        board.add_to_location(board, block, board.regions(board.regionID_dict[region_name.upper()]))
        
        print(block_name + ' moved from ' + combat.find_location(board, block_name).name + ' to ' + region_name)

    
def her_execution(board, position, role):
    '''
    Activates the HERALD card.
    position:  'opp' or 'comp' - ai or player
    board:  Board object
    '''

    #List of available nobles to steal
    enemy_nobles = []

    for enemy_region in board.get_controlled_regions(role):
        for block in enemy_region.blocks_present:

            if type(block) == blocks.Noble and block.name != 'MORAY':
                enemy_nobles.append(block)

    if position == 'opp':

        #Print out available nobles
        for noble in enemy_nobles:
            print(noble.name)

        #Take input
        valid_input = False
        while not valid_input:
            name_input = input('Which noble will you try to take?: ').strip()

            #Check if the input is valid
            for noble in enemy_nobles:

                if name_input == noble.name:
                    valid_input = True
                    noble_to_steal = noble

                else:
                    print('Invalid input. Please try again.')

    elif position == 'comp':
        #PICK A RANDOM NOBLE - TEMPORARY
        num_nobles = len(enemy_nobles)
        rand_selection = random.randint(num_nobles)
        noble_to_steal = enemy_nobles[rand_selection]

    #Roll the die and take the number from the list
    print('Roll a die to take the noble. 1-4 = success, 5-6 = failure.\n>')

    rand_num = dice.roll(1)[0]
    if rand_num <= 4:
        #STEAL NOBLE
        noble_to_steal.change_allegiance()

        #Find the noble's region
        for region in board.regions:
            if noble_to_steal in region.blocks_present:
                noble_region = region

        #Move the noble to its own region - will sort it into attacker/defender
        board.move_block(noble_to_steal, noble_region.regionID, noble_region.regionID)
        print('Success')
    else:
        print('Failure')


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
