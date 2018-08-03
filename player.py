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
		Reads in a hand and stores it in self.hand
		hand:  list of 5 cards (strings)
		Returns:  None
		'''
		all_strings = True
		for item in hand:
			if type(item) != string:
				all_strings = False

		if type(hand) != list or len(hand) != 5 or not all_strings:
			raise Exception('hand object is not a list of 5 strings.')
		else:
			self.hand = hand

	def play_event(self):
		'''
		Human player overrides this method - Computer player always plays its event card.
		'''
		return True


###
###
###
class Human(Player):

	def __init__(self, role):
		'''
		Initialize the human player.

		'''

		super(Player, self).__init__(self, role)


	def play_event(self):
		'''
		Give the human player an option to pass their event card
		'''

		invalid_input = True
		while invalid_input:
			user_input = input('Would you like to play the event card or pass it? (play/pass): ').strip().lower()

			#Check for valid input
			if user_input != 'play' and user_input.lower() != 'pass':
				print('Invalid input. Enter \'play\' or \'pass\': ')
			else:
				invalid_input = False
		
		#Return a boolean
		return user_input == 'play'

	def select_card(self):
		'''
		Print hand and prompt the user to pick a card.
		Returns:  card to be played (string)
			'''

		#Print hand
		print(role + '\'s hand:')
		for card in self.hand:
			print(card, end=' ')
		print()

		#Input and error check what card the user wants to play
		choice = ''

		valid_input = False
		while not valid_input:

			choice = input('Enter the card you want to play: ').strip().upper()

			#Allow the user to crash the program
			if choice == 'QUIT' or choice.lower() == 'quit':
				raise Exception('Quitting the program.')

			elif choice in self.hand:
				valid_input = True

		return choice

	def battle_choice(self, contested_regions):
		'''
		Print the contested regions and let the user pick the 
		'''



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














