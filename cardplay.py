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
import combat

    
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
    prev_paths = []
    if position == 'opp':

        blocks_moved = []
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
        end = False
        for i in range(moveable_count):
            if end == False:
                check_lst = list()
                #Go through blocks in focus region and put their names in a list
                for block in focus_region.blocks_present:
                    check_lst.append(block.name)

                block_name = ''
                block = ""
                end_region_name = ''
                end_region = ''
                end = False
                focus_blocks = []
                for x in focus_region.blocks_present:
                    focus_blocks.append(x.name)
                #Get user input as to which block they want to move
                while end == False and block_name not in check_lst:
                        #Input block name
                        block_name = input("Which block would you like to move from " + focus_region.name + " (Enter 'done' if done)?\n>").upper()
                        if block_name == 'DONE':
                            end = True
                        elif block_name in focus_blocks:
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
                '''
                check = False
                if block_name == 'DONE':
                    check = True
                while check == False:
                    
                    end_region_name = input("What region would you like to move to?\n>")

                    if end_region_name.upper() in board.regionID_dict:
                        end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                        check = True
                prev_paths = []

                while end == False and not board.check_path(block.movement_points,focus_region.regionID, end_region.regionID, block):

                    end_region_name = input("What region would you like to move to?\n>")
                    #Make sure that the region name is actually a region name
                    if end_region_name.upper() in board.regionID_dict:
                        #Get the region object from the region name
                        end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                        #Make sure that the move is a valid move
                        
                        '''
                #if board.move_block(block, focus_region.regionID, end_region.regionID,prev_paths, truce):
                        
                #Move the block to its location
                #Add the block to the moved blocks list
                if block_name != 'DONE':
                    blocks_moved.append(block.name)
                    board.move_block(block,focus_region.regionID, -1, position,prev_paths,truce)
                    #print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':

        
        #Get a random starting region
        start_regions = board.get_controlled_regions(role)
        rand_startID = random.randint(0, len(start_regions) - 1)
        start_region = start_regions[rand_startID]
        #Loop through blocks in random region
        for block in start_region.blocks_present:
            #75% chance that the computer will move block
            if random.randint(0,3) != 0:
                flag = True
                while flag:
                    #Get random region to move the block to
                    end_ID = random.randint(0,22)
                    if end_ID != start_region.regionID:
                        flag = False
                #Make sure that the move to random region is legal
                while not board.check_path(block.movement_points, start_region.regionID, end_ID, block):
                    flag = True
                    while flag:
                        #Get new random region
                        end_ID = random.randint(0,22)
                        if end_ID != start_region.regionID:
                            flag = False
                #Move block
                print('Comp makes a move')
                board.move_block(block, start_region.regionID, end_ID, position)
                #print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)

            else:
                print("Computer passes")





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
        blocks_moved = []
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
         
            
            

            
            end = False
            for i in range(moveable_count):
                if end == False:
                    check_lst = list()
                    for block in focus_region.blocks_present:
                        check_lst.append(block.name)

                    block_name = ""
                    block = ''
                    end_region_name = ''
                    end_region = ''
                    end = False
                    focus_blocks = []
                    for x in focus_region.blocks_present:
                        focus_blocks.append(x.name)
                    while end == False and block_name not in check_lst:
                        block_name = input("Which block would you like to move from " + focus_region.name + " (Enter 'done' if done)?\n>").upper()
                        if block_name == 'DONE':
                            end = True
                        elif block_name in focus_blocks:
                            block = find_block.find_block(block_name, focus_region.blocks_present)

                            if block_name not in check_lst:
                                print("That block in not in the focus region!")
                            if block.name in blocks_moved:
                                print("You have already moved that block this turn!")
                                block_name = ''
                
                '''
                check = False
                if block_name == 'DONE':
                    check = True
                while check == False:
                    
                    end_region_name = input("What region would you like to move to?\n>")

                    if end_region_name.upper() in board.regionID_dict:
                        end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                        check = True
                prev_paths = []

                while end == False and not board.check_path(block.movement_points,focus_region.regionID, end_region.regionID, block):

                    end_region_name = input("What region would you like to move to?\n>")
                    #Make sure that the region name is actually a region name
                    if end_region_name.upper() in board.regionID_dict:
                        #Get the region object from the region name
                        end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                        #Make sure that the move is a valid move
                        
                '''
                #if board.move_block(block, focus_region.regionID, end_region.regionID,prev_paths, truce):
                        
                #Move the block to its location
                #Add the block to the moved blocks list
                if block_name != 'DONE':
                    blocks_moved.append(block.name)
                    board.move_block(block,focus_region.regionID, -1,position,prev_paths,truce)
                    #print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':
        #Get a random starting region
        
        moved_blocks = list()
        for i in range(2):
            start_regions = board.get_controlled_regions(role)
            rand_startID = random.randint(0, len(start_regions) - 1)
            start_region = start_regions[rand_startID]
        
            for block in start_region.blocks_present:
                if block not in moved_blocks:
                    if random.randint(0,3) != 0:
                        flag = True
                        while flag:
                            end_ID = random.randint(0,22)
                            if end_ID != start_region.regionID:
                                flag = False
                        while not board.check_path(block.movement_points, start_region.regionID, end_ID,block):
                            flag = True
                            while flag:
                                end_ID = random.randint(0,22)
                                if end_ID != start_region.regionID:
                                    flag = False
                            
                        print('Computer should move')
                        board.move_block(block, start_region.regionID, end_ID,position, prev_paths,truce)
                        moved_blocks.append(block)
                        #print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)
                    else:
                        print('Computer passes')


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
        blocks_moved = []
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
            
            end = False
            for i in range(moveable_count):
                if end == False:
                    check_lst = list()
                    for block in focus_region.blocks_present:
                        check_lst.append(block.name)

                    block_name = ""
                    block = ''
                    end_region_name = ''
                    end_region = ''
                    end = False
                    focus_blocks = []
                    for x in focus_region.blocks_present:
                        focus_blocks.append(x.name)
                    while end == False and block_name not in check_lst:
                        block_name = input("Which block would you like to move from " + focus_region.name + " (Enter 'done' if done)?\n>").upper()
                        if block_name == 'DONE':
                            end = True
                        elif block_name in focus_blocks:
                            block = find_block.find_block(block_name, focus_region.blocks_present)
                            if block_name not in check_lst:
                                print("That block in not in the focus region!")
                            if block.name in blocks_moved:
                                print("You have already moved that block this turn!")
                                block_name = ''
                
                '''
                check = False
                if block_name == 'DONE':
                    check = True
                while check == False:
                    
                    end_region_name = input("What region would you like to move to?\n>")

                    if end_region_name.upper() in board.regionID_dict:
                        end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                        check = True
                prev_paths = []

                while end == False and not board.check_path(block.movement_points,focus_region.regionID, end_region.regionID, block):

                    end_region_name = input("What region would you like to move to?\n>")
                    #Make sure that the region name is actually a region name
                    if end_region_name.upper() in board.regionID_dict:
                        #Get the region object from the region name
                        end_region = board.regions[board.regionID_dict[end_region_name.upper()]]
                        #Make sure that the move is a valid move
                        
                        '''
                #if board.move_block(block, focus_region.regionID, end_region.regionID,prev_paths, truce):
                        
                #Move the block to its location
                #Add the block to the moved blocks list
                if block_name != 'DONE':
                    blocks_moved.append(block.name)
                    board.move_block(block,focus_region.regionID, -1,position,prev_paths,truce)
                    #print(block.name + " was moved from " + focus_region.name + ' to ' + end_region.name)

    if position == 'comp':
        #Get a random starting region
        moved_blocks = list()
        for i in range(3):
            start_regions = board.get_controlled_regions(role)
            rand_startID = random.randint(0, len(start_regions) - 1)
            start_region = start_regions[rand_startID]

            for block in start_region.blocks_present:
                if block not in moved_blocks:
                    if random.randint(0,3) != 0:
                        flag = True
                        while flag:
                            end_ID = random.randint(0,22)
                            if end_ID != start_region.regionID:
                                flag = False
                        while not board.check_path(block.movement_points, start_region.regionID, end_ID, block):
                            flag = True
                            while flag:
                                end_ID = random.randint(0,22)
                                if end_ID != start_region.regionID:
                                    flag = False
                        print('Computer should move')
                        board.move_block(block, start_region.regionID, end_ID,position,prev_paths,truce)
                        moved_blocks.append(block)
                        #print('Computer moves ' + block.name + ' from ' + start_region.name + " to " + board.regions[end_ID].name)
                    else:
                        print("Computer passes")
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
    quitt = False
    if position == 'comp':
            #temporary for dumb AI
            #create and print a list of coastal, friendly regions where norse is not the ONLY one
        
        possible_region_list = []
        
        #loops through list of friendly, coastal, not just Norse regions to append to a possible_region_list
        for region in board.get_controlled_regions(role):
            coastal = False
            just_norse = False
            if region.coast:
                coastal = True
            if len(region.blocks_present) == 1 and region.blocks_present[0].name.upper() == 'NORSE':
                just_norse = True
            
            if coastal and not just_norse:
                possible_region_list.append(region)
        
        
        #loops through list of friendly, coastal regions to append to a possible_final_region_list
            possible_final_region_list = []
            for region in board.get_controlled_regions(role):                
                if region.coast:
                    possible_final_region_list.append(region)
        
        
        
        if len(possible_final_region_list) >= 2:
        
            #random region from possible list
            original_region = possible_region_list[random.randint(0, len(possible_region_list) - 1)]
            #remove the original region from the possible end regions
            possible_final_region_list.remove(original_region)
            
            #possible_block_list
            #list of possible blocks to move (present in region) and not norse
            possible_block_list = []
            for block in original_region.blocks_present:
                if block.name != 'NORSE':
                    possible_block_list.append(block)
            
            move_block_list = []
            blocks_moved = 0
            while blocks_moved < 2:
                block = original_region.blocks_present[random.randint(0, len(original_region.blocks_present)-1)]
                #if it's not already on the list,append to move_block_list
                if block not in move_block_list:
                    move_block_list.append(block)
                    blocks_moved+=1
                elif block in move_block_list and len(possible_block_list) == 1:
                    blocks_moved+=1
            
                    
                    
            new_region = possible_final_region_list[random.randint(0, len(possible_region_list) - 1)]
                
            for block in move_block_list:
        
                board.add_to_location(block, new_region)
                print(block.name + ' moved from ' + original_region.name + ' to ' + new_region.name)
        
        else:
            print('There are not enough friendly regions with which to play this card.')
                
            
        #add in if it's not possible
    elif position == 'opp':
          
           
        possible_region_list = []
        
        #loops through list of friendly, coastal, not just Norse regions to append to a possible_region_list
        for region in board.get_controlled_regions(role):
            coastal = False
            just_norse = False
            if region.coast:
                coastal = True
            if len(region.blocks_present) == 1 and region.blocks_present[0].name.upper() == 'NORSE':
                just_norse = True
            
            if coastal and not just_norse:
                possible_region_list.append(region)
        
        
        #loops through list of friendly, coastal regions to append to a possible_final_region_list
            possible_final_region_list = []
            for region in board.get_controlled_regions(role):                
                if region.coast:
                    possible_final_region_list.append(region)
        
        
        
        if len(possible_final_region_list) >= 2:
            
            print('Possible origin regions:')
            for region in possible_region_list:
                print(region.name)
        
            #user input region, check if in possible list
            valid_region = False
            while not valid_region:
                
                original_region_name = input('What region would you like to move block(s) from? Enter a name or \'none\'.\n>')
            
                if original_region_name.lower() != 'none':
            
                    original_region = search.region_name_to_object(board, original_region_name)
                
                    if original_region and original_region in possible_region_list:
                        valid_region = True
                    else:
                        print('Invalid region.')
                else:
                    quitt = True
                
            if not quitt:
                #remove the original region from the possible end regions
                possible_final_region_list.remove(original_region)
                
                #possible_block_list
                #list of possible blocks to move (present in region) and not norse
                possible_block_list = []
                for block in original_region.blocks_present:
                    if block.name != 'NORSE':
                        possible_block_list.append(block)
                
                print('Possible blocks:')
                for block in possible_block_list:
                    print(block.name)
                
                
                move_block_list = []
                blocks_moved = 0
                
                while blocks_moved < 2:
                    valid_block = False
                    
                    while not valid_block:
                        
                        
                        block_name = input('Which block would you like to move? Enter a name or \'none\'.\n>').upper()
                    
                        if block_name.lower() != 'none':
                            
                            block_to_move = search.block_name_to_object(possible_block_list, block_name)
                    
                            if block_to_move and block_to_move not in move_block_list:
                                valid_block = True
                                move_block_list.append(block)
                                blocks_moved+=1
                            
                            elif block in move_block_list and len(possible_block_list) == 1:
                                blocks_moved+=1
                                
                            else:
                                print('Invalid block.')
                                continue
                        else:
                            valid_block = True
                            quitt = True
                            
                            
                        if not quitt:
                                  
                            print('Possible final regions:')
                            for region in possible_final_region_list:
                                print(region.name)
                        
                            #user input region, check if in possible list
                            valid_region = False
                            while not valid_region:
                                
                                new_region_name = input('What region would you like to move block(s) to? Enter a name or \'none\'.\n>')
                            
                                if new_region_name.lower() != 'none':
                            
                                    new_region = search.region_name_to_object(board, new_region_name)
                                
                                    if new_region and new_region in possible_final_region_list:
                                        valid_region = True
                                    else:
                                        print('Invalid region.')
                                        continue
                                else:
                                    valid_region = True
                                    quitt = True
                                    
                            if not quitt:
                                        
                                for block in move_block_list:
                            
                                    board.add_to_location(block, new_region)
                                    print(block.name + ' moved from ' + original_region.name + ' to ' + new_region.name)
                    
        else:
                print('There are not enough friendly coastal regions with which to play this card.')
            
            
def her_execution(board, position, role):
    '''
    Activates the HERALD card.
    position:  'opp' or 'comp' - ai or player
    board:  Board object
    '''

    #List of available nobles to steal
    enemy_nobles = []
    if role == 'SCOTLAND':
        enemy_role = 'ENGLAND'
    else:
        enemy_role = 'SCOTLAND'

    for enemy_region in board.get_controlled_regions(enemy_role):
        for block in enemy_region.blocks_present:

            if type(block) == blocks.Noble and block.name != 'MORAY' and block.allegiance != role:
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
        rand_selection = random.randint(0,num_nobles-1)
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

        if len(noble_region.blocks_present) > 1:
            for block in noble_region.blocks_present:
                if block == noble_to_steal:
                    noble_region.combat_dict['Attacking'].append(block)
                else:
                    noble_region.combat_dict['Defending'].append(block)

            combat.battle(noble_region.combat_dict['Attacking'], noble_region.combat_dict['Defending'], list(), list(), board, role)

        #Move the noble to its own region - will sort it into attacker/defender
        #board.move_block(noble_to_steal, noble_region.regionID, noble_region.regionID, position)

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

            if search.region_name_to_object(board, selected_region_name):
                selected_region = search.region_name_to_object(board, selected_region_name)
                valid_input = True


            else:
                print('Invalid input. Please try again.')

        health_points = 3

        possible_blocks = list()

        for block in selected_region.blocks_present:
            if block.allegiance == role:
                possible_blocks.append(block)
        print('Possible blocks: ')

        for i, block in enumerate(possible_blocks):

            print(block.name, '[', i, ']', end = '\t')
        while health_points > 0:
            bad_input = True
            while bad_input:
                try:
                    print('You have ', health_points, ' health points remaining')
                    ID_to_heal = int(input('Which block index would you like to heal: '))
                    if ID_to_heal not in range(len(possible_blocks)):
                        print('Type in a valid block index')
                        continue
                    healing_points = int(input('How many health points would you like to heal it: '))
                    if healing_points <= 0 or healing_points > health_points:
                        print('You do not have that many healing points left')
                        continue
                except ValueError:
                    print('type in a number')
                    continue
                block_to_heal = possible_blocks[ID_to_heal]
                health_points -= block_to_heal.heal_until_full(healing_points)
                
                print(block_to_heal.name, ' got healed')
                bad_input = False



    #Computer
    elif position == 'comp':

        possible_blocks = list()

        
        ###
        ###
        ### RANDOM DECISION - TEMPORARY
        ###
        ###
        num_regions = len(friendly_list)
        rand_selection = random.randint(0, num_regions - 1)
        selected_region = friendly_list[rand_selection]

        for block in selected_region.blocks_present:
            if block.allegiance == role:
                possible_blocks.append(block)

        for i in range(3):
            rand_block_selection = random.randint(0, len(possible_blocks) - 1)
            possible_blocks[rand_block_selection].heal_until_full()
            print(possible_blocks[rand_block_selection].name, ' healed one point')

def pil_execution(board, position, role):
    
    if position == 'comp':
        
        #loop through regions to make sure there is a region that it works in
        for region_controlled in board.get_controlled_regions(role):
            new_list = []
            new_list.append(region_controlled.regionID)
            for neighbor_region in board.find_all_borders(new_list):
                if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                    possible = True
        
        if possible:
            
            #make a list of possible opponent regions to be pillaged 
            possible_pill_lst = []
            for region in board.get_controlled_regions(role):
                new_list = []
                new_list.append(region.regionID)
                for neighbor_region in board.find_all_borders(new_list):
                    if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                        possible_pill_lst.append(neighbor_region)
            
            
            chosen_subtract_region = possible_pill_lst[random.randint(0, len(possible_pill_lst) - 1)]
            
            
            # pillage combat-style
            points_pillaged = 0
            
            for x in range (0,2):
                highest_block_lst = combat.find_max_strength(chosen_subtract_region.blocks_present)
            
                if highest_block_lst:
                    block = highest_block_lst[0]
                    #strike once
                    block.get_hurt(1)
                    print(block.name + ' took one hit.')
                    points_pillaged+=1
                    
                    if block.is_dead():
                        if role == 'SCOTLAND':
                            board.eng_pool.append(block)
                            board.eng_roster.remove(block)
                        elif role == 'ENGLAND':
                            board.scot_pool.append(block)
                            board.scot_roster.remove(block)
                        
            
            
            
            #make a list of possible owned regions to gain points
            possible_add_lst = []
            new_list = []
            new_list.append(chosen_subtract_region.regionID)
            
            for neighbor_region in board.find_all_borders(new_list):
                if neighbor_region.is_friendly(role):
                    possible_add_lst.append(neighbor_region)
    
            #choose randomly from the list
            chosen_add_region = possible_add_lst[random.randint(0, len(possible_add_lst) - 1)]


            health_points = points_pillaged
        
            possible_add_block_list = []
            
            #list for possible blocks to heal in chosen_add_region
            for block in chosen_add_region.blocks_present:
                possible_add_block_list.append(block)
            
            while health_points > 0:

                block = possible_add_block_list[random.randint(0, len(possible_add_block_list) - 1)]
                healing_points = random.randint(0, block.attack_strength - block.current_strength)
                block.heal_no_return(healing_points)
                health_points -= healing_points
                print(block.name + ' was healed ' + str(healing_points) + ' points.')
   
        else:
            print('There are no possible regions in which to play this card.')
            
            
        
    elif position == 'opp':
        quitt = False
        #loop through regions to make sure there is a region that it works in
        for region_controlled in board.get_controlled_regions(role):
            new_list = []
            new_list.append(region_controlled.regionID)
            for neighbor_region in board.find_all_borders(new_list):
                if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                    possible = True
        
        if possible:
            
            #make a list of possible opponent regions to be pillaged 
            possible_pill_lst = []
            for region in board.get_controlled_regions(role):
                new_list = []
                new_list.append(region.regionID)
                for neighbor_region in board.find_all_borders(new_list):
                    if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral():
                        possible_pill_lst.append(neighbor_region)
            
            print('Possible pillaging regions: ')
            for region in possible_pill_lst:
                print(region.name)
            
            
            valid_region = False
            
            while not valid_region:
                chosen_subtract_region_name = input('Which of your opponent\'s regions would you like to remove points from? Enter a name or \'none\'\n>').upper()
                
                if chosen_subtract_region_name.lower() == 'none':
                    quitt = True
                
                if not quitt:
                    chosen_subtract_region = search.region_name_to_object(board, chosen_subtract_region_name)
                        
                    if chosen_subtract_region in possible_pill_lst:
                        valid_region = True
                        
                    else:
                        print('Invalid region.')
                        continue
            
                    # pillage combat-style
                    points_pillaged = 0
                    
                    for x in range (0,2):
                        highest_block_lst = combat.find_max_strength(chosen_subtract_region.blocks_present)
                    
                        if highest_block_lst:
                            block = highest_block_lst[0]
                            #strike once
                            block.get_hurt(1)
                            print(block.name + ' took one hit.')
                            points_pillaged+=1
                            
                            if block.is_dead():
                                if role == 'SCOTLAND':
                                    board.eng_pool.append(block)
                                    board.eng_roster.remove(block)
                                elif role == 'ENGLAND':
                                    board.scot_pool.append(block)
                                    board.scot_roster.remove(block)
                        
            
            
            
                    #make a list of possible owned regions to gain points
                    possible_add_lst = []
                    new_list = []
                    new_list.append(chosen_subtract_region.regionID)
                    
                    for neighbor_region in board.find_all_borders(new_list):
                        if neighbor_region.is_friendly(role):
                            possible_add_lst.append(neighbor_region)
                    
                    print('Possible regions to add pillaged points to: ')
                    for region in possible_add_lst:
                        print(region.name)
            
            
                    valid_region = False
                    
                    while not valid_region:
                        chosen_add_region_name = input('Which of your regions would you like to add pillaged points to? Enter a name or \'none\'\n>').upper()
                        
                        if chosen_add_region_name.lower() == 'none':
                            quitt = True
                        
                        if not quitt:
                            chosen_add_region = search.region_name_to_object(board, chosen_add_region_name)
                                
                            if chosen_add_region in possible_add_lst:
                                valid_region = True
                                
                            else:
                                print('Invalid region.')
                                continue
            
            
                
            
                            health_points = points_pillaged
                        
                            possible_add_block_list = []
                            
                            while health_points > 0:
                                
                                #list for possible blocks to heal in chosen_add_region
                                for block in chosen_add_region.blocks_present:
                                    possible_add_block_list.append(block)
                                        
                                print('Possible blocks to heal: ')
                                for block in possible_add_block_list:
                                    print(block.name)
                                print()
                                
                                valid_input = False
                                
                                while not valid_input:
                                    
                                    print('You have ', health_points, ' health points.')
                                    block_name = input('Which block would you like to heal? Enter a name or \'none\'\n>').upper()
                                    
                                    if block_name.lower() == 'none':
                                        quitt = True
                                    #if player doesnt enter 'none'
                                    if not quitt:
                                        block = search.block_name_to_object(chosen_add_region.blocks_present, block_name)
                                        
                                        if block in possible_add_block_list:
                                            valid_input = True
                                        else:
                                            print('Invalid block.')
                                            continue
                                            

                                        valid_in = False
                                        while not valid_in:
                
                                            healing_points = input('How many points would you like to heal it? Enter an integer or \'none\'\n>')
                                            if healing_points.lower() == 'none':
                                                quitt = True
                                                
                                            if not quitt:
                                                if healing_points.isdigit():
                                                    healing_points = int(healing_points)
                                                    if healing_points <= 0 or healing_points > health_points:
                                                        print('You do not have that many healing points.')
                                                    else:
                                                        block.heal_until_full(healing_points)
                                                        health_points -= healing_points
                                                        print(block.name + ' was healed ' + str(healing_points) + ' points.')
                                                        valid_in = True
                                                else:
                                                    print('Invalid input.')

       
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

        if resolve_card(board, 'comp',comp_card,comp_role) == True:

            resolve_card(board, 'opp', opp_card, opp_role,True)

        else:

            resolve_card(board, 'opp', opp_card, opp_role)

        
    elif not who_goes_first: #if opponent goes first
        

        if resolve_card(board, 'opp', opp_card, opp_role) == True:

            resolve_card(board, 'comp', comp_card, comp_role,True)

        else:

            resolve_card(board, 'comp', comp_card, comp_role)

        
    return who_goes_first, year_ends_early
