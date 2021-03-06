#very sorry for the global variable
#it is up to sid to fix it
import search
import random
import copy
total_string = ''
def reset_total_string():
    global total_string
    total_string = ''
def add_to_total_string(*args):
    global total_string
    for thing in args:
        if type(thing) != str:
            total_string += ' ' + str(thing) + ' '
        else:
            total_string += thing
    total_string += '\n'
def print_total_string():
    global total_string
    print(total_string)

def skip_input(*args):
    pass


def move_block(board, block, start, end = -1, position = 'comp', prev_paths = [], is_truce = False):
        '''
        Changes a block's location on the board, assuming that all conditions are legal. 
        Adds them to appropriate dictionaries if in a combat or attack scenario

        Takes a list of all previous paths taken in that turn
        Takes a position -- computer or opponent

        block:  
        start:  starting location (Region ID)
        end:  end location (Region ID)
        '''
        
        block_to_return = None
        
        paths = board.check_path(block.movement_points,start,end, block, all_paths = list())

        if position == 'comp' and type(paths[0]) == list:
           


            #Find every path from the start regionID to the end regionID and put them in a list



            #debugging why type int have no thing len()
            #print('START', start)
            #print('END', end)
            #print('PATHS', paths)
            for path in paths:
                if type(path) != list:
                    
                    raise Exception('here is where it"s not being a list')





            #end debugging

            #add_to_total_string(paths)
            #If valid paths exist, keep going
            if paths:

               
                computer_path = random.choice(paths)
                add_to_total_string('computer chose ' + str(computer_path))


                path_taken = False



                for path in prev_paths:

                    if path == computer_path:

                        path_taken = True

                        break

                #If the final region in the path is contested
                if board.regions[end].is_contested():

                    if tuple(path) not in board.regions[end].enterers[block.allegiance]:
                        board.regions[end].enterers[block.allegiance][tuple(path)] = []
                    number_enterers = board.regions[end].get_number_enters()
                    board.regions[end].enterers[block.allegiance][tuple(path)].append((block,number_enterers+1))

                    #Remove the block from its starting location
                    board.regions[start].blocks_present.remove(block)

                    #Move it to the correct dictionary list
                    if board.regions[end].blocks_present[0].allegiance != block.allegiance and path_taken: 
                        board.regions[end].combat_dict['Attacking'].append(block)
                    
                    elif board.regions[end].blocks_present[0].allegiance != block.allegiance and board.regions[end].name == 'ENGLAND' and path_taken:
                        board.regions[end].combat_dict['Attacking'].append(block)

                    elif board.regions[end].blocks_present[0].allegiance != block.allegiance:
                        board.regions[end].combat_dict['Attacking Reinforcements'].append(block)
                        board.attacked_borders[computer_path[-2]][end] = 'attack'
                    
                    else:
                        board.regions[end].combat_dict['Defending Reinforcements'].append(block)
                        board.attacked_borders[computer_path[-2]][end] = 'defense'

                    #Add it to the region's overall block list as well
                    board.regions[end].blocks_present.append(block)

                  
                    add_to_total_string(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)

                #End location is not contested

                else:

                    #If it's an enemy controlled region
                    if len(board.regions[end].blocks_present) != 0 and board.regions[end].blocks_present[0].allegiance != block.allegiance:

                        if tuple(path) not in board.regions[end].enterers[block.allegiance]:
                            board.regions[end].enterers[block.allegiance][tuple(path)] = []
                        number_enterers = board.regions[end].get_number_enters()
                        board.regions[end].enterers[block.allegiance][tuple(path)].append((block,number_enterers+1))

                        #Stop the function if it's truce
                        if is_truce:
                            add_to_total_string("You can't move there fool, issa truce")
                            return False
              
                        #Set the defending blocks into the defending dictionary
                        for defending_block in board.regions[end].blocks_present:
                            board.regions[end].combat_dict['Defending'].append(defending_block)

                        #Move the attacking into the attacking dictionary
                        board.regions[end].combat_dict['Attacking'].append(block)
                        board.regions[end].blocks_present.append(block)
                        board.regions[start].blocks_present.remove(block)

                        
                        if not path_taken:
                            if type(prev_paths) != list:
                                prev_paths = list(prev_paths)
                                
                            prev_paths.append(computer_path)
                            


                            if computer_path[-1] == 22 or computer_path[0] == 22:
                                #if set don't change it in cardplay
                                prev_paths = tuple(prev_paths)

                        
                
                        add_to_total_string(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)

                        #Set the border between the last and second to last region in the path to attacked



                        ###temporary
                
                        ###
                        board.attacked_borders[computer_path[-2]][end] = 'attack'



                    #Friendly or neutral
                    else:

                        if tuple(path) not in board.regions[end].enterers[block.allegiance]:
                            board.regions[end].enterers[block.allegiance][tuple(path)] = []
                        number_enterers = board.regions[end].get_number_enters()
                        board.regions[end].enterers[block.allegiance][tuple(path)].append((block,number_enterers+1))
                        
                        board.regions[start].blocks_present.remove(block)
                        board.regions[end].blocks_present.append(block)
                        
                        add_to_total_string(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)

                #Decrement the border limits of each border in the path
                for i in range(len(computer_path)-2):
                    board.dynamic_borders[computer_path[i]][computer_path[i+1]] -= 1

            #No valid paths
            else:
                return False

        


def movement_execution(board, position, role, num_moves, truce=False):
    '''
    
    '''



   



    blocks_moved = []
    picked_regions = []
    computer_paths_1 = []
    move_pt = 0
    block_to_return = None
    #Pick n regions to 
    while move_pt < num_moves:
        
        #add_to_total_string(move_pt)
        #add_to_total_string (blocks_moved)

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

            user_region_skip_input = ''

            #Loop until valid skip_input for a focus region.
            valid_region_skip_input = False
            while not valid_region_skip_input:

                #Take a region name skip_input, then try to convert it into a region object
                user_region_skip_input = skip_input('Which region would you like to focus your movement (or pass)?\n>').strip().upper()

                if user_region_skip_input.lower() == 'pass':
                    passed = True
                    break

                focus_region = search.region_name_to_object(board, user_region_skip_input)

                #If it's actually a region - valid region name
                if focus_region:
                    #skip_inputted region is friendly and unique
                    if focus_region in board.get_controlled_regions(role) and focus_region not in picked_regions:
                        valid_region_skip_input = True
                    #Not friendly or neutral
                    else:
                        add_to_total_string('Invalid region. Please select a region you control that hasn\'t been moved')
                
                #Invalid region name
                else:
                    add_to_total_string('Invalid skip_input. Please skip_input a valid region name.')



        elif position == 'comp' and board.get_controlled_regions(role):
            
            skip_input('Computer Move Part 1')
            ###
            ###TEMPORARY
            ###

            #Get a random starting region
            
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
    
        if focus_region == None:
            passed = True
        if passed:
            move_pt += 1
            continue

        if focus_region.name != 'ENGLAND':
            
            picked_regions.append(focus_region)
        #assigns moveable count for contested regions
        #print(focus_region.is_contested())
        if focus_region.is_contested():

            num_enemy = len(focus_region.combat_dict['Attacking'])

            num_friends = len(focus_region.combat_dict['Defending'])

            moveable_count = num_friends - num_enemy

        #assigns moveable count for 
        else:

            moveable_count = len(focus_region.blocks_present)

        if focus_region.name == 'ENGLAND' and num_moves > move_pt:

            add_to_total_string(focus_region.blocks_present)

            if position == 'opp':

                valid_block = False

                while not valid_block and num_moves > move_pt:

                    user_block_name = skip_input("Choose a block to move (type 'done' if done): ").strip().upper()

                    if user_block_name.lower() == "done":

                        add_to_total_string ("You passed one movement point!")

                        valid_block = True

                    board_blocks = board.eng_roster + board.scot_roster
                    user_block = search.block_name_to_object(board_blocks, user_block_name)

                    if user_block:

                        if user_block in focus_region.blocks_present:

                            if user_block not in blocks_moved:

                                if move_block(board, user_block,focus_region.regionID,position='opp',prev_paths=prev_paths,is_truce=truce) == False:

                                    add_to_total_string ("That path was not valid!")

                                else:
                                    #move_pt +=1
                                    prev_paths = tuple(prev_paths)


                                    blocks_moved.append(user_block)

                                    valid_block = True

                          

                            else:

                                add_to_total_string ("You have already moved that block this turn!")

                        else:

                            add_to_total_string ("That block is not in the region!")

                    else:

                        add_to_total_string ("Please skip_input a valid block name!")

            elif position == 'comp':

              

                computer_choice = random.randint(0,100)

                if computer_choice == 0:
                    pass
                   

                else:


                    for block in focus_region.blocks_present:
                        if num_moves > move_pt:
                            possible_paths = board.check_all_paths(block.movement_points,focus_region.regionID,block,all_paths = [], truce=truce)

                            if possible_paths:
                                add_to_total_string(possible_paths)
                                computer_paths_1 = random.choice(possible_paths)

                                end = computer_paths_1[-1]

                                move_block(board, block,focus_region.regionID,end=end,position='comp',prev_paths=prev_paths,is_truce=truce)
                                block_to_return = block
                                move_pt +=1
                            else:
                                pass

                       

        else:
            count = 0
            can_go_again = True
            for i in range(moveable_count):

                if position == 'opp' and can_go_again:

                    valid_block = False

                    while not valid_block:

                        user_block_name = skip_input("Choose a block to move (type 'done' if done): ").strip().upper()

                        if user_block_name.lower() == "done":

                            add_to_total_string ("You passed one movement point!")

                            valid_block = True

                        board_blocks = board.eng_roster + board.scot_roster
                        user_block = search.block_name_to_object(board_blocks, user_block_name)

                        if user_block:

                            if user_block in focus_region.blocks_present:

                                if user_block not in blocks_moved:

                                    if move_block(board, user_block,focus_region.regionID,position='opp',prev_paths=prev_paths,is_truce=truce) == False:

                                        add_to_total_string ("That path was not valid!")

                                    else:
                                        

                                        if combat.find_location(board, user_block).name == 'ENGLAND':
                                            can_go_again = False
                                            picked_regions.remove(focus_region)
                                        blocks_moved.append(user_block)

                                        valid_block = True

                                else:

                                    add_to_total_string ("You have already moved that block this turn!")

                            else:

                                add_to_total_string ("That block is not in the region!")

                        else:

                            add_to_total_string ("Please skip_input a valid block name!")

                

                elif position == 'comp' and can_go_again:
                    skip_input('Computer Move Part 2')


                    computer_choice = random.randint(0,100)
                    
                    if computer_choice == 0:
                        pass
             

                    else:
                 
                        possible_paths_2 = list()
                        
                        block_index = i - count
                        block = focus_region.blocks_present[block_index]

                        if block not in blocks_moved:
                            possible_paths_2 = board.check_all_paths(block.movement_points,focus_region.regionID,block,path=[], all_paths=[],truce=truce, role = role)

                            
                            #add_to_total_string("CHECK PATHS", board.check_all_paths(block.movement_points,focus_region.regionID,block,truce=truce))
                            if possible_paths_2:

                                computer_paths_1 = copy.deepcopy(random.choice(possible_paths_2))
                                #add_to_total_string(possible_paths_2)
                                end = computer_paths_1[-1]
                                

                                move_block(board, block,focus_region.regionID,end=end,position='comp',prev_paths=prev_paths,is_truce=truce)

                                block_to_return = block
                                if board.regions[end].name == 'ENGLAND':
                                    prev_paths = tuple(prev_paths)
                                    can_go_again = False
                                    picked_regions.remove(focus_region)
                                else:
                                    if type(prev_paths) == list:
                                        prev_paths.append(computer_paths_1)
                                count+=1
                                blocks_moved.append(block)

                            #add_to_total_string(move_pt)

                        else:
                            pass

        #add_to_total_string(can_go_again)

        move_pt+=1
    return computer_paths_1, block_to_return

