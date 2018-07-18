import cards
import initialize_blocks
import static_locations

"""
stuff
"""
def play_game():
    #create stuff
    deck = Deck()
    nobles, non_noble_blocks = initilialize_blocks.initialize_blocks()
    static_locations = static_locations.create_static_locations()
    dynamic_locations = static_locations.create_static_locations()
    
    #deal hands
    my_hand = list()
    opp_hand = list()
    for i in range(5):
        my_hand.append(Deck.deal())
        opp_hand.append(Deck.deal())
    
play_game()
