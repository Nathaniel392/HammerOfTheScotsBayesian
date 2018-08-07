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

def win(block_list, year, scenario):
    """
    returns string of who wins
    or false
    """
    scot_noble_count = 0
    eng_noble_count = 0
    wallace_is_dead = True
    for block in block_list:
        if block.type == 'KING' and block.name == 'KING' and block.current_strength == 0:
            return 'ENGLAND WINS'
        elif block.type == 'KING' and block.current_strength == 0:
            return 'SCOTLAND WINS'

        if type(block) == blocks.Noble and block.allegiance == 'SCOTLAND':
            scot_noble_count += 1
        elif type(block) == blocks.Noble and block.allegiance == 'ENGLAND':
            eng_noble_count += 1
        if block.name == 'WALLACE' and block.current_strength != 0:
            wallace_is_dead = False

    if scot_noble_count == 0:
        return 'ENGLAND WINS'
    elif eng_noble_count == 0:
        return 'SCOTLAND WINS'

    if year == 1305 and scenario == 'BRAVEHEART':
        if scot_noble_count == eng_noble_count:
            if wallace_is_dead:
                return 'ENGLAND WINS'
            else:
                return 'SCOTLAND WINS'
        else:
            if scot_noble_count > eng_noble_count:
                return 'SCOTLAND WINS'
            else:
                return 'ENGLAND WINS'
    elif year == 1314 and scenario == 'BRUCE':
        if scot_noble_count > eng_noble_count:
            return 'SCOTLAND WINS'
        else:
            return 'ENGLAND WINS'
    elif year == 1305 and scenario == 'CAMPAIGN':
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

    
    #Initialize table with known probabilities
    location_prob_table = location_prob.init_probability_table(current_board, block_list)

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
    while game_playing:

        """INITIALIZE YEAR - deal, etc"""
        print('Year: ' + str(year))
        deck.reset()
        eng_hand, scot_hand = deck.deal_hands()

        #When this gets to 5, end the year
        turn_counter = 0
        play_turn = True


        
        while play_turn:
            
            turn_counter += 1
            current_board.turn = turn_counter

            #Reference to cards visible to the computer
            #known_cards = computer_hand

            #probabilites of cards
            #probability_cards = deck.count_probabilities(known_cards)

            #Find out what england wants to play
            if eng_type == 'opp':
                eng_card = opp_hand[opp_card_choice(opp_hand)]
            elif eng_type == 'comp':
                eng_card = cardplay.select_comp_card(current_board, eng_hand, 'ENGLAND')
            
            #Find out what scotland wants to play
            if scot_type == 'opp':
                scot_card = opp_hand[opp_card_choice(scot_hand)]
            elif scot_type == 'comp':
                scot_card = cardplay.select_comp_card(current_board, scot_hand, 'SCOTLAND')

            #Remove card from hands
            eng_hand.remove(eng_card)
            #Remove card from computer hand
            scot_hand.remove(scot_card)


            #Figure out who goes first, if it is true then Computer goes first - also resolves cards
            who_goes_first, year_cut_short = cardplay.compare_cards(current_board, eng_card, scot_card, eng_type, scot_type)
            
            #Get a list all the regions that are contested
            contested_regions = current_board.get_contested_regions()
            print(contested_regions)


            #If the human goes first find out what region they want to battle in
            while len(contested_regions) > 0:

                if who_goes_first == False:

                    battle_region = contested_regions[opp_battle_choice(contested_regions)]

                    combat.battle(battle_region.combat_dict['Attacking'], battle_region.combat_dict['Defending'], battle_region.combat_dict['Attacking Reinforcements'], battle_region.combat_dict['Defending Reinforcements'],current_board, eng_type, scot_type)

                    contested_regions.remove(battle_region)
                    


                else:

                    battle_region = contested_regions[random.randint(0, len(contested_regions)-1)]
                    combat.battle(battle_region.combat_dict['Attacking'], battle_region.combat_dict['Defending'], battle_region.combat_dict['Attacking Reinforcements'], battle_region.combat_dict['Defending Reinforcements'],current_board, eng_type, scot_type)

                    contested_regions.remove(battle_region)
                    
            border_raids.border_raid(current_board, eng_type, scot_type)
            update_roster.update_roster(block_list, current_board)

            if year_cut_short or turn_counter >= 5:
                play_turn = False
                year += 1
            if win(block_list, year, scenario):
                print(win(block_list, year, scenario))
                return 'game over'
        input('Start Winter')
        winter.initialize_winter(current_board, block_list, eng_type, scot_type, edward_prev_winter)
        winter.winter_builds(current_board, eng_type, scot_type)


def main():
    play_game()

if __name__ == '__main__':
    main()
