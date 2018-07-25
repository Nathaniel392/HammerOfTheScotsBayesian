import cards
import initialize_blocks
import location_prob
import blocks_occupied
import board

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
    while not flag:
        computer_role = input("Enter which side you want the computer to play (England or Scotland): ")
        computer_role = computer_role.upper()
        if computer_role == 'ENGLAND' or computer_role == 'SCOTLAND':
            flag = True
        else:
            print("Invalid input, try again")

    return computer_role

def play_game():
    #Determine scenario
    #scenario = prompt_scenario()
    scenario = 'BRAVEHEART'

    #Determine which side the computer plays:
    #computer_role = prompt_ai_side()
    computer_role = 'ENGLAND'

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
