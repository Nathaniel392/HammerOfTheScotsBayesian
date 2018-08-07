import math
import random
import search
import blocks
import board
import weighted_prob

def find_location(board, blok):
	for region in board.regions:
		for bllock in region.blocks_present:
			
			if bllock.name == blok.name:
				return region
	return False

def choose_location(location_list,allegiance,eng_type,scot_type, block):

	'''
	takes a list of locations and a block allegiance
	returns a random location from list or a user decision
	can be updated to do a smarter decision
	'''

	if allegiance == 'ENGLAND':

		if eng_type == 'comp':

			index = random.randint(0,len(location_list)-1)

			return location_list[index]

		elif eng_type == 'opp':

			new_bool = True

			while new_bool:

				print("Where would you like " + block.name + " to go? ")

				for ind, location in enumerate(location_list):
					if type(location) != str:
						print(location.name + "[" + str(ind) + ']')

				print('Type pool to disband')
				user_input = input('>')
				if user_input == 'pool' and user_input in location_list:
					if allegiance == 'SCOTLAND':
						return 'scottish pool'
					else:
						return 'english pool'

				else:

					try:

						return location_list[int(user_input)]

						new_bool = False

					except (ValueError,IndexError):

						return ("Invalid Input!!")

	if allegiance == 'SCOTLAND':

		if scot_type == 'comp':

			index = random.randint(0,len(location_list)-1)

			return location_list[index]

		elif scot_type == 'opp':

			new_bool = True

			while new_bool:

				print("Where would you like " + block.name + " to go? ")
    
				for ind, location in enumerate(location_list):
					if type(location) != str:
						print(location.name + "[" + str(ind) + ']')

				print('Type pool to disband')
				user_input = input('>')
				if user_input == 'pool' and user_input in location_list:
					if allegiance == 'SCOTLAND':
						return 'scottish pool'
					else:
						return 'english pool'

				else:

					try:

						return location_list[int(user_input)]

						new_bool = False

					except (ValueError,IndexError):

						return ("Invalid Input!!")


def go_home(board,noble,eng_type,scot_type):

	'''
	takes a noble from the location that they are at and then transports them
	home. also takes board object and the side that the computer is playing
	if there is more than 1 home location, it randomly picks one.
	changes allegiance based on who controls home area
	'''

	if type(noble.home_location) == int:

		
		if not board.regions[noble.home_location].blocks_present or board.regions[noble.home_location].blocks_present[0].allegiance == noble.allegiance:

			board.regions[find_location(board,noble).regionID].blocks_present.remove(noble)

			board.regions[noble.home_location].blocks_present.append(noble)

		else:

			noble.allegiance = board.regions[noble.home_location].blocks_present[0].allegiance

			print(noble.name + '\'s allegiance was changed to ' + board.regions[noble.home_location].blocks_present[0].allegiance)

			board.regions[find_location(board,noble).regionID].blocks_present.remove(noble)

			board.regions[noble.home_location].blocks_present.append(noble)


	else:

		possible_locations = []

		new_locations = []
		
		for home in noble.home_location:

			new_locations.append(home)

			if not board.regions[home].blocks_present or board.regions[home].blocks_present[0].allegiance == noble.allegiance:

				possible_locations.append(board.regions[home])

		else:

			if not possible_locations:

				if noble.allegiance == "SCOTLAND":

					noble.allegiance == "ENGLAND"

				else:

					noble.allegiance == "SCOTLAND"
				
				noble_choice = search.region_id_to_object(board, choose_location(new_locations,noble.allegiance,eng_type,scot_type,noble))
				print(noble.name + ' went home to ' + board.regions[noble_choice].name)
				add_to_location(board,noble,noble_choice)

			else:

				noble_new_home = choose_location(possible_locations,noble.allegiance,eng_type,scot_type,noble)
				
				add_to_location(board,noble,noble_new_home)

def add_to_location(board,block,location):

	'''
	takes a board, block, and region object
	removes block from its current region 
	puts it into the new location
	'''

	if location == 'scottish pool':
		board.regions[find_location(board, block).regionID].blocks_present.remove(block)

		board.scot_pool.append(block)
	elif location == 'english pool':
		board.regions[find_location(board, block).regionID].blocks_present.remove(block)
		board.eng_pool.append(block)
		print("Sent" + block.name + ' to ' + location.name)

	else:

		if find_location(board,block):

			find_location(board,block).blocks_present.remove(block)

			board.regions[location.regionID].blocks_present.append(block)

			print ("Sent " + block.name + " to " + location.name)

		else:

			if block.allegiance == 'SCOTLAND':

				board.scot_pool.remove(block)

				board.scot_roster.append(block)

			else:

				board.eng_pool.remove(block)

				board.eng_roster.append(roster)

			board.regions[location.regionID].blocks_present.append(block)	


def moray_util(board,noble):

	'''
	returns a dictionary with the utility of three choices for moray
	staying, going home, or disbanding
	takes a player object, board object, and moray's object
	'''

	util_dict = {'disband':0.001}

	stay_loc = find_location(board,noble)

	if board.regions[noble.home_location].is_friendly(noble.allegiance):

		util_dict['home'] = 0

	elif stay_loc.cathedral:

		if len(stay_loc.blocks_present) <= stay_loc.castle_points + 1:

			util_dict['stay'] = 0

	else:

		if len(stay_loc.blocks_present) <= stay_loc.castle_points:

			util_dict['stay'] = 0


	for i,border in enumerate(board.dynamic_borders[noble.home_location]):

		if border != 'X':

			if board.regions[i].is_friendly('ENGLAND'):

				if 'stay' in util_dict:

					util_dict['stay'] += 1
				
				util_dict['disband'] += 1

	for i,border in enumerate(board.dynamic_borders[stay_loc.regionID]):

		if border != 'X':

			if board.regions[i].is_friendly('ENGLAND'):

				if 'home' in util_dict:

					util_dict['home'] += 1
				
				util_dict['disband'] += 1


	moray_missing_strength = noble.attack_strength - noble.current_strength

	for health in range(moray_missing_strength):

		if 'home' in util_dict:

			util_dict['home'] += 2

	return util_dict

def edward_util(board,block,edward_prev_winter = False):

	util_dict = {'disband':0.001}

	if not edward_prev_winter:

		stay_loc = find_location(board,block)

		util_dict['stay'] = 0

	strength_missing = block.attack_strength - block.current_strength

	for health in range(strength_missing):

		util_dict['disband'] += 1

	for i,border in enumerate(board.dynamic_borders[stay_loc.regionID]):

		if border != 'X':

			if board.regions[i].is_friendly('SCOTLAND'):

				util_dict['disband'] += 1

	for support_block in stay_loc.blocks_present:

		if block.type != 'INFANTRY' or type(block) != blocks.Noble:

			if 'stay' in util_dict:

				util_dict['stay'] += 2

	return util_dict

def scot_king_util(board,block):

	'''
	returns all possible locations for scot king to move to
	as a dictionary with utilities as values and location names as keys
	'''

	util_dict = {'disband':1}

	for region in board.regions:

		if (region.is_friendly('SCOTLAND')) and region.cathedral and len(region.blocks_present) <= region.castle_points:

			util_dict[region.name] = 0

			for i,border in enumerate(board.dynamic_borders[region.regionID]):

				if border != 'X' and board.regions[i].is_friendly('SCOTLAND'):

					util_dict[region.name] += 1

	return util_dict


def disband_block_util(board,region):
	'''
	used when all important pieces have moved for winter
	checks to see if castle limits are infringed
	takes a player object,board object, and a region object
	returns a utility dictionary where more utility means higher
	chance of disbanding. also returns the number of keys that 
	need to be returned by the chancing function.
	'''



	util_dict = {}

	display_blocks = []

	if region.is_friendly('SCOTLAND'):

			if region.cathedral:

				castle_points = region.castle_points + 1

			else:

				castle_points = region.castle_points

	else:

		if find_location(board,search.block_name_to_object(board.all_blocks,'EDWARD')) == region:

			castle_points = 100

		else:

			castle_points = region.castle_points

	for region_block in region.blocks_present:

		if type(region_block) != blocks.Noble:

			display_blocks.append(region_block)

	have_to_move = len(region.blocks_present) - castle_points

	if have_to_move > 0:
	
		for block in display_blocks:

			util_dict[block.blockID] = 0

			for i in range(block.attack_strength-block.current_strength):

				util_dict[block.blockID] += 1

			if block.attack_letter == 'A':

				util_dict[block.blockID] += 1

			elif block.attack_letter == 'B':

				util_dict[block.blockID] += 2

			elif block.attack_letter == 'C':

				util_dict[block.blockID] += 3

	return util_dict,have_to_move


def choose_what_to_do_util(board,region,rp):

	'''
	if computer is scottish, adss utility to bump up a troop or add reinforcement
	takes a player object,board object, region object, and replacement points integer for that region
	returns utility dictionary
	'''

	util_dict = {'b':0.01,'r':0.01}

	if len(region.blocks_present) > rp:

		util_dict['r'] += 1

	if search.block_name_to_object(board,'WALLACE') in region.blocks_present and search.block_name_to_object(board,'WALLACE').current_strength < search.block_name_to_object(board,'WALLACE').attack_strength:

		util_dict['b'] += 1

	if search.block_name_to_object(board,'KING') in region.blocks_present and search.block_name_to_object(board,'KING').current_strength < search.block_name_to_object(board,'KING').attack_strength:

		util_dict['b'] += 1

	if search.block_name_to_object(board,'EDWARD') in region.blocks_present and search.block_name_to_object(board,'EDWARD').current_strength < search.block_name_to_object(board,'EDWARD').attack_strength:

		util_dict['b'] += 1

	return util_dict


def choose_what_to_bump_util(block_list):

	'''
	takes a list of potential blocks that can be bumped
	returns utilities for all blocks
	'''

	util_dict = {}

	for block in block_list:

		util_dict[block.name] = 0

		if type(block) == blocks.Noble:

			util_dict[block.name] += 4

		elif block.name == 'WALLACE' or block.name == 'EDWARD' or block.name == 'KING':

			util_dict[block.name] += 1

		util_dict[block.name] += (block.attack_strength-block.current_strength)

	return util_dict
			

def disband(board,block):

	'''
	takes a board object and block object
	sends the block to the board's draw pool
	'''

	board.regions[find_location(board,block).regionID].blocks_present.remove(block)


	if block.allegiance == 'SCOTLAND':
		board.scot_roster.remove(block)
		board.scot_pool.append(block)
	else:
		board.eng_roster.remove(block)
		board.eng_pool.append(block)

	print ("Disbanded " + block.name + "!")	

def initialize_winter(board,block_list,eng_type,scot_type, edward_prev_winter = [False]):

	'''
	takes a board object, list of all blocks in game, and which side the computer is playing
	moves every block to correct location -- random for computer, user input for human
	'''
	eng_nobles = []
	scot_nobles = []
	eng_king = []
	scot_king = []
	eng_edward = []

	for block in block_list:

		if block in board.eng_roster or block in board.scot_roster:

			if find_location(board,block).regionID == 22:

				disband(board,block)
			
			else:

				if type(block) == blocks.Noble:

					if block.allegiance == "ENGLAND":

						eng_nobles.append(block)

					elif block.allegiance == "SCOTLAND":

						scot_nobles.append(block)

				elif block.type == "KING":

					if block.allegiance == "ENGLAND":

						eng_king.append(block)

					if block.allegiance == "SCOTLAND":

						scot_king.append(block)

				elif block.type == "EDWARD":

					eng_edward.append(block)

	for noble in eng_nobles:
		
		go_home(board,noble,eng_type,scot_type)

		print ("Sent " + noble.name + " home!")

	for noble in scot_nobles:

		if noble.name == "MORAY":

			if scot_type == 'comp':

				moray_utilities = moray_util(board,noble)

				comp_choice_moray = weighted_prob.weighted_prob(moray_utilities)

				if comp_choice_moray == 'stay':

					print ("Moray stayed!")

				elif comp_choice_moray == 'home':

					go_home(board,noble,eng_type,scot_type)

					print ("Sent Moray Home!")	

				elif comp_choice_moray == 'disband':

					disband(board,noble)

			else:

				bool21 = True

				while bool21:

					user_decision = input("Where do you want Moray to go? 's' for stay, 'h' for home, 'd' for disband ")

					if user_decision == 's':

						if len(board.regions[find_location(board,noble).regionID].blocks_present) <= board.regions[find_location(board,noble).regionID].castle_points:

							print ("Moray stayed!")

							bool21 = False

						else:

							print ("Moray cannot stay!")

					elif user_decision == 'h':

						go_home(board,noble,eng_type,scot_type)

						print ("Sent Moray Home!")	

						bool21 = False

					elif user_decision == 'd':

						disband(board,noble)

						bool21 = False

					else:

						print ("invalid input!")	 

		else:

			go_home(board,noble,eng_type,scot_type)

			print ("Sent " + noble.name + " home!")

	if eng_edward:

		if eng_type == 'comp':

			edward_utilities = edward_util(board,eng_edward[0],edward_prev_winter[0])

			edward_choice = weighted_prob.weighted_prob(edward_utilities)

			if edward_choice == 'disband':

				disband(board,eng_edward[0])

			elif edward_choice == 'stay':

				print ("Edward I stayed!")


		else:
		
			if not edward_prev_winter[0]:
				add_to_location(board,eng_edward[0],choose_location([find_location(board,eng_edward[0]), 'english pool'],'ENGLAND',eng_type,scot_type, block))
				edward_prev_winter[0] = True
			else:
				disband(board, eng_king[0])

	if eng_king:

		disband(board,eng_king[0])

	if scot_king:

		block = scot_king[0]

		if scot_type == 'comp':

			scot_king_utilities = scot_util(board)

			scot_king_choice = weighted_prob.weighted_prob(scot_king_utilities)

			if scot_king_choice == 'disband':

				disband(board,block)

			else:

				add_to_location(board,block,board.regions[scot_king_choice])

		else:
		
			possible_locations = []

			for region in board.regions:

				if (region.is_friendly('SCOTLAND')) and region.cathedral and len(region.blocks_present) <= region.castle_points:

					region.append(possible_locations)

			place = choose_location(possible_locations,block.allegiance,eng_type,scot_type,block)

			add_to_location(board,block,place)

	for brit in board.eng_roster:

		if brit.type == 'ARCHER' or brit.type == 'KNIGHT' and find_location(board,search.block_name_to_object(board.all_blocks,'EDWARD')) != find_location(board,brit):

			disband(board,brit)

	for region in board.regions:

		computer_role = []

		if eng_type == 'comp':

			computer_role.append('ENGLAND')

		if scot_type == 'comp':

			computer_role.append('SCOTLAND')

		if region.blocks_present and region.blocks_present[0].allegiance not in computer_role:

			display_blocks = []

			if region.is_friendly('SCOTLAND'):

				if region.cathedral:

					castle_points = region.castle_points + 1

				else:

					castle_points = region.castle_points

			else:

				if find_location(board,search.block_name_to_object(board.all_blocks,'EDWARD')) == region:

					castle_points = 100

				else:

					castle_points = region.castle_points

			for region_block in region.blocks_present:

				if type(region_block) != blocks.Noble:

					display_blocks.append(region_block)

			user_inputting = True

			while user_inputting:

				if display_blocks:

					have_to_move = len(region.blocks_present) - castle_points

					if have_to_move < 0:

						have_to_move = 0

					print ("\n\nCurrent region is " + region.name + ":\n")

					for i,blck in enumerate(display_blocks):

						print (blck.name,"(" + str(i) + ")")

					print ("\n")

					user_input = input ("Choose a block to disband or move! \n You have to move at least " + str(have_to_move) + " blocks! 'Done' for done. \n>")

					try:

						if user_input.lower() == 'done':

							if have_to_move == 0:

								user_inputting = False

							else:

								print ("You are over castle limits! Continue disbanding!")

						else:

							user_block = display_blocks[int(user_input)]

							if user_block.type == "WALLACE":

								wallace_possible_locations = ['scottish pool',board.regions[18]]

								add_to_location(board,block,choose_location(wallace_possible_locations,block.allegiance,eng_type,scot_type,block))

								display_blocks.remove(user_block)

							else:

								disband(board,user_block)

								display_blocks.remove(user_block)

					except (ValueError,IndexError):

						print ("That is not a valid option!")

				else:

					print ("No blocks to move from " + region.name)

					user_inputting = False

		elif region.blocks_present and region.blocks_present[0].allegiance in computer_role:

			display_blocks = []

			for region_block in region.blocks_present:

				if type(region_block) != blocks.Noble:

					display_blocks.append(region_block)

			if display_blocks:

				disbanding_utilities,have_to_move = disband_block_util(board,region)

				computer_choices = weighted_prob.weighted_prob(disbanding_utilities,have_to_move)

				for computer_choice in computer_choices:

					computer_block = search.block_id_to_object(board.all_blocks,computer_choice)

					if computer_block.type == "WALLACE":

						wallace_possible_locations = ['scottish pool',board.regions[18]]

						add_to_location(board,computer_block,choose_location(wallace_possible_locations,block.allegiance,eng_type,scot_type,block))

					else:

						disband(board,computer_block)
		
	levy(board)

def distribute_rp(board,rp,region,eng_type,scot_type):

	'''
	takes a board object, a given rp, a region object, and the side the computer plays
	helper function for winter_builds
	assigns rp randomly based on side for computer
	asks for appropriate inputs from the user based on side 
	'''

	if scot_type == 'comp':

		if region.is_friendly('SCOTLAND'):

			points = rp

			while points > 0:

				choice_utilities = choose_what_to_do_util(board,region,rp)

				computer_choice = weighted_prob.weighted_prob(choice_utilities)

				if computer_choice == 'r':

					if len(region.blocks_present) < rp and board.scot_pool:

						valid_block = False

						while not valid_block:

							draw_block = random.choice(board.scot_pool)

							if draw_block.type == 'NORSE':

								if region.coast:

									valid_block = True

							elif draw_block.name == 'KING':

								pass

							elif draw_block.name == 'FRENCH':

								scottish_nobles = 0

								for scot in board.scot_roster:

									if type(scot) == blocks.Noble:

										scottish_nobles += 1

								if region.coast and scottish_nobles >= 8:

									valid_block = True

							else:

								valid_block = True

						draw_block.current_strength = 1 

						add_to_location(board,draw_block,region)

						points -= 1

				elif computer_choice == 'b':

					potential_blocks = []

					for block in region.blocks_present:

						if block.current_strength < block.attack_strength:

							potential_blocks.append(block)

					if potential_blocks:

						bump_block_utilities = choose_what_to_bump_util(potential_blocks)

						bump_choice = weighted_prob.weighted_prob(bump_block_utilities)

						bump_block = search.block_id_to_object(board.all_blocks,bump_choice)

						bump_block.current_strength += 1

						print ("Bumped " + bump_block.name + " up!")

						points -= 1

					elif not potential_blocks and len(region.blocks_present) >= rp:

						points = 0

				else:

					print ("Not a correct input! Please type 'r' or 'b'!")

		
		elif eng_type == 'opp':

			potential_blocks = []

			for block in region.blocks_present:

				if block.current_strength < block.attack_strength and (type(block) == blocks.Noble or block.type == 'INFANTRY'):

					potential_blocks.append(block)

			points = rp

			print (region.name + " has " + str(points))

			while points > 0 or potential_blocks:

				try:

					for index,name in enumerate(potential_blocks):

						print (str(index) + ":" + " "*5 + str(name))

					user_choice = input("Which block would you like to bump in " + region.name + "? \n Type 'done' if you are finished ")

					if user_choice.lower() == 'done':

						points = 0

					else:

						potential_blocks[int(user_choice)].current_strength += 1

						points -= 1

				except (IndexError,ValueError):

					print ("Not a valid option!")

	if eng_type == 'comp':
	
		if region.is_friendly('ENGLAND'):

			points = rp

			while points > 0 or potential_blocks:

				potential_blocks = []

				for block in region.blocks_present:

					if block.current_strength < block.attack_strength and (type(block) == blocks.Noble or block.type == 'INFANTRY'):

						potential_blocks.append(block)

				if potential_blocks:

					bump_block_utilities = choose_what_to_bump_util(potential_blocks)

					bump_choice = weighted_prob.weighted_prob(bump_block_utilities)

					bump_block = search.block_id_to_object(board.all_blocks,bump_choice)

					bump_block.current_strength += 1 

					print ("Bumped " + bump_block.name + " up!")

					points -= 1

				else:

					print (region.name + " has nothing to build!")

					points = 0

		elif scot_type == 'comp':

			points = rp

			print (region.name + " has " + str(points))

			while points > 0:

				user_choice = input("Strengthen a troop (t) or bring in reinforcements (r)? type 'd' for done ")

				if user_choice.lower() == "d":

					points = 0

				elif user_choice.lower() == "r":

					if board.scot_pool:

						if len(region.blocks_present) < rp:

							valid_block = False

							while not valid_block:

								draw_block = random.choice(board.scot_pool)

								if draw_block.type == 'NORSE':

									if region.coast:

										valid_block = True

								elif draw_block.name == 'KING':

									pass

								elif draw_block.name == 'FRENCH':

									scottish_nobles = 0

									for scot in board.scot_roster:

										if type(scot) == blocks.Noble:

											scottish_nobles += 1

									if region.coast and scottish_nobles >= 8:

										valid_block = True

								else:

									valid_block = True

							draw_block.current_strength = 1 

							board.scot_pool.remove(draw_block)

							region.blocks_present.append(draw_block)

							board.scot_roster.append(draw_block)

							print (draw_block.name + "added to reinforcements of " + region.name)

							points -= 1

						else:

							print ("Can't put reinforcements here!")

					else:

						print ("There are no blocks in the scottish pool!")

				elif user_choice.lower() == "t":

					potential_blocks = []

					for block in region.blocks_present:

						if block.current_strength < block.attack_strength:

							potential_blocks.append(block)

					if potential_blocks:

						try:

							for index,name in enumerate(potential_blocks):

								print (str(index) + ":" + " "*5 + str(name))

							user_choice2 = input("Which block would you like to bump in " + region.name + "? ")

							potential_blocks[int(user_choice2)].current_strength += 1

							points -= 1

						except (IndexError,ValueError):

							print ("Not a valid option!")

					else:

						print ("All blocks at full strength.")

				else:

					print ("Please type a valid choice!")



def winter_builds(board,eng_type,scot_type):

	'''
	takes a board object and the side the computer is playing
	assigns rp to each region and then uses the rp
	computer rp is assigned randomly
	human rp is inputed
	'''

	scottish_rp = 0
	english_rp = 0

	for region in board.regions:

		if len(region.blocks_present) > 0 and region.is_friendly('SCOTLAND'):

			if region.name == 'SELKIRK-FOREST':

				scottish_rp = 2

			elif region.cathedral:

				scottish_rp = region.castle_points + 1

			else:

				scottish_rp = region.castle_points

			distribute_rp(board,scottish_rp,region,eng_type,scot_type)

		elif len(region.blocks_present) > 0 and region.is_friendly('ENGLAND'):

			english_rp = region.castle_points

			distribute_rp(board,english_rp,region,eng_type,scot_type)


def levy(board, num_people = None):
	"""
	send 'start' if start
	otherwise it does levy
	"""
	if num_people == 'start':
		num_people = 4
	else:
		num_people = math.ceil(len(board.eng_pool) / 2)

	for i in range(num_people):
		block_to_get_put_in_num = random.randint(0, len(board.eng_pool) - 1)
		block_to_get_put_in = board.eng_pool[block_to_get_put_in_num]
		board.eng_pool.remove(block_to_get_put_in)
		board.eng_roster.append(block_to_get_put_in)
		board.regions[22].blocks_present.append(block_to_get_put_in)
		print(block_to_get_put_in.name , ' has moved to levy')





