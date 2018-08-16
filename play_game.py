import cards
import initialize_blocks
import location_prob
import blocks_occupied
import board
import cardplay
import blocks
import winter
import border_raids
import update_roster
import random
import combat
import exceptions
import search
import input_toggle
def find_location(board, blok):
    '''
    This function takes a board object and the name of a block
    and returns a region object where the block is
    '''

    
    for i,region in enumerate(board.regions):
        for bllock in region.blocks_present:
            
            if bllock.name == blok.name:
                return board.regions[i]
    
    return False
    #print('CANNOT FIND BLOCK WITH BLOCK NAME', blok.name)
    #raise Exception('cannot find block')

def clean_up_dict(region):

    for key in region.combat_dict:
        for block in region.combat_dict[key]:

            if block.current_strength <= 0:
                region.combat_dict[key].remove(block)
                if block in region.blocks_present:
                    region.blocks_present.remove(block)

    return region

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

def prompt_scenario():
    '''
    Ask the user for a scenario and return the string
    'BRAVEHEART' or 'BRUCE'
    '''
    flag = False
    while not flag:
        game_type = input("Enter whether you are playing BraveHeart (1), The Bruce (2), or Campaign (3): ")
        #Invalid input error message
        if game_type not in '123':
            print('Invalid input, try again')
        else:
            flag = True

    #Convert to int
    game_type = int(game_type)

    #Campaign setup is same as braveheart
    if game_type == 1 or game_type == 3:
        scenario = 'BRAVEHEART'
    else:   #2
        scenario = 'BRUCE'
    
    return scenario

def set_up_combat_dict(current_board, battle_region):
    battle_regionID = battle_region.regionID

    battle_region = current_board.regions[battle_regionID]

    for i,region in enumerate(current_board.regions):
        current_board.regions[i].combat_dict = {'Attacking':[], 'Defending':[], 'Attacking Reinforcements':[], 'Defending Reinforcements':[]}

    has_defenders = False
    defending_path = None
    defending_allegiance = None
    first_block = None
    for block in battle_region.blocks_present:


        if not battle_region.is_block_enterer(block) and block.current_strength>0:
            current_board.regions[battle_regionID].combat_dict['Defending'].append(block)
            has_defenders = True
            defending_allegiance = block.allegiance
        elif block.current_strength == 0:
            battle_region.blocks_present.remove(block)

    if not has_defenders:
        first_block,defending_path = battle_region.find_first_enterer()
        if first_block != None:
            current_board.regions[battle_regionID].combat_dict['Defending'].append(first_block)
            defending_allegiance = first_block.allegiance
        else:
            current_board.regions[battle_regionID].combat_dict['Defending'].append(battle_region.blocks_present[0])
            defending_allegiance = battle_region.blocks_present[0].allegiance

    attacking_path = None
    
    for role in battle_region.enterers:
        for path in battle_region.enterers[role]:
            for block,order in battle_region.enterers[role][path]:

                if (has_defenders or block != first_block) and block.current_strength > 0:
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


    return battle_region

def prompt_ai_side():
    '''
    Ask the user for which side the computer should play
    return the computer's role ('ENGLAND' or 'SCOTLAND')
    '''
    flag = False
    opp_role = ''
    while not flag:
        computer_role = input("Enter which side you want the computer to play (England or Scotland): ")
        computer_role = computer_role.upper()
        if computer_role == 'ENGLAND' or computer_role == 'SCOTLAND':
            flag = True
        else:
            print("Invalid input, try again")
    if computer_role == 'ENGLAND':
        opp_role = 'SCOTLAND'
    else:
        opp_role = 'ENGLAND'
    return computer_role, opp_role

def opp_card_choice(cards):
    '''
    Print out all of the humans cards
    Returns the index of the card in which they want
    to play
    '''
    choice = ''
    #Print out all the card possibilities
    print('opp hand: ')
    for card in cards:
        if card == '1' or card == '2' or card == '3':
            print(card, end = " ")
        elif card == 'SEA':
            print('SEA', end = " ")
        elif card == 'HER':
            print('HER', end = ' ')
        elif card == 'PIL':
            print('PIL', end = ' ')
        elif card == 'TRU':
            print('TRU', end = ' ')
        elif card == 'VIC':
            print('VIC', end = ' ')
    print()
    #Input and error check what card the user wants to play
    while choice not in cards:
        while True:
            choice = input('Enter the card you want to play: ')
            if choice.lower() == 'quit':
                raise Exception('You told me to quit')
            choice = choice.upper()
            for i,card in enumerate(cards):
                if card == choice:
                    return(i)
            print('type a valid card')





def opp_battle_choice(contested_regions):
    '''
    Print out all the contested regions
    Return the index of the region that they want
    to do the first battle in
    '''
    choice = " "
    print('Contested Regions: ', end = " ")
    for region in contested_regions:
        print(region.name, end = " ")
    
    while choice not in contested_regions:
        choice = input('Enter name of region you want to resolve the battle in: ').upper()
        for i,reg in enumerate(contested_regions):
            if reg.name == choice:
                return(i)

def win(block_list, year, scenario, current_board):
    """
    returns string of who wins
    or false
    """
    scot_noble_count = 0
    eng_noble_count = 0
    wallace_is_dead = True
    for block in block_list:
        if block.type == 'KING' and block.name == 'KING' and block.current_strength == 0:
            return 'ENGLAND WINS, SCOTTISH KING IS DEAD'
        elif block.type == 'KING' and block.current_strength == 0:
            return 'SCOTLAND WINS, EDWARD THE 2nd IS DEAD'

        if type(block) == blocks.Noble and block.allegiance == 'SCOTLAND':
            scot_noble_count += 1
        elif type(block) == blocks.Noble and block.allegiance == 'ENGLAND':
            eng_noble_count += 1
        if block.name == 'WALLACE' and block.current_strength != 0 and find_location(current_board, block):
            wallace_is_dead = False
            #print('WALLACES LOCATION: ', find_location(current_board, block))
    if scot_noble_count == 0:
        return 'ENGLAND WINS, SCOTLAND NOBLES ARE 0'
    elif eng_noble_count == 0:
        return 'SCOTLAND WINS, ENGLAND NOBLES ARE 0'

    if year == 1306 and scenario == 'BRAVEHEART':
        if scot_noble_count == eng_noble_count:
            if wallace_is_dead:
                return 'ENGLAND WINS, ON DECISION WITH WALLACE'
            else:
                return 'SCOTLAND WINS, ON DECISION WITH WALLACE'
        else:
            if scot_noble_count > eng_noble_count:
                return 'SCOTLAND WINS, WITH MORE NOBLES ' + str(scot_noble_count) + ' to ' + str(eng_noble_count)
            else:
                return 'ENGLAND WINS, WITH MORE NOBLES ' + str(eng_noble_count) + ' to ' + str(scot_noble_count)
    elif year == 1315 and scenario == 'BRUCE':
        if scot_noble_count > eng_noble_count:
            return 'SCOTLAND WINS, WITH MORE NOBLES ' + str(scot_noble_count) + ' to ' + str(eng_noble_count)
        else:
            return 'ENGLAND WINS, WITH MORE NOBLES ' + str(eng_noble_count) + ' to ' + str(scot_noble_count)
    elif year == 1306 and scenario == 'CAMPAIGN':
        block_list[27].type = 'KING'
        
            
    return False




def play_game():
    #Determine scenario
    #scenario = prompt_scenario()
    scenario = 'BRAVEHEART'

    #Determine which side the computer plays:
    #computer_role, opp_role = prompt_ai_side()
    eng_type = 'comp'
    scot_type = 'comp'
    

    #Create list of blocks
    block_list = initialize_blocks.initialize_blocks()
    
    
    #Initialize board
    current_board = board.Board()

    #Fill board with pieces
    current_board.fill_board(block_list, scenario)
    
    for block in current_board.all_blocks:
        if type(block) == blocks.Noble:
            current_board.all_nobles.append(block)

    
    #Initialize table with known probabilities
    #location_prob_table = location_prob.init_probability_table(current_board, block_list)

    #Initialize card deck
    deck = cards.Deck()

    """GAME START"""
    game_playing = True

    if scenario == 'BRUCE':
        year = 1306
    else:
        year = 1297

    winter.levy(current_board, 'start')

    edward_prev_winter = [False]
    if scenario == 'BRUCE':
        if current_board.all_blocks[28] in current_board.scot_pool:
            current_board.scot_pool.remove(current_board.all_blocks[28])
        if current_board.all_blocks[21] in current_board.scot_pool:
            current_board.scot_pool.remove(current_board.all_blocks[21])

    while game_playing:

        """INITIALIZE YEAR - deal, etc"""
        #print('Year: ' + str(year))
        deck.reset()
        eng_hand, scot_hand = deck.deal_hands()

        #When this gets to 5, end the year
        turn_counter = 0
        play_turn = True

        while play_turn:
            print('Year: ' + str(year))

            turn_counter += 1
            current_board.turn = turn_counter

            #Reference to cards visible to the computer
            #known_cards = computer_hand

            #probabilites of cards
            #probability_cards = deck.count_probabilities(known_cards)

           #Find out what england wants to play
            if eng_type == 'opp':
                eng_card = eng_hand[opp_card_choice(eng_hand)]
                eng_parameter = 0
            elif eng_type == 'comp':
                eng_card, eng_parameter = cardplay.select_comp_card(current_board, eng_hand, 'ENGLAND')
            
            #Find out what scotland wants to play
            if scot_type == 'opp':
                scot_parameter = 0
                scot_card = scot_hand[opp_card_choice(scot_hand)]
            elif scot_type == 'comp':
                scot_card, scot_parameter = cardplay.select_comp_card(current_board, scot_hand, 'SCOTLAND')

            #Remove card from hands
            eng_hand.remove(eng_card)
            #Remove card from computer hand
            scot_hand.remove(scot_card)



            #Figure out who goes first, if it is true then Computer goes first - also resolves cards
            who_goes_first, year_cut_short = cardplay.compare_cards(current_board, eng_card, scot_card, eng_type, scot_type, eng_parameter, scot_parameter)
            
            
            #Get a list all the regions that are contested
            contested_regions = current_board.get_contested_regions()

            for i,region in enumerate(contested_regions):
                contested_regions[i] = clean_up_dict(contested_regions[i])
                current_board.regions[contested_regions[i].regionID] = contested_regions[i]
            current_board = clean_up_board(current_board)
            contested_regions = current_board.get_contested_regions()
            #If the human goes first find out what region they want to battle in
            while len(contested_regions) > 0:

                if who_goes_first == False:

                    battle_region = contested_regions[opp_battle_choice(contested_regions)]
                    battle_region = set_up_combat_dict(current_board, battle_region)
                    if battle_region.is_contested():
                        combat.battle(battle_region.combat_dict['Attacking'], battle_region.combat_dict['Defending'], battle_region.combat_dict['Attacking Reinforcements'], battle_region.combat_dict['Defending Reinforcements'],current_board, eng_type, scot_type) 
                    contested_regions.remove(battle_region)
                    current_board.regions[battle_region.regionID] = battle_region


                else:
                    
                    battle_region = contested_regions[random.randint(0, len(contested_regions)-1)]
                   
                    battle_region = set_up_combat_dict(current_board, battle_region)
                    if battle_region.is_contested():
                        combat.battle(battle_region.combat_dict['Attacking'], battle_region.combat_dict['Defending'], battle_region.combat_dict['Attacking Reinforcements'], battle_region.combat_dict['Defending Reinforcements'],current_board, eng_type, scot_type)
                    contested_regions.remove(battle_region)
                    current_board.regions[battle_region.regionID] = battle_region

            border_raids.border_raid(current_board, eng_type, scot_type)
            update_roster.update_roster(block_list, current_board)

            if year_cut_short or turn_counter >= 5:
                play_turn = False
                year += 1
            if win(block_list, year, scenario, current_board):
                print(win(block_list, year, scenario, current_board))
                return 'game over'
            for i,region in enumerate(current_board.regions):
                current_board.regions[i].enterers = {'ENGLAND':dict(), 'SCOTLAND':dict()}

        
        input_toggle.toggle_input('other')
        winter.update_roster(current_board)
        #moray_loca = combat.find_location(current_board, search.block_name_to_object(current_board.all_blocks, 'MORAY'))
        winter.initialize_winter(current_board, block_list, eng_type, scot_type,edward_prev_winter)
        winter.winter_builds(current_board, eng_type, scot_type)
        winter.update_roster(current_board)
        
        input_toggle.toggle_input('other')

def main():
    try:
        play_game()
    except exceptions.EnglishKingDeadException:
        print('\n\n\nThe English King is Dead!\nSCOTLAND WINS')
    except exceptions.ScottishKingDeadException:
        print('\n\n\nThe Scottish King is Dead!\nENGLAND WINS')

if __name__ == '__main__':
    main()
