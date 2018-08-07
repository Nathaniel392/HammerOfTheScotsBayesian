import retreat

def good_move(board, role, turn, truce):

	"""
	board is a copy of the board
	going to make a move with copies of the board 
	goes and makes the move
	role is scotland or england
	turn is 1 2 3 4 or 5

	finds some utility and throws into random number generator to see if move chosen or not
	"""


	utility = 0


	#count how man value of location of homes owned before:

	value_loc_before = 0
	for region in board.regions:
		
		value_loc_before += retreat.value_of_location(board, region.regionID, role)


	
	#then makes the move on the copy of the board (not finished/not started)


	#find possible regions

	#move is dictionary of block_name (key) and path (value)
	#if path == 'pass' that block does not move

	move = dict()
	possible_regions = list()
	for region in board.regions:
		if region.is_friendly():
			possible_regions.append(region)
	possible_regions.append('pass')

	focus_region = random.choice(possible_regions)
	if focus_region != 'pass':
		for block in focus_region.blocks_present:
			path_table = board.check_all_paths(block.movement_points, focus_region.regionID, block, all_paths = list(), truce = truce)
			path_table.append('pass')
			path_to_take = random.choice(path_table)
			move[block.name] = path_to_take

	

	


	#checks utilitiy of the battles using the retreat elliot's thing
	noble_home_after = 0
	for region in board.regions:
		if region.is_contested():
			simulation_dict = simulations.simulation(board.combat_dict['Attacking'], board.combat_dict['Defending'], 1000, \
				board.combat_dict['Attacking Reinforcements'], board.combat_dict['Defending Reinforcements'])
			if role == board.combat_dict['Attacking'][0]:
				is_attacking = True
			else:
				is_attacking = False
			utility += retreat.retreat(board, region.regionID, [], simulation_dict, is_attacking, turn)['Staying value ']
		


	#account for difference in locations owned values
	value_loc_after = 0
	for region in board.regions:
		
		value_loc_after += retreat.value_of_location(board, region.regionID, role)

	utility += (value_loc_after - value_loc_before) * 4


	#throw in the random number generator with some base bad_move_utility
	#'move' is a substitute for whatever the move will be stored in later
	bad_move_utility = .3

	if utility <= 0:
		utility = .01

	

	utility_dict = {move: utility, 'not move': bad_move}

	if weighted_prob(utility_dict) == move:
		return move
	return False




