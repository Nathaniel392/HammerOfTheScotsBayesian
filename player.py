class Player(object):

	def __init__(self, role):
		'''
		Initializes a player.
		role:  'ENGLAND' or 'SCOTLAND'
		'''
		
		self.hand = []
		self.role = role

	def take_hand(self, hand):
		'''
		Reads in a 
		'''

		if type(hand) != list or len(hand) != 5:
			raise Exception('hand is not a list of 5 strings.')
		else:
			self.hand = hand


###
###
###
class Human(Player):

	def __init__(self, role):
		'''
		Initialize the human player.

		'''

		super(Player, self).__init__(self, role)


###
###
###
class Computer(Player):

	def __init__(self, role, board):
		'''
		Initializes the computer player. Has additional data.

		'''

		super(Player, self).__init__(self, role)


###
###
###
class English(Computer):

	def __init__(self, board):
		'''
		Initializes the English
		'''














