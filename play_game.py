import cards
import initialize_blocks
import location_prob
import blocks_occupied
import board

"""
stuff
"""
def play_game():
    '''
    David write a good function header here
    '''

    #Take input from the user for the scenario and which side to play
    flag = False
    while not flag:
        game_type = input("Enter whether you are playing BraveHeart (1), The Bruce (2), or Campaign (3): ")
        #Error message for incorrect input
        if game_type not in '123':
            print('Invalid input, try again.')
        else:
            #Convert from string input to int
            game_type = int(game_type)
            if game_type == 3:
                game_type = 1   #Campaign setup is the same as braveheart setup
            block_list = initialize_blocks.initialize_blocks(game_type)
            flag = True

    flag = False
    while not flag:
        computer_role = input("Enter which side you want the computer to play (England or Scotland): ")
        if computer_role.lower() == 'england' or computer_role.lower() == 'scotland':
            flag = True
        else:
            print("Invalid input, try again")

    #IDK what this does lol
    stc_locations = location_prob.create_static_locations()
    dyn_locations = location_prob.create_static_locations()

    #Initialize the deck of cards
    deck = cards.Deck()
    deck.shuffle()
    #deal hands of 5
    computer_hand = list()
    opp_hand = list()
    for i in range(5):
        computer_hand.append(deck.deal())
        opp_hand.append(deck.deal())

    known_cards = computer_hand

    #probabilites of cards
    probability_cards = deck.count_probabilities(known_cards)
    print(probability_cards)

    #Initialize board
    current_board = board.Board()

    add_starting_blocks(current_board, nobles, other_blocks)

    comp_roster, comp_pool = board.get_comp_blocks(current_board, computer_role)


def main():
    play_game()

if __name__ == '__main__':
    main()