import simulation
import blocks

def retreat(board, regionID, locations, simulation_dict, is_attacking, turn):
	'''
	This function is meant to calculate a weight to whether or not 
	the computer opponent should retreat at any point during
	a battle. regionID is a region ID, paths is a list of the possible
	paths of retreating, simulation_dict contains the win percentages from
	the simulations and average strength lost values. is_attacking is a boolean
	that is True if the computer is attacking and False if the computer is
	defending
	'''

	#Valuable Blocks and respective weights
	valuable_blocks = {'WALLACE':18, 'KING':22, 'EDWARD':16, 'HOBELARS':13}

	staying_value = value_of_location(board, regionID, role) * 5

	retreating_value = 0

	friendly_block_names = list()

	friendly_blocks = list()

	enemy_block_names = list()

	enemy_blocks = list()

	return_dict = {'Staying value': staying_value}

	if (is_attacking and board.regions[regionID].combat_dict['Attacking'][0].allegiance == 'ENGLAND') or (not is_attacking and board.regions[regionID].combat_dict['Defending'][0].allegiance == 'ENGLAND'):

		role = 'ENGLAND'

	else:

		role = 'SCOTLAND'

	#Add weight based on the difference is strength lost in the battle
	if is_attacking:

		strength_dif = simulation_dict['Attacker strength lost'] - simulation_dict['Defender strength lost']

	elif not is_attacking:

		strength_dif = simulation_dict['Defender strength lost'] - simulation_dict['Attacker strength lost']

	if role == 'SCOTLAND':

		retreating_value += strength_dif * 4

	else:

		retreating_value += strength_dif * 2



	#Add weight based on the results of the simulation
	if not is_attacking:

		retreating_value += simulation_dict['attacker wins'] * 10

	else:

		retreating_value += simulation_dict['defender wins'] * 10

		retreating_value += simulation_dict['attacker retreats'] * 2

	#Create a list of friendly blocks in the current battle
	if is_attacking:

		for block in board.regions[regionID].combat_dict['Attacking']:

			friendly_block_names.append(block.name)
			friendly_blocks.append(block)

		for block in board.regions[regionID].combat_dict['Defending']:

			enemy_block_names.append(block.name)
			enemy_blocks.append(block)

	else:

		for block in board.regions[regionID].combat_dict['Defending']:

			friendly_block_names.append(block.name)
			friendly_blocks.append(block)

		for block in board.regions[regionID].combat_dict['Attacking']:

			enemy_block_names.append(block.name):
			enemy_blocks.append(block)

	#Check to see if any of the friendly blocks are the valuable blocks
	for block_name in valuable_blocks:

		if block_name in friendly_block_names:

			retreating_value += valuable_blocks[block_name]

		elif block_name in enemy_block_names:

			retreating_value += -.5 * valuable_blocks[block_name]

	#Weight if you are going to lose a noble
	for block in friendly_blocks:

		if type(block) == blocks.Noble:

			retreating_value +=  noble_going_to_be_lost(board, block, role, turn) * -8

			retreating_value += noble_not_going_to_be_occupied(board, block, role, turn) * 8 

	#Weight if the enemy is going to lose a noble
	for block in enemy_blocks:

		if type(block) == blocks.Noble:

			retreating_value += noble_going_to_be_lost(board, block, role, turn) * 6

			retreating_value += noble_not_going_to_be_occupied(board, block, role, turn) * -6


	for location in locations:

		return_dict[location] = value_of_location(board, location, role) * retreating_value


	return return_dict








	




