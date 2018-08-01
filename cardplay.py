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

import dice
import search
import find_block
import blocks

    
#ultimately: return card that the computer decides to play


def pick_random_region(board, role):
    '''
    Picks a random region that the computer controls, returns its regionID.
    role:  'ENGLAND' or 'SCOTLAND'
    '''
    friendly_regions = board.get_controlled_regions(role)

    num_regions = len(friendly_regions)
    rand_selection = random.randint(0, num_regions-1)
    selected_region = friendly_regions[rand_selection]

    return selected_region


def order(): #returns randomly for now whether play one or two goes first
    if random.randint(1, 2) == 1:
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
    card_to_play = computer_hand[random_index]
    print('computer hand: ', computer_hand)
    print('computer plays ', card_to_play)
    return computer_hand[random_index]


def one_execution(board, position, role,truce=False):
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
            try:
                region_name = input("Which region would you like to focus your movement?\n>")
                focus_region = board.regions[board.regionID_dict[region_name.upper()]]
            except KeyError:
                print('not valid region')
                continue
            #Check to see if all the blocks are pinned or not
            if focus_region.is_contested() and len(focus_region.combat_dict['Attacking']) > len(focus_region.combat_dict['Defending']):
                print('All of the blocks in that region are pinned!')
                region_name = ''
            #Check to see if the region is friendly
            if focus_region not in board.get_controlled_regions(role):
                print('That region is not friendly!')
                region_name = ''


        #Set the moveable block count
        if focus_region.is_contested():
            moveable_count = len(focus_region.combat_dict['Attacking']) - len(focus_region.combat_dict['Defending'])

        else:
            moveable_count = len(focus_region.blocks_present)

        
        #Start moving specific blocks with user input
        for i in range(moveable_count):

            check_lst = list()
            #Go through blocks in focus region and put their names in a list
            for block in focus_region.blocks_present:
                check_lst.append(block.name)
            block_name = ''
            block = ""
            end_region_name = ''
            end_region = ''
            #Get user input as to which block they want to move
            while block_name not in check_lst:
                    #Input block name
                    block_name = input("Which block would you like to move from " + focus_region.name + "?\n>")
                    #Get block object
                    block = find_block.find_block(block_name, focus_region.blocks_present)
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
                    end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                    #Make sure that the move is a valid move
                    if board.move_block(block_choice.movement_points, focus_region.regionID, end_region.regionID,truce) == False:
                        print('That is an invalid move')
                        end_region = ''
            #Move the block to its location
            #Add the block to the moved blocks list
            blocks_moved.append(block.name)
            print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':

        
        #Get a random starting region
        start_regions = board.get_controlled_regions(role)
        rand_startID = random.randint(0, len(start_regions) - 1)
        start_region = start_regions[rand_startID]
        #Loop through blocks in random region
        for block in start_region.blocks_present:
            #50% chance that the computer will move block
            if random.randint(0,1) == 0:
                flag = True
                while flag:
                    #Get random region to move the block to
                    end_ID = random.randint(0,22)
                    if end_ID != start_region.regionID:
                        flag = False
                #Make sure that the move to random region is legal
                while not board.check_path(block, block.movement_points, start_region.regionID, end_ID):
                    flag = True
                    while flag:
                        #Get new random region
                        end_ID = random.randint(0,22)
                        if end_ID != start_region.regionID:
                            flag = False
                #Move block
                board.move_block(block, start_region.regionID, end_ID)
                print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)







def two_execution(board,position,role,truce=False):
    '''
    This function takes three parameters, a board object, a string
    position which is whether the computer or opponent is playing, and role
    that the player is playing (england or scotland). Then the function
    executes a 2 move card.
    '''

    #region_regions is a list of focus regions!!!!



    ####HELLO
   
    prev_paths = []

    if position == 'opp':
        region_regions = []
        for j in range(2):
            blocks_moved = list()
            region_name = ''
            focus_region = ''
            while focus_region not in board.get_controlled_regions(role):
                try:
                    region_name = input("Which region would you like to focus your movement?\n>")
                    focus_region = board.regions[board.regionID_dict[region_name.upper()]]
                except KeyError:
                    print('not valid region')
                    continue
                #Check to see if all the blocks are pinned or not
                if focus_region.is_contested() and len(focus_region.combat_dict['Attacking']) > len(focus_region.combat_dict['Defending']):
                    print('All of the blocks in that region are pinned!')
                    region_name = ''
                if focus_region not in board.get_controlled_regions(role):
                    print('That region is not friendly!')
                    region_name = ''
             

            if focus_region.is_contested():
                moveable_count = len(focus_region.combat_dict['Attacking']) - len(focus_region.combat_dict['Defending'])
                
            else:
                moveable_count = len(focus_region.blocks_present)
         
            region_regions.append(focus_region)
            

            for region_name_region in region_regions:
                
                for i in range(moveable_count):
                 
                    check_lst = list()
                    for block in focus_region.blocks_present:
                        check_lst.append(block.name)

                    block_name = ""
                    block = ''
                    end_region_name = ''
                    end_region = ''
                    while block_name not in check_lst:
                        block_name = input("Which block would you like to move from " + region_name_region.name + "?\n>")
                        block = find_block.find_block(block_name, focus_region.blocks_present)
                        if block_name not in check_lst:
                            print("That block in not in the focus region!")
                        if block.name in blocks_moved:
                            print("You have already moved that block this turn!")
                            block_name = ''

                    while end_region not in board.get_controlled_regions(role):
                        end_region_name = input("What region would you like to move to?\n>")

                        if end_region_name.upper() in board.regionID_dict:
                            end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                            if board.move_block(block_choice.movement_points, region_name_region.regionID, end_region.regionID,position,prev_paths,truce) == False:
                                print('That is an invalid move')
                                end_region = ''

                    blocks_moved.append(block.name)
                    print(block.name + " was moved from " + region_name_region.name + ' to ' + end_region.name)

    if position == 'comp':
        #Get a random starting region
        
        moved_blocks = list()
        for i in range(2):
            start_regions = board.get_controlled_regions(role)
            rand_startID = random.randint(0, len(start_regions) - 1)
            start_region = start_regions[rand_startID]
        
            for block in start_region.blocks_present:
                if block not in moved_blocks:
                    if random.randint(0,1) == 0:
                        flag = True
                        while flag:
                            end_ID = random.randint(0,22)
                            if end_ID != start_region.regionID:
                                flag = False
                        while not board.check_path(block.movement_points, start_region.regionID, end_ID,role,):
                            flag = True
                            while flag:
                                end_ID = random.randint(0,22)
                                if end_ID != start_region.regionID:
                                    flag = False
                        board.move_block(block, start_region.regionID, end_ID,position,prev_paths,truce)
                        moved_blocks.append(block)
                        print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)


def three_execution(board, position,role,truce = False):
    '''
    This function takes three parameters, a board object, a string
    position which is whether the computer or opponent is playing, and role
    that the player is playing (england or scotland). Then the function
    executes a 3 move card.
    '''


    #region_regions is a list of focus regions!!!!
    


   

    prev_paths = []
    ####HELLO
    if position == 'opp':
        region_regions = []
        for j in range(3):
            blocks_moved = list()
            region_name = ''
            focus_region = ''
            while focus_region not in board.get_controlled_regions(role):
                try:
                    region_name = input("Which region would you like to focus your movement?\n>")
                    focus_region = board.regions[board.regionID_dict[region_name.upper()]]
                except KeyError:
                    print('not valid region')
                    continue
                #Check to see if all the blocks are pinned or not
                if focus_region.is_contested() and len(focus_region.combat_dict['Attacking']) > len(focus_region.combat_dict['Defending']):
                    print('All of the blocks in that region are pinned!')
                    region_name = ''
                if focus_region not in board.get_controlled_regions(role):
                    print('That region is not friendly!')
                    region_name = ''
          

            if focus_region.is_contested():
                moveable_count = len(focus_region.combat_dict['Attacking']) - len(focus_region.combat_dict['Defending'])

            else:
                moveable_count = len(focus_region.blocks_present)
            
            region_regions.append(focus_region)
           
            for region_name_region in region_regions:
              
                for i in range(moveable_count):
                   
                    check_lst = list()
                    for block in focus_region.blocks_present:
                        check_lst.append(block.name)

                    block_name = ""
                    block = ''
                    end_region_name = ''
                    end_region = ''
                    while block_name not in check_lst:
                        block_name = input("Which block would you like to move from " + region_name_region.name + "?\n>")
                        block = find_block.find_block(block_name, focus_region.blocks_present)
                        if block_name not in check_lst:
                            print("That block in not in the focus region!")
                        if block.name in blocks_moved:
                            print("You have already moved that block this turn!")
                            block_name = ''

                    while end_region not in board.get_controlled_regions(role):
                        end_region_name = input("What region would you like to move to?\n>")

                        if end_region_name.upper() in board.regionID_dict:
                            end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                            if board.move_block(block_choice.movement_points, region_name_region.regionID, end_region.regionID,position,prev_paths,truce) == False:
                                print('That is an invalid move')
                                end_region = ''

                    blocks_moved.append(block.name)
                    print(block.name + " was moved from " + region_name_region.name + ' to ' + end_region.name)

    if position == 'comp':
        #Get a random starting region
        moved_blocks = list()
        for i in range(3):
            start_regions = board.get_controlled_regions(role)
            rand_startID = random.randint(0, len(start_regions) - 1)
            start_region = start_regions[rand_startID]

            for block in start_region.blocks_present:
                if block not in moved_blocks:
                    if random.randint(0,2) == 0:
                        flag = True
                        while flag:
                            end_ID = random.randint(0,22)
                            if end_ID != start_region.regionID:
                                flag = False
                        while not board.check_path(block.movement_points, start_region.regionID, end_ID, role):
                            flag = True
                            while flag:
                                end_ID = random.randint(0,22)
                                if end_ID != start_region.regionID:
                                    flag = False
                        board.move_block(block, start_region.regionID, end_ID,position,prev_paths,truce)
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
        
        #list of all blocks present in friendly areas
        friendly_blocks = []
        for region in board.get_controlled_regions(role):
            for block in region.blocks_present:
                friendly_blocks.append(block)

        for block in friendly_blocks:
            # if block in coastal, friendly region
            coastal = False
            friendly = False
            
            if combat.find_location(board, block.name).coast:
                coastal = True
                
            if combat.find_location(board, block.name) in board.get_controlled_regions(role):
                friendly = True
            
            if block.name.lower() != 'norse':
                not_norse = True
            
            if coastal and friendly and not_norse:
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
                
        
        
        old_region_name = combat.find_location(board, chosen_block.name).name
                    
        board.add_to_location(board, chosen_block, end_region)
                
        print(chosen_block.name + ' was moved from ' + old_region_name + ' to ' + end_region.name)
            
        
    elif position == 'opp':
          
            
        #create and print a list of coastal, friendly regions where norse is not the ONLY one
        
        possible_region_list = []
        
        for region in board.regions():
            if region.coast:
                coast = True
            if region in board.get_controlled_regions(role):
                friendly = True
            if len(region.blocks_present()) == 1 and region.blocks_present[0].name.upper() == 'NORSE':
                just_norse = True
            
            if coast and friendly and not just_norse:
                possible_region_list.append(region)
        
        
        original_region_name = input('Which region would you like to move block(s) from? Enter a name or \'none\'.\n>')
        
        if original_region_name.lower() != 'none':
            
            original_region = search.region_name_to_object(board, original_region_name)
        
            valid_region = False
            while not valid_region:
                
                if original_region in possible_region_list:
                    valid_region = True
                else:
                    print('Invalid region.')
                
            
            for x in range(0,2):
                #list of possible blocks to move (present in region)
                possible_block_list = []
                for block in original_region.blocks_present:
                    possible_block_list.append(block)
                
                block_name = input('Which block would you like to move? Enter a name.\n>')
                
                block_move_list = []
                
                block_to_move = search.block_name_to_object(possible_block_list, block_name)
            
                valid_block = False
                
                while not valid_block:
                    if block_to_move:
                        if block_to_move.name.upper() != 'NORSE':
                            valid_block = True
                            block_move_list.append(block_to_move)
                    else:
                        print('Invalid block.')
                        
                    
            new_region_name = input('Which region would you like to move block(s) to? Enter a name.\n>')

                
            new_region = search.region_name_to_object(board, new_region_name)
        
            valid_region = False
            
            while not valid_region:
                
                if original_region in possible_region_list:
                    valid_region = True
                else:
                    print('Invalid region.')
                
            for block in block_move_list:
        
                board.add_to_location(board, block, new_region)
        
                print(block.name + ' moved from ' + original_region.name + ' to ' + new_region.name)
            
            
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
            name_input = input('Which noble will you try to take?: ').strip().upper()

            #Check if the input is valid
            for noble in enemy_nobles:

                if name_input == noble.name:
                    valid_input = True
                    noble_to_steal = noble

                else:
                    print('Invalid input. Please try again.')

    elif position == 'comp':
        ###
        ###
        ### PICK A RANDOM NOBLE - TEMPORARY
        ###
        ###
        num_nobles = len(enemy_nobles)
        rand_selection = random.randint(num_nobles)
        noble_to_steal = enemy_nobles[rand_selection]
        print('Computer picked ' + noble_to_steal.name)
        ###
        ###
        ###
        ###
        ###

    #Roll the die and take the number from the list
    print('Roll a die to take the noble. 1-4 = success, 5-6 = failure.\n>')

    rand_num = dice.roll(1)[0]
    print('DIE ROLL: ' + str(rand_num))

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


def vic_execution(board, position, role):
    '''
    Pick a friendly region and distribute 3 health points to them.
    role = 'ENGLAND' or 'SCOTLAND'
    position = 'comp' or 'opp'
    '''

    #List of all friendly regions
    friendly_list = board.get_controlled_regions(role)

    #Remove regions with all blocks at full health
   

    #Human player
    if position == 'opp':

        #Print all available regions to select
        for region in friendly_list:
            print(region.name)

        #Prompt for a region to select
        valid_input = False
        selected_region = None
        while not valid_input:

            #Take a name input and convert it to a region object
            selected_region_name = input('Which region do you want to heal?: ').strip().upper()

            if search.region_name_to_object(friendly_list, selected_region_name):
                selected_region = search.region_name_to_object(friendly_list, selected_region_name)
                valid_input = True


            else:
                print('Invalid input. Please try again.')

        health_points = 3
        print('Possible blocks: ')
        for i, block in enumerate(selected_region.blocks_present):

            print(block.name, '[', i, ']', end = '\t')
        while health_points > 0:
            bad_input = True
            while bad_input:
                try:
                    print('You have ', health_points, ' health points remaining')
                    ID_to_heal = int(input('Which block index would you like to heal: '))
                    if ID_to_heal not in range(len(selected_region.blocks_present)):
                        print('Type in a valid block index')
                        continue
                    healing_points = int(input('How many health points would you like to heal it: '))
                    if healing_points <= 0 or healing_points > health_points:
                        print('You do not have that many healing points left')
                        continue
                except ValueError:
                    print('type in a number')
                    continue
                health_points -= selected_region.blocks_present[ID_to_heal].heal_until_full(healing_points)
                
                print(search.block_id_to_name(selected_region.blocks_present, ID_to_heal), ' got healed')



    #Computer
    elif position == 'comp':
        ###
        ###
        ### RANDOM DECISION - TEMPORARY
        ###
        ###
        num_regions = len(friendly_list)
        rand_selection = random.randint(0, num_regions - 1)
        selected_region = friendly_list[rand_selection]

        for i in range(3):
            rand_block_selection = random.randint(0, len(selected_region.blocks_present) - 1)
            selected_region.blocks_present[rand_block_selection].heal_until_full()
            print(selected_region.blocks_present[rand_block_selection].name, ' healed one point')

def pil_execution(board, position, role):
    possible = False
    if position == 'comp':
        
        #loop through regions to make sure there is a region that it works in
        for region_controlled in board.get_controlled_regions(role):
            for neighbor_region in region_controlled.find_all_borders(region_controlled.regionID):
                if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                    possible = True
        
        if possible:
            
            #make a list of possible opponent regions to be pillaged 
            possible_pill_lst = []
            for region in board.get_controlled_regions(role):
                for neighbor_region in region_controlled.find_all_borders(region_controlled.regionID):
                    if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                        possible_pill_lst.append(neighbor_region)
            
            valid_region = False
            while not valid_region:
                if role == 'SCOTLAND':
                    random_region = pick_random_region(board, 'ENGLAND')
                elif role == 'SCOTLAND':
                    random_region = pick_random_region(board, 'SCOTLAND')
                
                if board.regions(board.regionID_dict[random_region.upper()]) in possible_pill_lst:
                    valid_region = True
                    chosen_subtract_region = random_region
            
            
            # pillage combat-style
            for x in range (0,2):
                highest_strength_block = blocks.Block(intial_attack_strength = 0)
                #loop through and find the max strength block in the region
                #repeat twice for 2 hits total
                for block in chosen_subtract_region.blocks_present:
                    if block.current_strength > highest_strength_block.current_strength:
                        highest_strength_block = block
                        #strike once
                highest_strength_block.get_hurt(1)
                
                print(highest_strength_block.name + ' took one hit.')
                
                if block.is_dead():
                    if role == 'SCOTLAND':
                        board.eng_pool.append(block)
                        board.eng_roster.remove(block)
                    elif role == 'SCOTLAND':
                        board.scot_pool.append(block)
                        board.scot_roster.remove(block)
                
                
            taken_points = 2 #temp until I add in code to do less than 2 hits
            
            
            
            while not valid_region:
                #adding points to your own
                rand_region = pick_random_region(board, role)  
                if rand_region in chosen_subtract_region.find_all_borders(chosen_subtract_region.regionID):
                    neighbour = True
                if rand_region.is_friendly(role):
                    friendly = True
                if neighbour and friendly:
                    valid_region = True
            chosen_add_region = rand_region
                
            
            # CHANGE SO THAT HEALTH_PTS IS BASED ON HOW MANY ARE TAKEN FROM THE OPP REGION
            health_points = taken_points
            while health_points > 0:
                valid_input = False
                while not valid_input:
                    print('You have ', health_points, ' health points.')
                    #just a line for a random block in the chosen region
                    rand_block = chosen_add_region.blocks_present[0]
                    
                valid_block = False
                while not valid_block:
                    
                    #if the block is in the chosen region
                    if rand_block in chosen_add_region.blocks_present:
                        healing_points = random.randint(1,2)
                        if healing_points <= 0 or healing_points > health_points:
                            pass
                        else:
                            health_points -= healing_points
                            print(rand_block.name + ' was healed ' + healing_points + ' points.')
        
        else:
            print('There are no regions in which to play this card.')
            
            
        
    elif position == 'opp':
        #loop through regions to make sure there is a region that it works in
        for region_controlled in board.get_controlled_regions(role):
            for neighbor_region in region_controlled.find_all_borders(region_controlled.regionID):
                if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                    possible = True
        
        if possible:
            
            #make a list of possible opponent regions to be pillaged 
            possible_pill_lst = []
            for region in board.get_controlled_regions(role):
                for neighbor_region in region_controlled.find_all_borders(region_controlled.regionID):
                    if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                        possible_pill_lst.append(neighbor_region)
            
            valid_region = False
            while not valid_region:
                chosen_region_name = input('Which of your opponent\'s regions would you like to remove points from?')
                #region = board.regions(board.regionID_dict[chosen_region_name.upper()])
                chosen_region = search.region_name_to_object(board, chosen_region_name)
                    
                if chosen_region in possible_pill_lst:
                    valid_region = True
                    chosen_subtract_region = chosen_region
                    
                else:
                    print('Invalid region.')
            
            
            # pillage combat-style
            for x in range (0,2):
                highest_strength_block = blocks.Block(intial_attack_strength = 0)
                #loop through and find the max strength block in the region
                #repeat twice for 2 hits total
                for block in chosen_subtract_region.blocks_present:
                    if block.current_strength > highest_strength_block.current_strength:
                        highest_strength_block = block
                        #strike once
                highest_strength_block.get_hurt(1)
                print(highest_strength_block.name + ' took one hit.')
                
                if block.is_dead():
                    if role == 'SCOTLAND':
                        board.eng_pool.append(block)
                        board.eng_roster.remove(block)
                    elif role == 'SCOTLAND':
                        board.scot_pool.append(block)
                        board.scot_roster.remove(block)
                
            taken_points = 2 #temp until I add in code to do less than 2 hits
            
            while not valid_region:
                #adding points to your own
                chosen_add_region_name = input('Which of your neighbouring regions would you like to add points to? If none, enter \'none\'')    
                #region itself = board.regions(board.regionID_dict[chosen_add_region_name.upper()])
                
                if chosen_add_region_name.lower() != 'none':
                    
                    chosen_add_region = search.region_name_to_object(board, chosen_add_region_name)
                    
                    #nested so that no error if chosen_add_region is False
                    if chosen_add_region in chosen_subtract_region.find_all_borders(chosen_subtract_region.regionID):
                        neighbour = True
                        if chosen_add_region.is_friendly(role):
                            friendly = True
                        
                    if neighbour and friendly:
                        valid_region = True
                        
                    else:
                        print('Invalid region.')
                
            
            # CHANGE SO THAT HEALTH_PTS IS BASED ON HOW MANY ARE TAKEN FROM THE OPP REGION
            health_points = taken_points
            while health_points > 0:
                valid_input = False
                while not valid_input:
                    print('You have ', health_points, ' health points.')
                    block_name = int(input('Which block would you like to heal?\n>'))
                    block = search.block_name_to_object(chosen_add_region.blocks_present, block_name)
                valid_block_name = False
                while not valid_block_name:
                    #block itself = board.get_block(block_name, combat.find_location(board, block_name))
                    
                    #if the block is in the chosen region
                    if block in chosen_add_region_name.blocks_present:
                        healing_points = input('How many points would you like to heal it?\n>')
                        
                        if healing_points.isdigit():
                            if healing_points <= 0 or healing_points > health_points:
                                print('You do not have that many healing points left.')
                            else:
                                health_points -= healing_points
                                print(board.get_block(block_name, combat.find_location(board, block_name)).name + ' was healed ' + healing_points + ' points.')
                        else:
                            print('Invalid healing points.')
        else:
            print('There are no possible regions in which to play this card.')

def resolve_card(board, which_side, card, role,truce=False):
    
    """
    Takes in a string that lists side (comp/opp), the card for that side, and the role (england/scotland)
    based on string value of card, calls a function to execute the card itself
    
    """


    if card == '1':
        one_execution(board, which_side, role,truce)
    elif card == '2':
        two_execution(board, which_side, role,truce)
    elif card == '3':
        three_execution(board, which_side, role,truce)
            
    elif card == 'SEA':

        if which_side == 'opp':

            play_pass = input('Would you like to play the event card or pass it? (play/pass)')

        else:

            play_pass = 'play'
        
        if play_pass.lower() == 'play':
            sea_execution(board, which_side, role)
        else:
            pass
        
    elif card == 'HER':
        if which_side == 'opp':

            play_pass = input('Would you like to play the event card or pass it? (play/pass)')

        else:

            play_pass = 'play'
        
        if play_pass.lower() == 'play':
            her_execution(board, which_side, role)
        else:
            pass
        
    elif card == 'VIC':
        if which_side == 'opp':

            play_pass = input('Would you like to play the event card or pass it? (play/pass)')

        else:

            play_pass = 'play'
        
        if play_pass.lower() == 'play':
            vic_execution(board, which_side, role)
        else:
            pass
        
    elif card == 'PIL':
        
        if which_side == 'opp':

            play_pass = input('Would you like to play the event card or pass it? (play/pass)')

        else:

            play_pass = 'play'
        
        if play_pass.lower() == 'play':
            pil_execution(board, which_side, role)
        else:
            pass
        
    elif card == 'TRU':
        
        if which_side == 'opp':

            play_pass = input('Would you like to play the event card or pass it? (play/pass)')

        else:

            play_pass = 'play'
        
        if play_pass.lower() == 'play':
            return True
        else:
            pass
        
            
def compare_cards(board, opp_card, comp_card, comp_role):
    """
    takes the opponent card, computer card, and computer allegiance (ENGLAND/SCOTLAND)
    compares cards for which side plays their turn first
    returns True for computer going first, False for opponent first
    """
    
    year_ends_early = False

    
    
    if comp_role == 'SCOTLAND':
        opp_role = 'ENGLAND'
    elif comp_role == 'ENGLAND':
        opp_role = 'SCOTLAND'
    
    if get_card_val(opp_card) > get_card_val(comp_card):
      
        who_goes_first = False
    elif get_card_val(opp_card) < get_card_val(comp_card):
    
        who_goes_first = True
    elif get_card_val(opp_card) == get_card_val(comp_card):
     
        if comp_role == 'ENGLAND':
            who_goes_first = True
        elif comp_role == 'SCOTLAND':
            who_goes_first = False
        if get_card_val(opp_card) == 4 and get_card_val(comp_card) == 4:
            year_ends_early = True
        
        
    if who_goes_first: #if computer goes first
        resolve_card(board, 'comp', comp_card, comp_role)

        if resolve_card(board, 'comp',comp_card,comp_role) == True:

            resolve_card(board, 'opp', opp_card, opp_role,True)

        else:

            resolve_card(board, 'opp', opp_card, opp_role)

        
    elif not who_goes_first: #if opponent goes first
        
        resolve_card(board, 'opp', opp_card, opp_role)

        if resolve_card(board, 'opp', opp_card, opp_role) == True:

            resolve_card(board, 'comp', comp_card, comp_role,True)

        else:

            resolve_card(board, 'comp', comp_card, comp_role)

        
    return who_goes_first, year_ends_early
