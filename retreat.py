import simulations
import blocks
import weighted_prob
import region_danger
import play_game
def find_location(board, blok):
	'''
	This function takes a board object and the name of a block
	and returns a region object where the block is
	'''

	
	for region in board.regions:
		for bllock in region.blocks_present:
			
			if bllock.name == blok.name:
				return region

def retreat(board, regionID, locations, simulation_dict, is_attacking, turn, combat_dict={}):
	'''
	This function is meant to calculate a weight to whether or not 
	the computer opponent should retreat at any point during
	a battle. regionID is a region ID, paths is a list of the possible
	paths of retreating, simulation_dict contains the win percentages from
	the simulations and average strength lost values. is_attacking is a boolean
	that is True if the computer is attacking and False if the computer is
	defending
	'''

	if len(combat_dict) == 0:
		play_game.set_up_combat_dict(board,board.regions[regionID])
		combat_dict = board.regions[regionID].combat_dict



	if(len(combat_dict['Attacking']) == 0 or len(combat_dict['Defending']) == 0):

		return_dict = {'Staying value ': 10}
		return return_dict


	#Valuable Blocks and respective weights
	valuable_blocks = {'WALLACE':18, 'KING':22, 'EDWARD':16, 'HOBELARS':13}

	if (is_attacking and combat_dict['Attacking'][0].allegiance == 'ENGLAND') or (not is_attacking and combat_dict['Defending'][0].allegiance == 'ENGLAND'):

		role = 'ENGLAND'

	else:

		role = 'SCOTLAND'

	staying_value = value_of_location(board, regionID, role) * 1.3

	retreating_value = 0

	friendly_block_names = list()

	friendly_blocks = list()

	enemy_block_names = list()

	enemy_blocks = list()

	return_dict = {'Staying value ': staying_value}

	

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

		for block in combat_dict['Attacking']:

			friendly_block_names.append(block.name)
			friendly_blocks.append(block)

		for block in combat_dict['Defending']:

			enemy_block_names.append(block.name)
			enemy_blocks.append(block)

	else:

		for block in combat_dict['Defending']:

			friendly_block_names.append(block.name)
			friendly_blocks.append(block)

		for block in combat_dict['Attacking']:

			enemy_block_names.append(block.name)
			enemy_blocks.append(block)

	#Check to see if any of the friendly blocks are the valuable blocks
	if len(friendly_blocks) == 0 and friendly_blocks[0].current_strength == 1:
		retreating_value += 10

	for block_name in valuable_blocks:

		if block_name in friendly_block_names:

			retreating_value += valuable_blocks[block_name]

		elif block_name in enemy_block_names:

			retreating_value += -.5 * valuable_blocks[block_name]

	#Weight if you are going to lose a noble
	for block in friendly_blocks:

		if type(block) == blocks.Noble:

			retreating_value +=  noble_going_to_be_lost(board, block, role, turn) * -8

			retreating_value += noble_not_going_to_be_occupied(board, block, turn, role) * 8 

	#Weight if the enemy is going to lose a noble
	for block in enemy_blocks:

		if type(block) == blocks.Noble:

			retreating_value += noble_going_to_be_lost(board, block, role, turn) * 6

			retreating_value += noble_not_going_to_be_occupied(board, block, turn, role) * -6
	if 'WALLACE' in friendly_block_names and len(enemy_blocks) == 1:

		retreating_value = 1

	for location in locations:

		return_dict[location] = value_of_location(board, location, role) * retreating_value

	for key in return_dict:
		
		if return_dict[key] <= 0:
			return_dict[key] = 0.000000001

	return return_dict



def noble_going_to_be_lost(board, noble_object, role, turn):
	"""
	returns float
	1.0 means better chances of being lost
	0.0 means lower chances of being lost
	very arbitrary numbers
	not very good indication
	"""

	close_to_winter = .2 * turn
	lost_flt = 0.0
	if type(noble_object.home_location) == int:
		home_location_tuple = (noble_object.home_location,)
	else:
		home_location_tuple = noble_object.home_location

	#checking who occupies it
	for home_location_id in home_location_tuple:
		if board.regions[home_location_id].is_enemy(role):
			lost_flt += 0.7
		elif board.regions[home_location_id].is_friendly(role):
			lost_flt += 0.03
		else:
			lost_flt += 0.2

		#checking who is around the noble_home_location
		current_location = find_location(board, noble_object)
		for regionID, border in enumerate(board.dynamic_borders[current_location.regionID]):
			if border != 0:
				if board.regions[regionID].is_enemy(role):
					lost_flt += 0.3
				elif board.regions[regionID].is_friendly(role):
					lost_flt += .01
				else:
					lost_flt += .07

	return lost_flt * close_to_winter
def noble_going_to_be_kept(board, noble_object, turn, role):
	"""
	returns between 0.0 and 1.0
	1.0 more likely to be kept
	"""
	return (1 - noble_going_to_be_lost(board, noble_object, turn, role))

def noble_not_going_to_be_occupied(board, noble_object, turn, role):
	"""
	returns between 0.0 and 1.0
	1.0 home locatino more likely to be not occupied
	"""
	lost_flt = 0.0
	close_to_winter = .2 * turn
	if type(noble_object.home_location) == int:
		home_location_tuple = (noble_object.home_location, )
	else:
		home_location_tuple = noble_object.home_location

	#checking who occupies it
	for home_location_id in home_location_tuple:
		if board.regions[home_location_id].is_enemy(role):
			lost_flt += 0.05
		elif board.regions[home_location_id].is_friendly(role):
			lost_flt += 0.05
		else:
			lost_flt += 0.7

		#checking who is around the noble_home_location
		current_location = find_location(board, noble_object)
		for regionID, border in enumerate(board.dynamic_borders[current_location.regionID]):
			if border != 0:
				if board.regions[regionID].is_enemy(role):
					lost_flt += 0.13
				elif board.regions[regionID].is_friendly(role):
					lost_flt += 0.13
				else:
					lost_flt += 0.3
	return lost_flt * close_to_winter

def value_of_location(current_board, regionID, role):
	"""
	returns float between 0.0 and 1.0
	ROSS            0  F T 1
GARMORAN        1  F T 0
MORAY           2  F T 2
STRATHSPEY      3  T T 1 
BUCHAN          4  F T 2
LOCHABER        5  F T 1 
BADENOCH        6  F F 2
MAR             7  F F 1
ANGUS           8  F T 2
ARGYLL          9  F T 2
ATHOLL          10 F F 1
FIFE            11 T T 2
LENNOX          12 T T 1 
MENTIETH        13 F T 3
CARRICK         14 F T 1
LANARK          15 F F 2
LOTHIAN         16 F T 2
DUNBAR          17 F T 2
SELKIRK-FOREST  18 F F 0
GALLOWAY        19 F T 1
ANNAN           20 F T 2
TEVIOT          21 F F 1
ENGLAND         22 F T 0
	"""
	enemy_strength_lst = region_danger.table(current_board, role)
	value_lst = [22, 5, 14, 10, 30, 11, 15, 18, 37, 17, 21, 42, 27, 50, 11, 26, 13, 17, 5, 19, 15, 12, 11]

	for i, number in enumerate(enemy_strength_lst):
		if number != -1:
			value_lst[i] -= number
		value_lst[i] = value_lst[i] / 50
		if value_lst[i] < 0:
			value_lst[i] = 0
	#print('VALUE ' + str(value_lst[regionID]))
	return value_lst[regionID]








	




