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

def resolve_card_opp(card, opp_role):
    '''
    This function takes two parameters. One is the card itself and
    the other is the side in which the opponent is on. The function
    determines which card is being played and calls functions accordingly
    to resolve the card
    '''
    pass

def resolve_card_computer(card, comp_role):
    '''
    This function takes two parameters. One is the card itself and the
    other is the side in which the computer is playing. The function determines
    which card is being played and calls functions accordingly to resolve
    the card
    '''
    pass

def play_game():
    #Determine scenario
    #scenario = prompt_scenario()
    scenario = 'BRAVEHEART'

    #Determine which side the computer plays:
    #computer_role, opp_role = prompt_ai_side()
    computer_role = 'ENGLAND'
    opp_role = 'SCOTLAND'

    stc_locations = location_prob.create_static_locations()
    dyn_locations = location_prob.create_static_locations()

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
    
    #Find out what card the human wants to play
    opp_card = opp_hand(opp_card_choice(opp_hand))
    #Remove card from human hand
    opp_hand.remove(opp_card)
    #Get card for computer
    computer_card = cardplay.random_card(computer_hand)
    #Remove card from computer hand
    computer_hand.remove(computer_card)

    if compare_cards(opp_card, computer_card, computer_role):
        #Enter code to resolve computer card first
        resolve_card_computer(computer_card, computer_role)
        resolve_card_opp(opp_card, opp_role)

    else:
        #Enter code to resolve human card first
        resolve_card_opp(opp_card, opp_role)
        resolve_card_computer(computer_card, computer_role)

    
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
