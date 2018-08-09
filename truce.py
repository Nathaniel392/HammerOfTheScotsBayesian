import blocks
import search

def tru_utility(self, board):

	if len(self.hand) == 0:
		return 1.0
	else:
		return 0.0000001

	'''

	utility = 0.0

	if self.role == 'ENGLAND':
		enemy_role = 'SCOTLAND'
	else:
		enemy_role = 'ENGLAND'

	friendly_regions = board.get_controlled_regions(self.role)
	friendly_region_IDs = []
	for region in friendly_regions:
		friendly_region_IDs.append(region.regionID)

	enemy_regions = board.get_controlled_regions(enemy_role)

	num_attacking_blocks = 0

	regions_to_test = []

	defending_blocks = []

	#Check if the enemy can attack you - if you're in danger
	for enemy_region in enemy_regions:

		num_enemies_in_region = len(region.blocks_present)

		mp_to_check = 2
		for block in enemy_region:
			if block.movement_points == 3:
				mp_to_check = 3

		#Send a random block to the check_all_paths function - doesn't matter
		temp_block = enemy_region.blocks_present[0]

		all_paths = board.check_all_paths(mp_to_check, enemy_region.regionID, temp_block)

		#Make a list of the potential enemy destinations
		destinations_IDs = []
		for path in all_paths:
			destination_IDs.append(path[-1])

		can_attack = False

		for friendly_region in friendly_regions:
			if friendly_region.ID in destination_IDs:
				can_attack = True

				#Store the blocks in the defending region
				for block in friendly_region.blocks_present:
					defending_blocks.append(block)

		if can_attack:
			num_attacking_blocks += num_enemies_in_region



	num_defending_blocks = len(defending_blocks)

	#Determine the percentage of health points you have
	current_health_sum = 0
	max_health_sum = 0

	for block in defending_blocks:
		current_health_sum += block.current_strength
		max_health_sum += block.attack_strength

	percent_health = current_health_sum / max_health_sum

	#Calculate utility here
	#
	#
	#
	#

	#Check if you control regions that nobles go home to - prevent enemy from attacking those regions

	#Store a list of enemy nobles and and enemy noble home IDs
	enemy_nobles = []
	noble_home_IDs = []
	for block in board.all_blocks:
		if block.allegiance == enemy_role and type(block) == blocks.Noble:
			enemy_nobles.append(block)

			if type(block.home) == int:
				noble_home_IDs.append(block.home)
			else:
				for home_ID in block.home:
					noble_home_IDs.append(home_ID)

	#Check if you control the enemy's nobles' home regions
	for enemy_noble_home_ID in noble_home_IDs:
		temp_region = region_id_to_object(board.all_blocks, enemy_noble_home_ID)

		if temp_region.is_friendly(self.role):








	#Check if there's a region in danger - king, etc
	for friendy_region in friendly_regions:

		#Check if the king is in the region
		king_present = False
		for block in friendly_region.blocks_present:
			if block.type == 'KING':
				king_present = True

		bordering_regions = board.find_adjacent_regions(friendly_region.regionID)

		num_adjacent_enemy_blocks = 0
		surrounded = True
		num_retreatable_regions = 0
		total_adjacent_regions = len(bordering_regions)

		for adjacent_region in bordering_regions:
			if adjacent_region.is_neutral() or adjacent_region.is_friendly(self.role):
				num_retreatable_regions += 1
				surrounded = False

		percent_retreatable_regions = num_retreatable_regions / total_adjacent_regions

		#Most severe case
		if king_present and surrounded:
			return 1.0



	
	'''









