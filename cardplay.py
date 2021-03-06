#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:05:44 2018
Created on Tue Jul 24 15:05:44 2018

@author: amylvaganam
"""


import random
import combat
import dice
import search
import find_block
import blocks
import copy
import scottish_king
import comp_card_utilities
import move_utility
import weighted_prob

    
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

def select_comp_card(board, computer_hand, role): #role = 'ENGLAND' or 'SCOTLAND'
    prob_dict = dict()
    for card in computer_hand:
        if card == '1':
            value = 0.6
        elif card == '2':
            value = 0.6
        elif card == '3':
            value = 0.6
        elif card == 'SEA':
            value = comp_card_utilities.sea_utility(board, role)
        elif card == 'HER':
            value = comp_card_utilities.her_utility(board, role)
        elif card == 'VIC':
            value, vic_block_list = comp_card_utilities.vic_utility(board, role)
        elif card == 'PIL':
            value, region_to_pillage_ID, region_to_heal_ID = comp_card_utilities.pil_utility(board, role)
            pil_data = [region_to_pillage_ID, region_to_heal_ID]
        elif card == 'TRU':
            value = comp_card_utilities.tru_utility(board, role)
        
        prob_dict[card] = value
        
    chosen_card = weighted_prob.weighted_prob(prob_dict)

    print(role, computer_hand)
    print(role, 'plays', chosen_card)
    
    if chosen_card == '1' or chosen_card == '2' or chosen_card == '3' or chosen_card == 'TRU':
        return chosen_card, 0 #empty second parameter because it's unnecessary
    elif chosen_card == 'SEA':
        return chosen_card, 0 #empty parameter temp before strategy is coded in
    elif chosen_card == 'HER':
        return chosen_card, 0 #empty parameter temp before noble_to_steal strat
    elif chosen_card == 'VIC':
        return chosen_card, vic_block_list
    elif chosen_card == 'PIL':
        return chosen_card, pil_data

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

def movement_execution(board, position, role, num_moves, truce=False):
    '''
    
    '''



    #this is where I started implementing move_utility (david)
    blocks_moved = []
    if position == 'comp':
        i = 0
        move_found = False
        while not move_found:
            i += 1
            
            
            for j in range(num_moves):

                board = move_utility.good_move(board, num_moves, role, board.turn, truce, blocks_moved)
            move_found = True
            
            return None
            
        #input()



    #this is where I ended implementing move_utility (david)



    blocks_moved = []
    picked_regions = []
    move_pt = 1
    #Pick n regions to 
    while move_pt <= num_moves:
        #print("LOOPING AGAIN", move_pt, num_moves)
        #print(move_pt)
        #print (blocks_moved)

        focus_region = None
        
        try:
       
            if type(prev_paths) != tuple:
                prev_paths = []
            else:
                
                prev_paths = list(prev_paths)


        except UnboundLocalError:
            prev_paths = list()

     



        passed = False
        #FIND A FOCUS REGION AND PATH
        if position == 'opp':

            user_region_input = ''

            #Loop until valid input for a focus region.
            valid_region_input = False
            while not valid_region_input:

                #Take a region name input, then try to convert it into a region object
                user_region_input = input('Which region would you like to focus your movement (or pass)?\n>').strip().upper()

                if user_region_input.lower() == 'pass':
                    passed = True
                    break

                focus_region = search.region_name_to_object(board, user_region_input)

                #If it's actually a region - valid region name
                if focus_region:
                    #Inputted region is friendly and unique
                    if focus_region in board.get_controlled_regions(role) and focus_region not in picked_regions:
                        valid_region_input = True
                    #Not friendly or neutral
                    else:
                        print('Invalid region. Please select a region you control that hasn\'t been moved.\n>')
                
                #Invalid region name
                else:
                    print('Invalid input. Please input a valid region name.\n>')



        elif position == 'comp':
            if move_pt == 1:
                print('First move:')
            elif move_pt == 2:
                print('Second move:')
            elif move_pt == 3:
                print('Third move:')

            unique_region = False
            while not unique_region:

                friendly_regions = board.get_controlled_regions(role)
                if len(friendly_regions) > 1:
                    rand_startID = random.randint(0, len(friendly_regions) - 1)
                else:
                    rand_startID = 0
                focus_region = friendly_regions[rand_startID]

                if focus_region not in picked_regions:
                    unique_region = True
            print(role + ' selected ' + focus_region.name + ' to move from.')

        if passed:
            move_pt += 1
            print(role + ' passed a movement point.')
            continue

        if focus_region.name != 'ENGLAND':
            
            picked_regions.append(focus_region)
        #assigns moveable count for contested regions

        if focus_region.is_contested():

            num_enemy = len(focus_region.combat_dict['Attacking'])

            num_friends = len(focus_region.combat_dict['Defending'])

            moveable_count = num_friends - num_enemy

        #assigns moveable count for 
        else:

            moveable_count = len(focus_region.blocks_present)

        if focus_region.name == 'ENGLAND' and num_moves > move_pt:

            print('Blocks in ENGLAND: each block requires one movement point.')
            for block in focus_region.blocks_present:
                print(block)

            if position == 'opp':

                valid_block = False

                while not valid_block and num_moves > move_pt:

                    user_block_name = input("Choose a block to move (type 'done' if done): ").strip().upper()

                    if user_block_name == "DONE":

                        print (role + ' chose not to move a block and passed a movement point.')

                        valid_block = True

                    user_block = search.block_name_to_object(board.all_blocks, user_block_name)

                    if user_block:

                        if user_block in focus_region.blocks_present:

                            if user_block not in blocks_moved:
                
                                if board.move_block(user_block,focus_region.regionID,position='opp',prev_paths=prev_paths,is_truce=truce) == False:

                                    print ("That path was not valid!")

                                else:
                                    #move_pt +=1
                                    prev_paths = tuple(prev_paths)


                                    blocks_moved.append(user_block)

                                    valid_block = True

                          

                            else:

                                print ("You have already moved that block this turn!")

                        else:

                            print ("That block is not in the region!")

                    else:

                        print ("Please input a valid block name!")

            elif position == 'comp':

                computer_choice = random.randint(0,100)

                if computer_choice == 0:

                    print (role + " passes a Movement Point")

                else:


                    for block in focus_region.blocks_present:
                        if num_moves > move_pt:
                            possible_paths = board.check_all_paths(block.movement_points,focus_region.regionID,block,all_paths = [], truce=truce)

                            if possible_paths:
                                print(role + ' may take the following paths from its selected region:')
                                print(possible_paths)
                                computer_path1 = random.choice(possible_paths)

                                end = computer_path1[-1]

                                board.move_block(block,focus_region.regionID,end=end,position='comp',prev_paths=prev_paths,is_truce=truce, path = computer_path1)

                                move_pt +=1
                            else:

                                print("Computer chosen region has no moves from its selected region.")

        else:
            count = 0
            can_go_again = True
            for i in range(moveable_count):

                if position == 'opp' and can_go_again:

                    valid_block = False

                    while not valid_block:

                        user_block_name = input("Choose a block to move (type 'done' if done): ").strip().upper()

                        if user_block_name == "DONE":

                            print (role + ' chose not to move a block and passed a movement point.')

                            valid_block = True

                        user_block = search.block_name_to_object(board.all_blocks, user_block_name)

                        if user_block:

                            if user_block in focus_region.blocks_present:

                                if user_block not in blocks_moved:

                                    if board.move_block(user_block,focus_region.regionID,position='opp',prev_paths=prev_paths,is_truce=truce) == False:

                                        print ("That path was not valid!")

                                    else:
                                        

                                        if combat.find_location(board, user_block).name == 'ENGLAND':
                                            can_go_again = False
                                            picked_regions.remove(focus_region)
                                        blocks_moved.append(user_block)

                                        valid_block = True

                                else:

                                    print ("You have already moved that block this turn!")

                            else:

                                print ("That block is not in the region!")

                        else:

                            print ("Please input a valid block name!")

                

                elif position == 'comp' and can_go_again:
                    #input('Computer Move Part 2')
                    print('It is computer turn to make a move')

                    computer_choice = random.randint(0,100)
                    
                    if computer_choice == 0:

                        print ("Computer Passes a Movement Point")

                    else:
                        possible_paths_2 = list()
                        
                        block_index = i - count
                        block = focus_region.blocks_present[block_index]

                        if block not in blocks_moved:
                            possible_paths_2 = board.check_all_paths(block.movement_points,focus_region.regionID,block,path=[], all_paths=[],truce=truce, role = role)

                            
                            #print("CHECK PATHS", board.check_all_paths(block.movement_points,focus_region.regionID,block,truce=truce))
                            if possible_paths_2:

                                computer_paths_1 = copy.deepcopy(random.choice(possible_paths_2))
                                #print(possible_paths_2)
                                end = computer_paths_1[-1]
                                

                                board.move_block(block,focus_region.regionID,end=end,position='comp',prev_paths=prev_paths,is_truce=truce, path = computer_paths_1)
                                if board.regions[end].name == 'ENGLAND':
                                    prev_paths = tuple(prev_paths)
                                    can_go_again = False
                                    picked_regions.remove(focus_region)
                                else:
                                    if type(prev_paths) == list:
                                        prev_paths.append(computer_paths_1)
                                count+=1
                                blocks_moved.append(block)
        #print(can_go_again)
        move_pt+=1

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
        #print(1)
            #temporary for dumb AI
            #create and print a list of coastal, friendly regions where norse is not the ONLY one
        
        possible_region_list = []
        
        #loops through list of friendly, coastal, not just Norse regions to append to a possible_region_list
        for region in board.get_controlled_regions(role):
            #print(2)
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
                #print(3)               
                if region.coast:
                    possible_final_region_list.append(region)
        
        
        
        if len(possible_final_region_list) >= 2:
            #if you want to add in last-min strategy, do it here
            #random region from possible list
            england = board.regions[22]
            if england in possible_region_list:
                original_region = england
            else:
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
            #print(4)

            while blocks_moved < 2:
                #print(5)
                block = possible_block_list[random.randint(0, len(possible_block_list)-1)]
                #if it's not already on the list,append to move_block_list
                if block not in move_block_list:
                    move_block_list.append(block)
                    blocks_moved+=1
                elif block in move_block_list and len(possible_block_list) == 1:
                    blocks_moved+=1
                else:
                    print('neither condition was met so this is an infinite loop')
            
                    
            #print(6)    
            new_region = possible_final_region_list[random.randint(0, len(possible_final_region_list) - 1)]
                
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
                
                original_region_name = input('What region would you like to move block(s) from? Enter a name or \'none\'.\n>').upper()
            
                if original_region_name != 'NONE':
            
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
                quittt = False
                block_name = ''
                while blocks_moved < 2 and not quittt:
                    if block_name != 'NONE':
                        valid_block = False
                    while not valid_block:
                        
                        
                        block_name = input('Which block would you like to move? Enter a name or \'none\'.\n>').upper()
                    
                        if block_name != 'NONE':
                            
                            block_to_move = search.block_name_to_object(possible_block_list, block_name)
                    
                            if block_to_move and block_to_move not in move_block_list:
                                valid_block = True
                                move_block_list.append(block_to_move)
                                blocks_moved+=1
                            
                            elif block in move_block_list and len(possible_block_list) == 1:
                                blocks_moved=1
                                
                            else:
                                print('Invalid block.')
                                continue
                        else:
                            valid_block = True
                            if len(move_block_list) == 1:
                                quittt = True
                quitt = False
                if len(move_block_list) > 0:              
                    print('Possible final regions:')
                    for region in possible_final_region_list:
                        print(region.name)
                
                    #user input region, check if in possible list
                    valid_region = False
                    while not valid_region:
                        
                        new_region_name = input('What region would you like to move block(s) to? Enter a name or \'none\'.\n>').upper()
                    
                        if new_region_name != 'NONE':
                    
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
            
            
def her_execution(board, position, role, eng_type, scot_type):
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
                    

            if not valid_input:
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

        print('Success')
        print(noble_to_steal.name, 'changed allegiance.' )

        #Find the noble's region
        noble_region = combat.find_location(board, noble_to_steal)



        if len(board.regions[noble_region.regionID].blocks_present) > 1:
            for block in noble_region.blocks_present:
                if block == noble_to_steal:
                    print(block.name + ' added to attacking dict')
                    board.regions[noble_region.regionID].combat_dict['Attacking'].append(block)
                else:
                    print(block.name + ' added to defending dict')
                    board.regions[noble_region.regionID].combat_dict['Defending'].append(block)

            print('DID HERALD BATTLE IN HERALD FUNCTION')
            board.regions[noble_region.regionID].combat_dict['Attacking'][0].change_allegiance()
            combat.battle(board.regions[noble_region.regionID].combat_dict['Attacking'], board.regions[noble_region.regionID].combat_dict['Defending'], list(), list(), board, eng_type, scot_type)

        #Move the noble to its own region - will sort it into attacker/defender
        #board.move_block(noble_to_steal, noble_region.regionID, noble_region.regionID, position)

    else:
        print('Failure')


def vic_execution(board, position, role, vic_block_list):
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

       #below is random decision
        """
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
            
        """
        
        #below is strategized decision:
        for block in vic_block_list:
            block.heal_until_full()
            print(block.name, ' healed one point')

def pil_execution(board, position, role, pil_data):

    print(role)
    
    if position == 'comp':
        """
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
                    if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral() and neighbor_region not in possible_pill_lst:
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
                        print(block.name, 'goes to the pool')
                        if role == 'SCOTLAND':
                            board.eng_pool.append(block)
                            board.eng_roster.remove(block)
                            board.remove_from_region(block, chosen_subtract_region.regionID)
                        elif role == 'ENGLAND':
                            board.scot_pool.append(block)
                            board.scot_roster.remove(block)
                            board.remove_from_region(block, chosen_subtract_region.regionID)
                        
            
            
            
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
                healing_points = random.randint(0, health_points)
                block.heal_until_full(healing_points)
                health_points -= healing_points
                print(block.name + ' was healed ' + str(healing_points) + ' points.')
   
        else:
            print('There are no possible regions in which to play this card.')
        """
        
        #this is strategized, receives chosen region IDs from utility:
        region_to_pil_id = pil_data[0]
        region_to_heal_id = pil_data[1]
        region_to_pil = search.region_id_to_object(board, region_to_pil_id)
        region_to_heal = search.region_id_to_object(board, region_to_heal_id)
        
        #pillage combat style
        points_pillaged = 0
        good_list = True
        for block in region_to_pil.blocks_present:
            if block.current_strength > 0:
                good_list = True
            else:
                good_list = False
        for x in range (0,2):
            if len(region_to_pil.blocks_present) != 0 and good_list:
                highest_block_lst = combat.find_max_strength(region_to_pil.blocks_present)
            else:
                highest_block_lst = False

            if highest_block_lst:
                block = highest_block_lst[0]
                #strike once
                block.get_hurt(1)
                print(block.name + ' took one hit.')
                points_pillaged+=1
                
                if block.is_dead():
                    print(block.name + ' has been pillaged to death')
                    board.kill_block(block, role)
    
        #use weighted prob to choose blocks to add pts to
        #for block in blocks_present
        
        block_val_dict = dict()
            
            #list for possible blocks to heal in chosen_add_region
        for block in region_to_heal.blocks_present:
            utility_value = 0.0000000001
            if block.name == 'KING' and block.current_strength < block.attack_strength:
                utility_value += .5
                #if block is wallace and he needs it
            elif block.name == 'WALLACE' and block.current_strength < block.attack_strength:
                utility_value += .4
            #for england:
            #if block is edward and he needs it
            if block.name == 'EDWARD' and block.current_strength < block.attack_strength:
                utility_value += .45
            #if block is hobelars and he needs it
            elif block.name == 'HOBELARS' and block.current_strength < block.attack_strength:
                utility_value += .3
                
            #if block is type noble and he needs it
            elif type(block) == blocks.Noble and block.current_strength < block.attack_strength:
                utility_value += .25
            #if block is below full health
            elif block.current_strength < block.attack_strength:
                utility_value += .1
            
            block_val_dict[block.name] = utility_value
            
        #possible healing pts = # pts taken from other region
        health_points = points_pillaged
        
        while health_points > 0 and len(region_to_heal.blocks_present) > 0:

                #should i add something here so it doesn't choose the same blocks???
                block_name = weighted_prob.weighted_prob(block_val_dict)
                healing_points = random.randint(0, health_points)
                block.heal_until_full(healing_points)
                health_points -= healing_points
                print(block.name + ' was healed ' + str(healing_points) + ' points.')
                
        
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
                        if not neighbor_region in possible_pill_lst:
                            possible_pill_lst.append(neighbor_region)
            
            print('Possible pillaging regions: ')
            for region in possible_pill_lst:
                print(region.name)
            
            
            valid_region = False
            
            while not valid_region:
                chosen_subtract_region_name = input('Which of your opponent\'s regions would you like to remove points from? Enter a name or \'none\'\n>').upper()
                
                if chosen_subtract_region_name.lower() == 'none':
                    quitt = True
                    valid_region = True
                
                if quitt:
                    valid_region = True
                else:
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
                                board.kill_block(block, role)
                        
            
            
            
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
                            valid_region = True
                        
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
                                        valid_input = True
                                        health_points = 0
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
                                                valid_in = True
                                                
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

def play_pass(which_side):
    """
    prompts user if they want to play or pass event card.
    if comp, automatically plays.
    returns 'play' or 'pass'
    """

    if which_side == 'opp':
    
        bad_input = True
        while bad_input:
            play_pass = input('Would you like to play the event card or pass it? (play/pass)')
            if play_pass.lower() != 'play' and play_pass.lower() != 'pass':
                print('type in play or pass')
            else:
                bad_input = False
                return play_pass.lower()
    
    else:
    
        return 'play'
            
def resolve_card(board, eng_type, scot_type, card, role, parameter, truce = False):
    
    """
    Takes in a string that lists side (comp/opp), the card for that side, and the role (england/scotland)
    based on string value of card, calls a function to execute the card itself
    
    """

    if role == 'ENGLAND':
        which_side = eng_type
    elif role == 'SCOTLAND':
        which_side = scot_type


    if card == '1':
        movement_execution(board, which_side, role, int(card), truce)
    elif card == '2':
        movement_execution(board, which_side, role, int(card), truce)
    elif card == '3':
        movement_execution(board, which_side, role, int(card), truce)

    else:

        if role == 'ENGLAND' or not scottish_king.run_king(board, eng_type, scot_type):
            
        
            
            if card == 'SEA':
                
                if play_pass(which_side) == 'play':
                    sea_execution(board, which_side, role)
                
                
            elif card == 'HER':
                
                if play_pass(which_side) == 'play':
                    her_execution(board, which_side, role, eng_type, scot_type)
                
                
            elif card == 'VIC':
                if play_pass(which_side) == 'play':
                    vic_execution(board, which_side, role, parameter)
                
                
            elif card == 'PIL':
                
                if play_pass(which_side) == 'play':
                    pil_execution(board, which_side, role, parameter)
                
                
            elif card == 'TRU':
                
                if play_pass(which_side) == 'play':
                    return True
               
    
            
def compare_cards(board, eng_card, scot_card, eng_type, scot_type, eng_parameter, scot_parameter):
    """
    takes the opponent card, computer card, and computer allegiance (ENGLAND/SCOTLAND)
    compares cards for which side plays their turn first
    returns True for computer going first, False for opponent first
    """


    
    year_ends_early = False

    
    if get_card_val(eng_card) > get_card_val(scot_card):
        who_goes_first = 'ENGLAND'
        
    elif get_card_val(eng_card) < get_card_val(scot_card):
        who_goes_first = 'SCOTLAND'
        
    elif get_card_val(eng_card) == get_card_val(scot_card):
     
        who_goes_first = 'ENGLAND'
        
        if get_card_val(eng_card) == 4 and get_card_val(scot_card) == 4:
            year_ends_early = True
        
    board.who_goes_first = who_goes_first

    eng_played_truce = False
    if eng_card == 'TRU':
        eng_played_truce = True

    scot_played_truce = False
    if scot_card == 'TRU':
        scot_played_truce = True

    if who_goes_first == 'ENGLAND':

        resolve_card(board, eng_type, scot_type, eng_card, 'ENGLAND', eng_parameter, scot_played_truce)
        resolve_card(board, eng_type, scot_type, scot_card, 'SCOTLAND', scot_parameter, eng_played_truce)
        
    elif who_goes_first == 'SCOTLAND':
        
        resolve_card(board, eng_type, scot_type, scot_card, 'SCOTLAND', scot_parameter, eng_played_truce)
        resolve_card(board, eng_type, scot_type, eng_card, 'ENGLAND', eng_parameter, scot_played_truce)
        
    return who_goes_first, year_ends_early

