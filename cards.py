import random

class Deck( object ):

  def __init__ ( self ):    
    """ initializes at the start of the game a deck of cards with 7 '1's', 10 '2's', 3 '3's' and 5 event cards """
    
    self.__deck = []
    
    for i in range(0,7):
      self.__deck.append('1')
      
    for i in range(0,10):
      self.__deck.append('2')
      
    for i in range(0,3):
      self.__deck.append('3')
      
    #appends the event cards using the first 3 letters of the card in all caps
    self.__deck.append('SEA')
    self.__deck.append('HER')
    self.__deck.append('VIC')
    self.__deck.append('PIL')
    self.__deck.append('TRU')
    
  def shuffle( self ):
    """
    Shuffle deck using shuffle method in random module.
    """
    random.shuffle(self.__deck)

  def deal( self ):
    """ Return top card from deck (return None if deck empty). """
 
    return self.__deck.pop() if len(self.__deck) else None # Use ternary expression to guard against empty deck.

  def is_empty( self ):
    """ Return True if deck is empty; False, otherwise """
      
    return len(self.__deck) == 0

  def __len__( self ):
    """ Return number of cards remaining in deck. """
      
    return len(self.__deck)
  
  def __str__( self ):
    return str(self.__deck)

  def deal_hands( self ):
  	""" Shuffle deck and return two 5-card hands. Used at the start of a turn. """
  	self.shuffle()
  	hand_one = []
  	hand_two = []

  	for counter in range(5):
  		hand_one.append(self.deal())
  		hand_two.append(self.deal())

  	return hand_one, hand_two

  
  def count_probabilities(self, known):
    '''returns probabilities of each type of card being picked after each turn depeneding on the other cards that have 
    been picked'''
    
    probabilities_lst = []

    ones_probability = float((7 - known.count('1'))) / (25 - len(known))
    probabilities_lst.append(ones_probability)
    
    twos_probability = float((10 - known.count('2'))) / (25 - len(known))
    probabilities_lst.append(twos_probability)
    
    threes_probability = float((3 - known.count('3'))) / (25 - len(known))
    probabilities_lst.append(threes_probability)
    
    SEA_probability = float((1- known.count('SEA'))) / (25 - len(known))
    probabilities_lst.append(SEA_probability)
    
    HER_probability = float((1-known.count('HER'))) / (25 - len(known))
    probabilities_lst.append(HER_probability)
    
    TRU_probability = float((1-known.count('TRU'))) / (25 - len(known))
    probabilities_lst.append(TRU_probability)
    
    VIC_probability = float((1-known.count('VIC'))) / (25 - len(known))
    probabilities_lst.append(VIC_probability)
    
    PIL_probability = float((1-known.count('PIL'))) / (25 - len(known))
    probabilities_lst.append(PIL_probability)
    
    return probabilities_lst
    
  def reset(self):
    '''resets the deck after each year so that all the cards are accounted for in the following year'''
    
    self.__deck = []
    
    for i in range(0,7):
      self.__deck.append('1')
      
    for i in range(0,10):
      self.__deck.append('2')
      
    for i in range(0,3):
      self.__deck.append('3')
      
    #appends the event cards using the first 3 letters of the card in all caps
    self.__deck.append('SEA')
    self.__deck.append('HER')
    self.__deck.append('VIC')
    self.__deck.append('PIL')
    self.__deck.append('TRU')
    
    
    
    
  
