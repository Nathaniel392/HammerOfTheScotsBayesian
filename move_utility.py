import retreat
import random
import weighted_prob
import copy
import simulations
import other_movement
import input_toggle
def clean_up_board(board1):
    '''
    This function is a function that is meant
    to loop through all regions of the board
    and remove blocks that are dead and should
    not be present on the board.
    '''
    for region in board1.regions:
        for block in region.blocks_present:
            if block.current_strength == 0:

                board1.regions[region.regionID].blocks_present.remove(block)

                if block in board1.eng_roster:
                    board1.eng_roster.remove(block)
                if block in board1.scot_roster:
                    board1.scot_roster.remove(block)
                if block not in board1.eng_pool and block.allegiance == 'ENGLAND' and not block.has_cross:
                    board1.eng_pool.append(block)
                if block not in board1.scot_pool and block.allegiance == 'SCOTLAND' and not block.has_cross:
                    board1.eng_pool.append(block)

    return board1
def clean_up_dict(region):

    for key in region.combat_dict:
        for block in region.combat_dict[key]:

            if block.current_strength <= 0:
                #print("THIS BLOCK SHOULD NOT BE HERE!!!!!", block)
                region.combat_dict[key].remove(block)
                if block in region.blocks_present:
                    region.blocks_present.remove(block)

    return region
def set_up_combat_dict(current_board, battle_region):
    battle_regionID = battle_region.regionID

    battle_region = current_board.regions[battle_regionID]

    for i,region in enumerate(current_board.regions):
        current_board.regions[i].combat_dict = {'Attacking':[], 'Defending':[], 'Attacking Reinforcements':[], 'Defending Reinforcements':[]}

    has_defenders = False
    defending_path = None
    defending_allegiance = None

    for block in battle_region.blocks_present:


        if not battle_region.is_block_enterer(block):
            current_board.regions[battle_regionID].combat_dict['Defending'].append(block)
            has_defenders = True
            defending_allegiance = block.allegiance

    if not has_defenders:
        first_block,defending_path = battle_region.find_first_enterer()
        current_board.regions[battle_regionID].combat_dict['Defending'].append(first_block)
        defending_allegiance = first_block.allegiance

    attacking_path = None
    for role in battle_region.enterers:
        for path in battle_region.enterers[role]:
            for block,order in battle_region.enterers[role][path]:

                if has_defenders or block != first_block:
                    if block.allegiance != defending_allegiance:
                        if len(current_board.regions[battle_regionID].combat_dict['Attacking']) == 0 or path == attacking_path:
                            current_board.regions[battle_regionID].combat_dict['Attacking'].append(block)
                            attacking_path = path
                        else:
                            current_board.regions[battle_regionID].combat_dict['Attacking Reinforcements'].append(block)
                    else:
                        if path == defending_path:
                            current_board.regions[battle_regionID].combat_dict['Defending'].append(block)
                        else:
                            current_board.regions[battle_regionID].combat_dict['Defending Reinforcements'].append(block)


def good_move(board, num_moves, role, turn, truce, blocks_moved):
    
    """
    board is a copy of the board
    going to make a move with copies of the board 
    goes and makes the move
    role is scotland or england
    turn is 1 2 3 4 or 5
    finds some utility and throws into random number generator to see if move chosen or not





    READ ME READ ME READ ME READ ME READ ME READ ME
    MAKES A COPY OF THE BOARD DOES THE MOVE EVALUATES THE MOVE IF BAD MOVE AGAIN AND CONTINUE LOOPING
    UNTIL FINDS GOOD MOVE AND THEN IT EXECUTES IT ON THE ACTUAL BOARD
    """

    board_copy = copy.deepcopy(board)


    utility = 0


    #count how man value of location of homes owned before:

    value_loc_before = 0
    for region in board_copy.regions:
        
        value_loc_before += retreat.value_of_location(board_copy, region.regionID, role)

    computer_block = None
    
    #does movement
    
    while computer_block in blocks_moved or computer_block == None:
        computer_path, computer_block = other_movement.movement_execution(board_copy, 'comp', role, num_moves, truce=truce)


    #debugging why things aren't in combat dictionary
    #for region in board.regions:
        #if region.is_contested():
            #for block in region.blocks_present:
                #if block not in 
    

    #checks utilitiy of the battles using the retreat elliot's thing
    noble_home_after = 0
    for i,region in enumerate(board_copy.regions):
        if region.is_contested():
            board_copy.regions[i] = clean_up_dict(region)
            #board_copy.regions[contested_regions[i].regionID] = contested_regions[i]
    board_copy = clean_up_board(board_copy)
    for region in board_copy.regions:
        if region.is_contested():
            '''
            
            print("***ATTACKING***")
            print(region.combat_dict['Attacking'])
            print("******")
            print("***DEFENDING***")
            print(region.combat_dict['Defending'])
            print("******")
            print('attack reinforcements')
            print(region.combat_dict['Attacking Reinforcements'])
            print('defense reinforcements')
            print(region.combat_dict['Defending Reinforcements'])
            '''
            
            combat_dict = copy.deepcopy(region.combat_dict)
            #print('IN COMPUTER:',combat_dict)
            #print('REGION IS: ', region)
            #print('ENTERERS:', region.enterers)
            #print(region.is_contested())

            set_up_combat_dict(board_copy, region)
            #print('AFTER:',board_copy.regions[region.regionID].combat_dict)
            simulation_dict = simulations.simulation(region.combat_dict['Attacking'], region.combat_dict['Defending'], 1000, \
                region.combat_dict['Attacking Reinforcements'], region.combat_dict['Defending Reinforcements'])
            '''
            print("***ATTACKING***")
            print(region.combat_dict['Attacking'])
            print("******")
            print("***DEFENDING***")
            print(region.combat_dict['Defending'])
            print("******")

            #for key in region.combat_dict:
                #print(region.combat_dict[key])
            '''
            

            if len(combat_dict['Attacking']) > 0:
                if role == combat_dict['Attacking'][0].allegiance:
                    is_attacking = True
                else:
                    is_attacking = False
                utility += retreat.retreat(board_copy, region.regionID, [], simulation_dict, is_attacking, turn,combat_dict)['Staying value '] * 4
        


    #account for difference in locations owned values
    value_loc_after = 0
    for region in board_copy.regions:
        
        value_loc_after += retreat.value_of_location(board_copy, region.regionID, role)

    utility += (value_loc_after - value_loc_before) * 2


    #throw in the random number generator with some base bad_move_utility
    #'move' is a substitute for whatever the move will be stored in later
    bad_move_utility = 3.5

    if utility <= 0:
        utility = .01

    

    utility_dict = {'move': utility, 'not move': bad_move_utility}

    if weighted_prob.weighted_prob(utility_dict) == 'move':
    #if utility > bad_move_utility:
        #total_string = ''
        #pause
        input_toggle.toggle_input('movement')
        print('computer ready to make a move')

        #input()
        if computer_path[0] != computer_path[-1] and computer_block in board.regions[computer_path[0]].blocks_present:
            board.move_block(computer_block,computer_path[0], end = computer_path[-1], position='comp', is_truce=truce, path = computer_path)
        else:
            print('Computer passes a movement point')
        other_movement.reset_total_string()
        print('computer done with move\n')
        #input_toggle.toggle_input('movement')
        #input()
        return board
    else:
        
    
        
        return good_move(board, num_moves, role, turn, truce, blocks_moved)



