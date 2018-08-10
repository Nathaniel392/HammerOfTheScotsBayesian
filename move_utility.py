import retreat
import random
import weighted_prob
import copy
import simulations
import other_movement




def good_move(board, num_moves, role, turn, truce, blocks_moved):
	
	"""
	board is a copy of the board
	going to make a move with copies of the board 
	goes and makes the move
	role is scotland or england
	turn is 1 2 3 4 or 5
	finds some utility and throws into random number generator to see if move chosen or not





	READ ME READ ME READ ME READ ME READ ME READ ME
	MAKES A COPY OF THE BOARD DOES THE MOVE EVALUATES THE MOVE IF BAD MOVE AGAIN AND CONTINUE LOOPING
	UNTIL FINDS GOOD MOVE AND THEN IT EXECUTES IT ON THE ACTUAL BOARD
	"""

	board_copy = copy.deepcopy(board)


	utility = 0


	#count how man value of location of homes owned before:

	value_loc_before = 0
	for region in board_copy.regions:
		
		value_loc_before += retreat.value_of_location(board_copy, region.regionID, role)

	computer_block = None
	
	#does movement
	

	computer_path, computer_block = other_movement.movement_execution(board_copy, 'comp', role, num_moves, truce=truce)


	#debugging why things aren't in combat dictionary
	#for region in board.regions:
		#if region.is_contested():
			#for block in region.blocks_present:
				#if block not in 
	

	#checks utilitiy of the battles using the retreat elliot's thing
	noble_home_after = 0
	for region in board_copy.regions:
		if region.is_contested():
			'''
			
			print("***ATTACKING***")
			print(region.combat_dict['Attacking'])
			print("******")
			print("***DEFENDING***")
			print(region.combat_dict['Defending'])
			print("******")
			print('attack reinforcements')
			print(region.combat_dict['Attacking Reinforcements'])
			print('defense reinforcements')
			print(region.combat_dict['Defending Reinforcements'])
			'''
			
			combat_dict = copy.deepcopy(region.combat_dict)

			simulation_dict = simulations.simulation(combat_dict['Attacking'], combat_dict['Defending'], 1000, \
				combat_dict['Attacking Reinforcements'], combat_dict['Defending Reinforcements'])
			'''
			print("***ATTACKING***")
			print(region.combat_dict['Attacking'])
			print("******")
			print("***DEFENDING***")
			print(region.combat_dict['Defending'])
			print("******")

			#for key in region.combat_dict:
				#print(region.combat_dict[key])
			'''
			


			if role == combat_dict['Attacking'][0].allegiance:
				is_attacking = True
			else:
				is_attacking = False
			utility += retreat.retreat(board_copy, region.regionID, [], simulation_dict, is_attacking, turn,combat_dict)['Staying value '] * 4
		


	#account for difference in locations owned values
	value_loc_after = 0
	for region in board_copy.regions:
		
		value_loc_after += retreat.value_of_location(board_copy, region.regionID, role)

	utility += (value_loc_after - value_loc_before) * 2


	#throw in the random number generator with some base bad_move_utility
	#'move' is a substitute for whatever the move will be stored in later
	bad_move_utility = 5

	if utility <= 0:
		utility = .01

	

	utility_dict = {'move': utility, 'not move': bad_move_utility}

	if weighted_prob.weighted_prob(utility_dict) == 'move':
	#if utility > bad_move_utility:
		#total_string = ''
		#pause
		print('computer ready to make a move')
		input()
		
		board.move_block(computer_block,computer_path[0], end = computer_path[-1], position='comp', is_truce=truce, path = computer_path)
		other_movement.reset_total_string()
		print('computer done with move')
		input()
		return board
	else:
		
	
		
		return good_move(board, num_moves, role, turn, truce, bad_move_utility)



