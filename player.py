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
	def her_utility(self, board, role, hand, card_prob, loc_prob, enemy_nobles):
		"""
		board: the board
		role: the role
		hand: the hand
		card_prob: card probability table
		loc_prob: location probability table
		enemy_nobles: list of enemy nobles
		"""
		###
		#CONSTANTS
		BOTTOM_CERTIAINTY = .10
		TOP_CERTAINTY = .90
		CERTAINTY_THRESHOLD = .40
		BLOCK_CERTAINTY_THRESHOLD = .25
		WINNING_THRESHOLD = .75
		UNSCATHED_UTILITY = 15
		COMBAT_UTILITY = 10
		NUM_SIMULATIONS = 1000
		FRIENDLY_UNITS_SCALAR = 2
		KING_UTILITY = 15

		###

		noble_to_steal = None
		
		#Find enemy regions
		if role == 'ENGLAND':
			enemy_role = 'SCOTLAND'
		else:
			enemy_role = 'ENGLAND'


		
		

		### TEMPORARY									###
		### random choice								###
		###												###
		#noble_to_steal = random.choice(enemy_nobles)	###
		#return noble_to_steal							###
		###												###
		###												###
		###												###

		###
		# Check each noble for their utility - store it into a dictionary
		###

		# FORMAT noble.name (string) : utility (int)
		utility_dict = {}

		for enemy_noble in enemy_nobles:

			utility = 0

			#Declaring variables here
			battle_outcome_util = 0
			final_position_util = 0
			king_possibility_util = 0


			###
			# Find the region that that noble is most likely to be in
			###

			#List of probabilities that a noble is in a region - indeces are regionIDs - find the most probable one
			noble_region_probability = loc_prob[enemy_noble.regionID]
			most_probable_region_index_list = computer_decisions.find_n_highest_indeces(noble_region_probability)

			likely_region = search.region_id_to_object(most_probable_region_index_list[0])

			#Look at the combat immediately after - run most probable enemies through a simulation
			num_blocks_in_region = len(enemy_noble_region.blocks_present)
			num_other_blocks = num_blocks_in_region - 1

			###
			# Check if you can actually win the fight after flipping the noble
			###

			#That noble is alone in the region -  no battle
			if num_blocks_in_region == 1:
				battle_outcome_util = UNSCATHED_UTILITY

			#Noble will have to fight after flipping
			else:

				#Find the 
				likely_blocks = computer_decisions.likely_blocks(board, region, loc_prob)

				#Possible error in previous calculations - lowers value of choosing this region (?)
				if enemy_noble not in likely_blocks:
					#
					# Do something here
					#
					#
					#
					#
					#
					#
					pass
				else:
					likely_blocks.remove(enemy_noble)


				###
				# Run a simulation with the most probable blocks in the area
				###

				#Temporarily flip the noble for the simulation
				enemy_noble.allegiance = enemy_role

				attack = [enemy_noble]
				defense = likely_blocks

				simulation_results = simulations.simulation(attack, defense, NUM_SIMULATIONS)
				win_rate = simulation_results['attacker wins'] / NUM_SIMULATIONS

				#Flip it back
				enemy_noble.allegiance = role

				#Value from 0-COMBAT_UTILITY, scaled by distance from the WINNING_THRESHOLD
				if win_rate > WINNING_THRESHOLD:
					battle_outcome_util = (win_rate - WINNING_THRESHOLD) / (1.0 - WINNING_THRESHOLD) * COMBAT_UTILITY

			#If the block has a high chance of successfully flipping and winning the battle
			if battle_outcome_util > 0:

				###
				# Look at the surrounding regions to see if it is in danger or in a good position
				###

				adjacent_regions = board.find_adjacent_regions_object(region)

				###
				###
				###	POTENTIAL CHANGES
				### - don't just check adjacent blocks - look at the strategic value of having a noble in that region,
				###   and check all enemies that could potentially reach the noble's location and take it back
				###
				###

				#Count the friendly and enemy blocks nearby
				num_adjacent_friendly_blocks = 0
				num_adjacent_enemy_blocks = 0


				for adjacent_region in adjacent_regions:
					for block in adjacent_region.blocks_present:

						adjacent_blocks.append(block)

						if role == 'ENGLAND':
							if block.allegiance == 'ENGLAND':
								num_adjacent_friendly_blocks += 1
							else:
								num_adjacent_enemy_blocks += 1

						elif role == 'SCOTLAND':
							if block.allegiance == 'SCOTLAND':
								num_adjacent_friendly_blocks += 1
							else:
								num_adjacent_enemy_blocks += 1

				#More adjacent friends than enemies - set the utility
				final_position_util = (num_adjacent_friendly_blocks - num_adjacent_enemy_blocks) * FRIENDLY_UNITS_SCALAR

			'''
			###
			# UNCOMMENT THIS WHEN crown_king() IS FINISHED
			###

			#Check if herald should be used to take a potential king
			if enemy_noble.name == 'BRUCE' or enemy_noble.name == 'COMYN':

				crown_king = crown_king(board, role, hand, prob_info)

				#If this noble should be crowned, add utility
				if enemy_noble == crown_king:
					king_possiblity_util = KING_UTILITY

			'''


			###
			# Sum the utility and store it
			###
			utility = battle_outcome_util + final_position_util + king_possibility_util
			utility_dict[enemy_noble.name] = utility






		###
		# Process the utility dictionary
		###

		#Since the dictionary keys are names, store the best noble as a name
		noble_to_steal_name = enemy_nobles[0].name

		#Loop through the dictionary and find the noble with highest utility
		for enemy_noble_name, enemy_noble_utility in utility_dict.items():

			if enemy_noble_utility > utility_dict[noble_to_steal_name]:
				noble_to_steal_name = enemy_noble_name

		#Convert the noble from name to object
		#noble_to_steal = search.block_name_to_object(board.all_blocks, noble_to_steal_name)

		#Final noble object
		return utility_dict[noble_to_steal_name]

	def sea_utility(self, board, role, hand, card_prob, loc_prob, possible_sea_moves):
		"""
		returns sea card uility
		possible_sea_moves is a list of lists start and end sea moves
		returns utility (float)
		"""
		utility = [[]]
		for i, start in enumerate(possible_sea_moves):
			for j, end in enumerate(possible_sea_moves[i]):
				utility[i][j] = 7.0

		return computer_decisions.find_n_highest_indeces_table(utility)[0]

	def vic_utility(self, board, role, hand, card_prob, loc_prob, possible_regions):
		"""
		returns vic utility
		possible_regions is list of possible regions
		returns utility (float)
		"""
		utility = []
		for i, region in enumerate(possible_regions):
			utility[i] = 7.0

		return utility[computer_decisions.find_n_highest_indeces()[0]]

	def pil_utility(self, board, role, hand, card_prob, loc_prob, possible_regions):
		"""
		returns pil utility
		possible_regions is a list of possible regions
		returns utility (float)
		"""
		utility = []
		for i, region in enumerate(possible_regions):
			utility[i] = 7.0

		return utility[computer_decisions.find_n_highest_indeces()[0]]
	def tru_utility(self, board, role, hand, card_prob, loc_prob):
		"""
		returns pil utility
		possible_regions is a list of possible regions
		returns utility (float)
		"""
		return 7.0
	def moves_utility(self, board, role, hand, card_prob, path_lst, num_moves = 1):
		"""
		returns move utility
		path_lst is a list of lists with possible paths
		num_moves is 1 2 or 3
		returns utility (float)
		"""
		
		utility = []
		for i, region in enumerate(path_lst):
			utility[i] = 7.0

		utility_to_return
		for utility in computer_decisions.find_n_highest_indeces_table(num_moves):
			utility_to_return += utility

		return utility_to_return


###
###
###
class English(Computer):

	def __init__(self, board):
		'''
		Initializes the English
		'''














