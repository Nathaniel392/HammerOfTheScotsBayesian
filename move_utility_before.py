import retreat
import random
import weighted_prob
import copy
import simulations

#very sorry for the global variable
#it is up to sid to fix it
total_string = ''
def move_block(board, block, start, end = -1, position = 'comp', prev_paths = [], is_truce = False):
		'''
		Changes a block's location on the board, assuming that all conditions are legal. 
		Adds them to appropriate dictionaries if in a combat or attack scenario

		Takes a list of all previous paths taken in that turn
		Takes a position -- computer or opponent

		block:  
		start:  starting location (Region ID)
		end:  end location (Region ID)


		READ ME:
		same move block but without print statements, instead add to total_string so that output only once when good move
		'''
		global total_string

		

		if position == 'comp':
			#print('comp tried to move')

			#Find every path from the start regionID to the end regionID and put them in a list
			paths = board.check_path(block.movement_points,start,end, block, all_paths = list())

			#print(paths)
			#If valid paths exist, keep going
			if paths:

				#print('THERE IS A VALID PATH')
				computer_path = random.choice(paths)
				print('computer chose ' + str(computer_path))
				total_string += 'computer chose ' + str(computer_path) + '\n'


				path_taken = False



				for path in prev_paths:

					if path == computer_path:

						path_taken = True

						break

				#If the final region in the path is contested
				if board.regions[end].is_contested():
			
					#Remove the block from its starting location
					board.regions[start].blocks_present.remove(block)

					#Move it to the correct dictionary list
					if board.regions[end].blocks_present[0].allegiance != block.allegiance and path_taken: 
						board.regions[end].combat_dict['Attacking'].append(block)
					
					elif board.regions[end].blocks_present[0].allegiance != block.allegiance and board.regions[end].name == 'ENGLAND' and path_taken:
						board.regions[end].combat_dict['Attacking'].append(block)

					elif board.regions[end].blocks_present[0].allegiance != block.allegiance:
						board.regions[end].combat_dict['Attacking Reinforcements'].append(block)
						board.attacked_borders[computer_path[-2]][end] = 'attack'
					
					else:
						board.regions[end].combat_dict['Defending Reinforcements'].append(block)
						board.attacked_borders[computer_path[-2]][end] = 'defense'

					#Add it to the region's overall block list as well
					board.regions[end].blocks_present.append(block)

					#print('Moved into contested region.')
					total_string += 'Moved into contested region.\n'
					#print(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)
					total_string += block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name + '\n'
				#End location is not contested

				else:

					#If it's an enemy controlled region
					if len(board.regions[end].blocks_present) != 0 and board.regions[end].blocks_present[0].allegiance != block.allegiance:

						#Stop the function if it's truce
						if is_truce:
							#print("You can't move there fool, issa truce")
							total_string += 'comp tried to move into truce region\n'
							return False
			  
						#Set the defending blocks into the defending dictionary
						for defending_block in board.regions[end].blocks_present:
							board.regions[end].combat_dict['Defending'].append(defending_block)

						#Move the attacking into the attacking dictionary
						board.regions[end].combat_dict['Attacking'].append(block)
						board.regions[end].blocks_present.append(block)
						board.regions[start].blocks_present.remove(block)

						
						if not path_taken:
							if type(prev_paths) != list:
								prev_paths = list(prev_paths)
								
							prev_paths.append(computer_path)
							


							if computer_path[-1] == 22 or computer_path[0] == 22:
								#if set don't change it in cardplay
								prev_paths = tuple(prev_paths)

						
						#print('Moved into enemy region')
						total_string += 'Moved into enemy region \n'
						#print(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)
						total_string += block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name + '\n'

						#Set the border between the last and second to last region in the path to attacked



						###temporary
						#print(computer_path)
						total_string += str(computer_path) + '\n'
						#print('updating border between', computer_path[-2], 'and', end)
						###
						board.attacked_borders[computer_path[-2]][end] = 'attack'



					#Friendly or neutral
					else:
						board.regions[start].blocks_present.remove(block)
						board.regions[end].blocks_present.append(block)
						#print('Moved to friendly or neutral region')
						total_string += 'Moved to friendly or neutral region \n'
						#print(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)
						total_string += block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name + '\n'

				#Decrement the border limits of each border in the path
				for i in range(len(computer_path)-2):
					board.dynamic_borders[computer_path[i]][computer_path[i+1]] -= 1

			#No valid paths
			else:
				return False

		#Human player input
		else:	#if position == 'opp'

			raise Exception('not supposed to be opp')

			taking_input = True

			user_path = [start]

			print ("Enter your path ('done' to stop):")

			counter = 1
			user_input_region = False
			while taking_input:

				print(user_path)

				user_input = input("Location " + str(counter) + ": ")
				
				user_input_region = search.region_name_to_id(board,user_input.upper())

				#If it's a valid region, add it to the list

				if type(user_input_region) == int and (user_input_region == 0 or user_input_region):

					if user_input_region == start:

						print("Don't include starting location!")

					else:

						user_path.append(user_input_region)

						counter += 1

				#Stop taking input
				elif user_input.lower() == 'done':

					taking_input = False

				#Invalid input
				else:

					print ("Not a valid location!")

			end = user_path[-1]
			potential_paths = board.check_path(block.movement_points,user_path[0],user_path[-1], block, all_paths = [])
			print(potential_paths)
			if user_path in potential_paths:

				path_taken = False

				for path in prev_paths:

					if path == user_path:

						path_taken = True

						break


				#If the final region in the path is contested
				if board.regions[end].is_contested():
			
					#Remove the block from its starting location
					board.regions[start].blocks_present.remove(block)

					#Move it to the correct dictionary list
					if board.regions[end].blocks_present[0].allegiance != block.allegiance and path_taken: 
						board.regions[end].combat_dict['Attacking'].append(block)

					elif board.regions[end].blocks_present[0].allegiance != block.allegiance and board.regions[end].name == 'ENGLAND' and path_taken:
						board.regions[end].combat_dict['Attacking'].append(block)

					elif board.regions[end].blocks_present[0].allegiance != block.allegiance:
						board.regions[end].combat_dict['Attacking Reinforcements'].append(block)
						board.attacked_borders[user_path[-2]][end] = 'attack'

					else:
						board.regions[end].combat_dict['Defending Reinforcements'].append(block)
						board.attacked_borders[user_path[-2]][end] = 'defense'

					#Add it to the region's overall block list as well
					board.regions[end].blocks_present.append(block)
					#print('Moved into contested region.')
					total_string += 'Moved into contested region \n'
					#print(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)
					total_string += block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name + '\n'
					#print(board.regions[end].combat_dict['Attacking'])
				#End location is not contested
				else:

					#If it's an enemy controlled region
					if len(board.regions[end].blocks_present) != 0 and board.regions[end].blocks_present[0].allegiance != block.allegiance:

						#Stop the function if it's truce
						if is_truce:
							print("You can't move there fool, issa truce")
							return False
			  
						#Set the defending blocks into the defending dictionary
						for defending_block in board.regions[end].blocks_present:
							board.regions[end].combat_dict['Defending'].append(defending_block)

						#Move the attacking into the attacking dictionary
						print('SHOULD BE ADDING TO ATTACKING ' + block.name)
						board.regions[end].combat_dict['Attacking'].append(block)
						board.regions[end].blocks_present.append(block)
						board.regions[start].blocks_present.remove(block)

						if not path_taken:
							if type(prev_paths) != list:
								prev_paths = list(prev_paths)
							prev_paths.append(user_path)

							if user_path[-1] == 22 or user_path[0] == 22:
								prev_paths = tuple(prev_paths)
								


						#print('Moved into enemy region')
						total_string += 'Moved into enemy region \n'
						#print(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)
						total_string += block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name + '\n'
						#Set the border between the last and second to last region in the path to attacked

						###temporary
						print(user_path)
						print('updating border between', user_path[-2], 'and', end)
						###
						board.attacked_borders[user_path[-2]][end] = 'attack'

					#Friendly or neutral
					else:
						board.regions[start].blocks_present.remove(block)
						board.regions[end].blocks_present.append(block)
						#print('Moved to friendly or neutral region')
						total_string += 'Moved to friendly or neutral region\n'
						#print(block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name)
						total_string += block.name + " was moved from " + board.regions[start].name + " to " + board.regions[end].name + '\n'

				#Decrement border limits on borders crossed in the path
				for i in range(len(user_path)-2):

					board.dynamic_borders[user_path[i]][user_path[i+1]] -= 1

			#No valid paths
			else:

				return False

		#Successfully executed
		
		return True
def movement_execution(board, position, role, num_moves, truce=False):
	'''
	currently has unnecessary print statements because it was copy and pasted
	and rather unnessary code in general but that can't be helped
	when you just want to copy paste :P
	'''

	global total_string

	

	blocks_moved = []
	picked_regions = []
	move_pt = 0
	#Pick n regions to 
	while move_pt < num_moves:
		#print("LOOPING AGAIN", move_pt, num_moves)

		#print(move_pt)
		#print (blocks_moved)

		focus_region = None
		
		try:
	   
			if type(prev_paths) != tuple:
				prev_paths = []
			else:
				
				prev_paths = list(prev_paths)


		except UnboundLocalError:
			prev_paths = list()

	 



		passed = False
		#FIND A FOCUS REGION AND PATH
		if position == 'opp':

			user_region_input = ''

			#Loop until valid input for a focus region.
			valid_region_input = False
			while not valid_region_input:

				#Take a region name input, then try to convert it into a region object
				user_region_input = input('Which region would you like to focus your movement (or pass)?\n>').strip().upper()

				if user_region_input.lower() == 'pass':
					passed = True
					break

				focus_region = search.region_name_to_object(board, user_region_input)

				#If it's actually a region - valid region name
				if focus_region:
					#Inputted region is friendly and unique
					if focus_region in board.get_controlled_regions(role) and focus_region not in picked_regions:
						valid_region_input = True
					#Not friendly or neutral
					else:
						print('Invalid region. Please select a region you control that hasn\'t been moved')
				
				#Invalid region name
				else:
					print('Invalid input. Please input a valid region name.')



		elif position == 'comp':
			#print('Num of move= ', move_pt)
			#input('Computer Move Part 1')
			###
			###TEMPORARY
			###

			#Get a random starting region

			unique_region = False
			while not unique_region:

				friendly_regions = board.get_controlled_regions(role)
				rand_startID = random.randint(0, len(friendly_regions) - 1)
				focus_region = friendly_regions[rand_startID]

				if focus_region not in picked_regions:
					unique_region = True
			#print('Focus Region = ', focus_region.name)

		if passed:
			move_pt += 1
			continue

		if focus_region.name != 'ENGLAND':
			
			picked_regions.append(focus_region)
		#assigns moveable count for contested regions

		if focus_region.is_contested():

			num_enemy = len(focus_region.combat_dict['Attacking'])

			num_friends = len(focus_region.combat_dict['Defending'])

			moveable_count = num_friends - num_enemy

		#assigns moveable count for 
		else:

			moveable_count = len(focus_region.blocks_present)

		if focus_region.name == 'ENGLAND' and num_moves > move_pt:

			#print(focus_region.blocks_present)

			if position == 'opp':

				valid_block = False

				while not valid_block and num_moves > move_pt:

					user_block_name = input("Choose a block to move (type 'done' if done): ").strip().upper()

					if user_block_name.lower() == "done":

						print ("You passed one movement point!")

						valid_block = True

					board_blocks = board.eng_roster + board.scot_roster
					user_block = search.block_name_to_object(board_blocks, user_block_name)

					if user_block:

						if user_block in focus_region.blocks_present:

							if user_block not in blocks_moved:

								if move_block(board, user_block,focus_region.regionID,position='opp',prev_paths=prev_paths,is_truce=truce) == False:

									print ("That path was not valid!")

								else:
									#move_pt +=1
									prev_paths = tuple(prev_paths)


									blocks_moved.append(user_block)

									valid_block = True

						  

							else:

								print ("You have already moved that block this turn!")

						else:

							print ("That block is not in the region!")

					else:

						print ("Please input a valid block name!")

			elif position == 'comp':

				#print('It is computer turn to make a move')

				computer_choice = random.randint(0,100)

				if computer_choice == 0:

					#print ("Computer Passes a Movement Point")
					total_string += "Computer Passes a Movement Point\n"

				else:


					for block in focus_region.blocks_present:
						if num_moves > move_pt:
							possible_paths = board.check_all_paths(block.movement_points,focus_region.regionID,block,all_paths = [], truce=truce)

							if possible_paths:
								print(possible_paths)
								computer_path1 = random.choice(possible_paths)

								end = computer_path1[-1]

								move_block(board, block,focus_region.regionID,end=end,position='comp',prev_paths=prev_paths,is_truce=truce)
								#move_pt +=1
							else:

								#print("Computer chosen region has no moves!")
								total_string += "Computer chosen region has no moves!\n"

		else:
			count = 0
			can_go_again = True
			for i in range(moveable_count):

				if position == 'opp' and can_go_again:

					valid_block = False

					while not valid_block:

						user_block_name = input("Choose a block to move (type 'done' if done): ").strip().upper()

						if user_block_name.lower() == "done":

							print ("You passed one movement point!")

							valid_block = True

						board_blocks = board.eng_roster + board.scot_roster
						user_block = search.block_name_to_object(board_blocks, user_block_name)

						if user_block:

							if user_block in focus_region.blocks_present:

								if user_block not in blocks_moved:

									if move_block(board, user_block,focus_region.regionID,position='opp',prev_paths=prev_paths,is_truce=truce) == False:

										print ("That path was not valid!")

									else:
										

										if combat.find_location(board, user_block).name == 'ENGLAND':
											can_go_again = False
											picked_regions.remove(focus_region)
										blocks_moved.append(user_block)

										valid_block = True

								else:

									print ("You have already moved that block this turn!")

							else:

								print ("That block is not in the region!")

						else:

							print ("Please input a valid block name!")

				

				elif position == 'comp' and can_go_again:
					#input('Computer Move Part 2')
					#print('It is computer turn to make a move')

					computer_choice = random.randint(0,100)
					
					if computer_choice == 0:

						#print ("Computer Passes a Movement Point")
						total_string += "Computer Passes a Movement Point\n"

					else:
						#print('Reset List')
						possible_paths_2 = list()
						
						block_index = i - count
						block = focus_region.blocks_present[block_index]

						if block not in blocks_moved:
							possible_paths_2 = board.check_all_paths(block.movement_points,focus_region.regionID,block,path=[], all_paths=[],truce=truce, role = role)

							
							#print("CHECK PATHS", board.check_all_paths(block.movement_points,focus_region.regionID,block,truce=truce))
							if possible_paths_2:

								computer_paths_1 = copy.deepcopy(random.choice(possible_paths_2))
								#print(possible_paths_2)
								end = computer_paths_1[-1]
								

								move_block(board, block,focus_region.regionID,end=end,position='comp',prev_paths=prev_paths,is_truce=truce)
								if board.regions[end].name == 'ENGLAND':
									prev_paths = tuple(prev_paths)
									can_go_again = False
									picked_regions.remove(focus_region)
								else:
									if type(prev_paths) == list:
										prev_paths.append(computer_paths_1)
								count+=1
								blocks_moved.append(block)

							#print(move_pt)

						else:

							#print("Computer chosen region has no moves!")
							total_string += "Computer chosen region has no moves!\n"
		#print(can_go_again)
		#print(move_pt)
		move_pt+=1

def good_move(board, num_moves, role, turn, truce, original_board):

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

	global total_string

	utility = 0


	#count how man value of location of homes owned before:

	value_loc_before = 0
	for region in board.regions:
		
		value_loc_before += retreat.value_of_location(board, region.regionID, role)


	
	#does movement

	board_copy = copy.deepcopy(board)
	movement_execution(board_copy, 'comp', role, num_moves, truce=truce)


	

	


	#checks utilitiy of the battles using the retreat elliot's thing
	noble_home_after = 0
	for region in board_copy.regions:
		if region.is_contested():

			set_up_combat_dict(board_copy,region)
			
			simulation_dict = simulations.simulation(region.combat_dict['Attacking'], region.combat_dict['Defending'], 1000, \
				region.combat_dict['Attacking Reinforcements'], region.combat_dict['Defending Reinforcements'])
			for key in region.combat_dict:
				print(region.combat_dict[key])
			if role == region.combat_dict['Attacking'][0].allegiance:
				is_attacking = True
			else:
				is_attacking = False
			utility += retreat.retreat(board_copy, region.regionID, [], simulation_dict, is_attacking, turn)['Staying value '] * 4
		


	#account for difference in locations owned values
	value_loc_after = 0
	for region in board_copy.regions:
		
		value_loc_after += retreat.value_of_location(board_copy, region.regionID, role)

	utility += (value_loc_after - value_loc_before) * 2


	#throw in the random number generator with some base bad_move_utility
	#'move' is a substitute for whatever the move will be stored in later
	bad_move_utility = .1 * num_moves

	if utility <= 0:
		utility = .01

	

	utility_dict = {'move': utility, 'not move': bad_move_utility}

	if weighted_prob.weighted_prob(utility_dict) == 'move':
		total_string = ''
		#pause
		print('computer ready to make a move')
		input()
		movement_execution(board, 'comp', role, num_moves, truce=truce)
		original_board = board_copy
		print(total_string)
		total_string = ''
		print('computer done with move')
		input()
		
	else:
		total_string = ''
		good_move(original_board, num_moves, role, turn, truce, original_board)
		


