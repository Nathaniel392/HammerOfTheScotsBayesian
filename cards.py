import random
"""
card class
abstract plz
not finished
"""
class Card(object):
def __init__(self):
  """
  initiliaze stuff
  """
  self.visible_bool = False
  
class Deck(object):
  """model of the deck
  """
  
  def __init__(self):
    """initliaze deck"""
    #self.__deck = stuff using card classes
    
  def shuffle(self):
    """shuffle"""
    random.shuffle(self.__deck)
  def deal(self):
    """ return top card from deck"""
    return self.__deck.pop() if len(self.__deck) else None
  def is_empty(self):
    """ return true if deck is empty; False otherwise"""
    return len(self.__deck) == 0
  def __len(self):
    """return number of cards remaining in deck."""
    return len(self.__deck)
  def __str(self):
    """return string"""
    return ", ".join([str(card) for card in self.__deck])
  def __repr__( self ):
        """ Return string representing deck (for use in shell). """
        return self.__str__()

  def display( self, cols=13 ):
    """ Column-oriented display of deck. """
    for index, card in enumerate(self.__deck):
      if index%cols == 0:
        print()
      print("{:3s} ".format(str(card)), end="" )
     print()
     print()
