import random

class Deck( object ):

  def __init__ ( self ):    
    '''initializes at the start of the game a deck of cards with 7 '1's', 10 '2's', 3 '3's' and 5 event cards'''
    
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
        """ Shuffle deck using shuffle method in random module. """
      
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
    return self.__deck
  
  def count_probabilities( self ):
    '''returns probabilities of each type of card being picked'''
    
    ones_probability = self.__deck.count('1') / len(self.__deck)
    twos_probability = self.__deck.count('2') / len(self.__deck)
    threes_probability = self.__deck.count('3') / len(self.__deck)
    event_card_probabilities = 1 - (ones_probability + twos_probabilty + threes_probability)
    
    return ones_probability,twos_probability,threes_probabilities,event_card_probabilities
  
  def reset(self):
    '''resets the deck after each year so that  all the cards are accounted for in the following year'''
    
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
    
    
    
    
  
