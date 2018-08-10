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

	num_times = 1
	max_utility = 0
	best_move_board = copy.deepcopy(board)
	best_move_string = ''
	computer_passes = False
	for k in range(num_times):
		print('testing move #', k)


		board_copy = copy.deepcopy(board)


		utility = 0

	

		#count how man value of location of homes owned before:

		value_loc_before = 0
		for region in board_copy.regions:
			
			value_loc_before += retreat.value_of_location(board_copy, region.regionID, role)

		
		#does movement
		computer_block = None

		original_blocks_moved = copy.deepcopy(blocks_moved)
		while computer_block in blocks_moved or computer_block == None and not computer_passes:
			

			
			computer_path, computer_block = other_movement.movement_execution(board_copy, 'comp', role, num_moves, truce=truce, blocks_moved = blocks_moved)
			if computer_block == None:
				computer_passes = True
			if computer_block in blocks_moved:
				board_copy = copy.deepcopy(board)
				blocks_moved = copy.deepcopy(original_blocks_moved)




		#debugging why things aren't in combat dictionary
		#for region in board.regions:
			#if region.is_contested():
				#for block in region.blocks_present:
					#if block not in 
		

		#checks utilitiy of the battles using the retreat elliot's thing

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
				
				simulation_dict = simulations.simulation(copy.deepcopy(region.combat_dict['Attacking']), copy.deepcopy(region.combat_dict['Defending']), 1000, \
					copy.deepcopy(region.combat_dict['Attacking Reinforcements']), copy.deepcopy(region.combat_dict['Defending Reinforcements']))
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
				


				if role == region.combat_dict['Attacking'][0].allegiance:
					is_attacking = True
				else:
					is_attacking = False
				utility += retreat.retreat(board_copy, region.regionID, [], simulation_dict, is_attacking, turn)['Staying value '] * 4
				print(retreat.retreat(board_copy, region.regionID, [], simulation_dict, is_attacking, turn)['Staying value '] * 4)


			


		#account for difference in locations owned values
		value_loc_after = 0
		for region in board_copy.regions:
			
			value_loc_after += retreat.value_of_location(board_copy, region.regionID, role)

		utility += (value_loc_after - value_loc_before) * 2


		#throw in the random number generator with some base bad_move_utility
		#'move' is a substitute for whatever the move will be stored in later
		

		if utility <= 0:
			utility = .01

		

		if utility > max_utility:
			max_utility = utility
			best_move_board = copy.deepcopy(board_copy)
			best_move_string = other_movement.get_total_string()
		other_movement.reset_total_string()
	



		
	input('move is going to be utility of:' + str(max_utility))
	print(best_move_string)
	return copy.deepcopy(best_move_board)



