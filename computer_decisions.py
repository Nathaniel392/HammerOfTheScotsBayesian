import random
import blocks
import search
import simulations
import computer_decisions


'''
NEW UTILITY FUNCIONS IN BOARD.PY

find_adjacent_regions_object()
find_adjacent_blocks_roles()
'''

def process_info(*prob_info):
	#Process the information passed in prob_info - logic to prevent crashing from version differences
	if len(prob_info) > 0:
		card_prob = prob_info[0]
	if len(prob_info) > 1:
		loc_prob = prob_info[1]
	if len(prob_info) > 2:
		pass

	return card_prob, loc_prob

def find_n_highest_indeces(value_list, num_values=1, highest=[]):
	'''
	Recursively searches a list of values and returns a list of the indeces of the n highest values
	'''

	#Erroneous input
	if num_values > len(value_list):
		return False

	#Base case
	if len(highest) == num_values:
		return highest

	else:
		#Find the index of the highest value not already stored
		max_value = value_list[0]
		max_index = 0
		for index, value in enumerate(value_list):

			if index not in highest and value > max_value:
				max_value = value
				max_index = index

		highest.append(max_index)
		return find_n_highest_indeces(value_list, num_values, highest)

def likely_blocks(board, region, loc_prob):
	'''
	Returns a list of the most probable blocks that are in the region.
	Returns an equal number of blocks are there are in the region.
	loc_prob:  42x23 table of blocks and the probability they are in a certain region
	'''

	num_blocks_in_region = len(region.blocks_present)

	#Pull a column out of the location probability matrix
	block_probs = []
	for blockID, prob_list in enumerate(loc_prob):
		block_probs.append(prob_list[region.regionID])

	#Find the n highest probability blockIDs from that column
	likely_blocks_IDs = computer_decisions.find_n_highest_indeces(block_probs, num_blocks_in_region)

	#Convert those blockIDs to Block objects - store in new list
	likely_blocks = []
	for index, blockID in enumerate(likely_blocks_IDs):

		#Convert and append
		temp_block_list = board.eng_pool + board.scot_pool
		temp_block = search.block_id_to_object(temp_block_list, blockID)
		likely_blocks.append(temp_block)

	return likely_blocks

def select_card(board, role, hand, *prob_info):

	card_prob, loc_prob = computer_decisions.process_info(prob_info)

	### TEMPORARY									###
	### random choice								###
	###												###
	selected_card = random.choice(hand)				###
	###												###
	###												###
	###												###

	return selected_card

def sea_move(board, role, hand, *prob_info):

	card_prob, loc_prob = computer_decisions.process_info(prob_info)


def herald(board, role, hand, *prob_info):

	###
	#CONSTANTS
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

	card_prob, loc_prob = computer_decisions.process_info(prob_info)
	noble_to_steal = None
	
	#Find enemy regions
	if role == 'ENGLAND':
		enemy_role = 'SCOTLAND'
	else:
		enemy_role = 'ENGLAND'
	enemy_regions = board.get_controlled_regions(enemy_role)

	#Iterate through those regions to find nobles (not Moray)
	enemy_nobles = []
	for enemy_region in enemy_regions:

		#Check every block in the region
		for enemy_block in enemy_region:

			#Append enemy non moray nobles to the noble list
			if type(enemy_block) == blocks.Noble and enemy_block.name != 'MORAY':
				enemy_nobles.append(enemy_block)

	### TEMPORARY									###
	### random choice								###
	###												###
	noble_to_steal = random.choice(enemy_nobles)	###
	return noble_to_steal							###
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
	noble_to_steal = search.block_name_to_object(board.all_blocks, noble_to_steal_name)

	#Final noble object
	return noble_to_steal


	def crown_king(board, role, hand, *prob_info):
		'''
		Determines whether or not to crown a king and which one.
		Returns the Bruce or Comyn block, or False if it doesn't crown
		role should be SCOTLAND, but it's still passed for consistency


		COPY PASTED FROM OLD FUNCTION - DOES NOT WORK
		'''
		card_prob, loc_prob = process_info(prob_info)

		if role != 'SCOTLAND':
			return False

		else:
			#Declaring variables
			king_present = False
			french_present = False

			#Check if the king is already there, french knight, and find comyn and bruce
			for block in board.all_blocks:

				if block.name == 'COMYN':
					comyn = block
				elif block.name == 'BRUCE':
					bruce = block
				elif block.name == 'FRENCH':
					french_present = True
				elif block.name == 'KING' and block.allegiance == 'SCOTLAND':
					king_present = True

			#Boolean for controlling each noble
			control_bruce = bruce in board.scot_roster
			control_comyn = comyn in board.scot_roster

			#Check if SCOTLAND controls FIFE or if it will need to battle for it
			control_fife = board.regions[11].is_friendly('SCOTLAND')

			#King can be crowned 
			if not king_present and not (control_bruce and control_comyn):

				#Check if you have another event card
				event_card = False
				for card in hand:
					if card not in '123' and card != 'HER':
						event_card = True

				#Count the nobles you control loyal to each faction
				friendly_bruce = 0
				friendly_comyn = 0

				#Loop through the board to find Bruce and Comyn loyal nobles
				for block in board.all_blocks:

					#Found a noble - note its loyalty
					if type(block) == blocks.Noble and block.allegiance == 'SCOTLAND':

						if block.loyalty == 'BRUCE':
							friendly_bruce += 1
						elif block.loyalty == 'COMYN':
							friendly_comyn += 1

				#Create a list of every friendly noble, for comyn and bruce too
				friendly_nobles = []
				friendly_bruce_nobles = []
				friendly_comyn_nobles = []

				for block in board.scot_roster:
					if type(block) == blocks.Noble and block.allegiance == 'SCOTLAND':
						friendly_nobles.append(block)

						if block.loyalty == 'BRUCE':
							friendly_bruce_nobles.append(block)
						elif block.loyalty == 'COMYN':
							friendly_comyn_nobles.append(block)

				#Make dictionaries to store the probability that a noble will successfully flip
				bruce_recovery_dict = {}
				comyn_recovery_dict = {}

				'''
				if control_bruce:

					for noble in friendly_bruce_nobles:

						###
						# Run a simulation for the noble and check if SCOTLAND can recover the noble
						###
				'''



				for region_temp in board.regions:
					for block in region_temp:

						if type(block) == blocks.Noble and block.allegiance == 'SCOTLAND':

							#Add the probability of the noble living through the flip to a dictionary
							if len(region_temp.blocks_present) == 1:
								if block.loyalty == 'BRUCE':
									bruce_recovery_dict[block.name] = 1.0
								elif block.loyalty == 'COMYN':
									comyn_recovery_dict[block.name] = 1.0

							#Noble must fight
							else:

								###
								# Run a simulation for the noble and check if SCOTLAND can recover the noble
								###

								#Temporarily flip the noble for the simulation
								block.allegiance = 'ENGLAND'

								attack = [enemy_noble]
								#defense = 

								simulation_results = simulations.simulation(attack, defense, NUM_SIMULATIONS)
								win_rate = simulation_results['attacker wins'] / NUM_SIMULATIONS

								#Flip it back
								enemy_noble.allegiance = role

								#Value from 0-COMBAT_UTILITY, scaled by distance from the WINNING_THRESHOLD
								if win_rate > WINNING_THRESHOLD:
									battle_outcome_util = (win_rate - WINNING_THRESHOLD) / (1.0 - WINNING_THRESHOLD) * COMBAT_UTILITY

							###
							###
							###	UNFINISHED FUNCTION
							###
							###





def main():
	pass

if __name__ == '__main__':
	main()




