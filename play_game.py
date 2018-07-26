import cards
import initialize_blocks
import location_prob
import blocks_occupied
import board
import cardplay

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
    for card in cards:
        if card == '1' or card == '2' or card == '3':
            print(card, end = " ")
        elif card == 'SEA':
            print('SEA', end = " ")
        elif card == 'HER':
            print('HER')
        elif card == 'PIL':
            print('PIL')
        elif card == 'TRU':
            print('TRU')
        elif card == 'VIC':
            print('VIC')
    #Input and error check what card the user wants to play
    while choice not in cards:
        choice = input('Enter the card you want to play: ')
        choice = choice.upper()
        for i,card in enumerate(cards):
            if card == choice:
                return(i)


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
        choice = input('Enter name of region you want to resolve the battle in: ')
        for i,reg in enumerate(contested_regions):
            if reg == choice:
                return(i)

def play_game():
    #Determine scenario
    #scenario = prompt_scenario()
    scenario = 'BRAVEHEART'

    #Determine which side the computer plays:
    #computer_role, opp_role = prompt_ai_side()
    computer_role = 'ENGLAND'
    opp_role = 'SCOTLAND'

    #Initialize card stuff
    deck = cards.Deck()
    deck.shuffle()
    #deal hands
    computer_hand = list()
    opp_hand = list()
    for i in range(5):
        computer_hand.append(deck.deal())
        opp_hand.append(deck.deal())

    known_cards = computer_hand

    #probabilites of cards
    probability_cards = deck.count_probabilities(known_cards)
    #print(probability_cards)

    #Create list of blocks
    block_list = initialize_blocks.initialize_blocks()
    
    #Initialize board
    current_board = board.Board()

    #Fill board with pieces
    current_board.fill_board(block_list, scenario)

    #Initialize table with known probabilities
    location_prob_table = location_prob.init_probability_table(current_board, block_list)
    
    #Find out what card the human wants to play

    opp_card = opp_hand[opp_card_choice(opp_hand)]

    #Remove card from human hand
    opp_hand.remove(opp_card)
    #Get card for computer
    computer_card = cardplay.random_card(computer_hand)
    #Remove card from computer hand
    computer_hand.remove(computer_card)

    #Figure out who goes first, if it is true then Computer goes first
    who_goes_first = cardplay.compare_cards(opp_card, computer_card, computer_role)

    if who_goes_first:

        #Enter code to resolve computer card first
        resolve_card('comp', computer_card, computer_role)
        resolve_card('opp', opp_card, opp_role)

    else:
        
        #Enter code to resolve human card first
        resolve_card('opp', opp_card, opp_role)
        resolve_card('comp', computer_card, computer_role)


    #Get a list all the regions that are contested
    contested_regions = current_board.get_contested_regions()

    #If the human goes first find out what region they want to battle in
    while len(contested_regions) > 0:

        if who_goes_first == False:

            battle_region = contested_regions[opp_battle_choice(contested_regions)]

            combat.battle(battle_region.combat_dict['Attacking'], battle_region.combat_dict['Defending'], battle_region.combat_dict['Attacking Reinforcements'], current_board, computer_role= computer_role)

            contested_regions.remove(battle_region)
            
    #Print blocks for testing
    #for block in block_list:
    #    print(block)

    #for region in current_board.regions:
        #print(region)
    
    #add_starting_blocks(current_board, nobles, other_blocks)

    #comp_roster, comp_pool = board.get_comp_blocks(current_board, computer_role)


def main():
    play_game()

if __name__ == '__main__':
    main()
