import cards
import initialize_blocks
import location_prob
import blocks_occupied
import board

"""
stuff
"""
def play_game():
    #create stuff
    game_type = input("Enter whether you are playing BraveHeart (1), The Bruce (2), or Campaign (3): ")
    computer_role = input("Enter which side you want the computer to play (England or Scotland): ")
    
    if game_type == 1 or game_type == 3:
        nobles, non_noble_blocks, static_nobles, static_non_noble_blocks = initialize_blocks.initialize_blocks()
    elif game_type == 2:
        nobles, non_noble_blocks, static_nobles, static_non_noble_blocks = initialize_blocks.initlialize_blocks_bruce()


    stc_locations = location_prob.create_static_locations()
    dyn_locations = location_prob.create_static_locations()

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
    print(probability_cards)
    #map of occupied
    map_of_blocks = blocks_occupied.make_occupied()

    current_board = board.Board()
    
    add_starting_blocks(board, nobles, other_blocks)

    if computer_role.lower() == 'england':
        computer_pool = board.eng_pool
        computer_roster = board.eng_roster
    elif computer_role.lower() == 'scotland':
        computer_roster = board.scot_roster
        computer_pool = board.scot_pool

    edward = static_non_noble_blocks[27]
    scot_king = static_non_noble_blocks[28]
    
play_game()