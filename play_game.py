import cards
import initialize_blocks
import static_locations
import blocks_occupied
import board

"""
stuff
"""
def play_game():
    #create stuff
    deck = cards.Deck()
    deck.shuffle()
    nobles, non_noble_blocks = initialize_blocks.initialize_blocks()
    stc_locations = static_locations.create_static_locations()
    dyn_locations = static_locations.create_static_locations()
    
    #deal hands
    my_hand = list()
    opp_hand = list()
    for i in range(5):
        my_hand.append(deck.deal())
        opp_hand.append(deck.deal())
        
    #probabilites of cards
    probability_cards = deck.count_probabilities()
    
    #map of occupied
    map_of_blocks = blocks_occupied.make_occupied()
play_game()
