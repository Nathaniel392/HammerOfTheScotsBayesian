import random
import blocks
import search
import simulations


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

def find_n_highest_indeces(value_list, num_values, highest=[]):
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
	likely_blocks_IDs = find_n_highest_indeces(block_probs, num_blocks_in_region)

	#Convert those blockIDs to Block objects - store in new list
	likely_blocks = []
	for index, blockID in enumerate(likely_blocks_IDs):

		#Convert and append
		temp_block_list = board.eng_pool + board.scot_pool
		temp_block = search.block_id_to_object(temp_block_list, blockID)
		likely_blocks.append(temp_block)

	return likely_blocks

def select_card(board, role, hand, *prob_info):

	card_prob, loc_prob = process_info(prob_info)

	### TEMPORARY									###
	### random choice								###
	###												###
	selected_card = random.choice(hand)				###
	###												###
	###												###
	###												###

	return selected_card

def sea_move(board, role, hand, *prob_info):

	card_prob, loc_prob = process_info(prob_info)


def herald(board, role, hand, *prob_info):

	###
	#CONSTANTS
	TOP_CERTAINTY = .90
	CERTAINTY_THRESHOLD = .40
	BLOCK_CERTAINTY_THRESHOLD = .25
	WINNING_THRESHOLD = .75
	NUM_SIMULATIONS = 1000
	###

	card_prob, loc_prob = process_info(prob_info)
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

	#start at the first noble, overwrite it if there's a better one to pick
	noble_to_steal = enemy_nobles[0]

	###
	# Check each noble for successful steal probability (combat) and value after steal
	###
	for enemy_noble in enemy_nobles:

		#Declaring variables here
		win_fight = None
		good_position = None
		possible_king = None


		###
		# Find the region that that noble is most likely to be in
		###
		likely_region = None
		region_found = False

		#List of probabilities that a noble is in a region - indeces are regionIDs - find the most probable one
		noble_region_probability = loc_prob[enemy_noble.regionID]
		most_probable_region_index_list = find_n_highest_indeces(noble_region_probability, 1)

		likely_region = search.region_id_to_object(most_probable_region_index_list[0])

		#Look at the combat immediately after - run most probable enemies through a simulation
		num_blocks_in_region = len(enemy_noble_region.blocks_present)
		num_other_blocks = num_blocks_in_region - 1

		###
		# Check if you can actually win the fight after flipping the noble
		###
		win_fight = False

		#That noble is alone in the region
		if num_blocks_in_region == 1:
			win_fight = True

		#Noble will have to fight after flipping
		else:

			likely_blocks = likely_blocks(board, region, loc_prob)

			#Possible error in previous calculations - lowers value of choosing this region
			if enemy_noble not in likely_blocks:
				#
				# Do something here
				#
				pass
			else:
				likely_blocks.remove(enemy_noble)


			###
			# Run a simulation with the most probable blocks in the area
			###
			attack = [enemy_noble]
			defense = likely_blocks

			simulation_results = simulations.simulation(attack, defense, NUM_SIMULATIONS)
			win_rate = simulation_results['attacker wins'] / NUM_SIMULATIONS

			if win_rate >= WINNING_THRESHOLD:
				win_fight = True

		#If the block has a high chance of successfully flipping and winning the battle
		if win_fight:

			###
			# Look at the surrounding regions to see if it is in danger or in a good position
			###

			adjacent_regions = board.find_adjacent_regions_object(region)

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

			good_position = False
			#More adjacent friends than enemies
			if num_adjacent_friendly_blocks > num_adjacent_enemy_blocks:
				good_position = True
		
		###
		# Account for taking Bruce or Comyn to crown a king
		###
		if role == 'SCOTLAND':

			#Declaring variables
			king_present = False
			french_present = False

			#Check if the king is already there, french knight, and find comyn and bruce's locations
			for region_temp in board.regions:
				for block in region_temp.blocks_present:

					if block.name == 'COMYN':
						comyn = block
						comyn_region = region_temp
					elif block.name == 'BRUCE':
						bruce = block
						bruce_region = region_temp
					elif block.name == 'FRENCH':
						french_present = True
					elif block.name == 'KING' and block.allegiance == 'SCOTLAND':
						king_present = True

			#King can be crowned 
			if not king_present:
				#Count the nobles you control loyal to each faction
				friendly_bruce = 0
				friendly_comyn = 0

				#Loop through all blocks to count the nobles
				friendly_regions = board.get_controlled_regions(role)

				for friendly_region in friendly_regions:
					for block in friendly_region.blocks_present:

						#Found a noble - note its loyalty
						if type(block) == blocks.Noble:

							if block.loyalty == 'BRUCE':
								friendly_bruce += 1
							elif block.loyalty == 'COMYN':
								friendly_comyn += 1

				

				#
				#
				# Stopped working here thursday
				#
				#










	return noble_to_steal



def main():
	pass

if __name__ == '__main__':
	main()




