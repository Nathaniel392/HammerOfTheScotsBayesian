import math
import random
def go_home(board,noble):

	'''
	takes a noble from the location that they are at and then transports them
	home. if there is more than 1 home location, it randomly picks one.
	changes allegiance based on who controls home area
	'''

	if type(noble.home_location) == int:

		
		if not board.regions[noble.home_location].blocks_present or board.regions[noble.home_location].blocks_present[0].allegiance == noble.allegiance:

			board.regions[find_location(board,noble.blockID).regionID].blocks_present.pop(noble)

			board.regions[noble.home_location].blocks_present.append(noble)

		else:

			noble.allegiance = board_regions[noble.home_location].blocks_present[0].allegiance

			board.regions[find_location(board,noble.blockID).regionID].blocks_present.pop(noble)

			board.regions[noble.home_location].blocks_present.append(noble)


	else:

		possible_locations = []
		
		for home in noble.home_location:

			if not board.regions[home].blocks_present or board.regions[home].blocks_present[0].allegiance == noble.allegiance:

				possible_locations.append(home)

		else:

			if not possible_locations:

				board.regions[home].blocks_present.pop(noble)

				homeless_nobles.append(noble)

				noble.allegiance = board.regions[find_location(board,noble.blockID).regionID].blocks_present[0].allegiance

			else:

				board.regions[find_location(board,noble.blockID).regionID].blocks_present.pop(noble)

				board.regions[random.choice(possible_locations)].blocks_present.append(noble)


def add_to_location(board,block,location):

	'''
	takes a board, block, and region object
	removes block from its current region 
	puts it into the new location
	'''

	board.regions[find_location(board,block.blockID).regionID].blocks_present.pop(block)

	board.regions[location.regionID].blocks_present.append(block)

	print ("Sent " + str(block) + " to " + str(location))	

def choose_location(location_list,allegiance,computer_role):

	'''
	takes a list of locations and a block allegiance
	returns a random location from list or a user decision
	can be updated to do a smarter decision
	'''

	if allegiance == computer_role:

		index = random.randint(len(location_list))

		return location_list[index]

	else:

		new_bool = True

		while new_bool:

			user_input = input("Where would you like " + str(block) + " to go? ")

			region_choice = board.regionID_dict[user_input.upper()]

			if int(region_choice) in location_list:

				new_bool = False

				return region_choice

			else:

				print ("Not valid!")

def disband(board,block):

	'''
	takes a board object and block object
	sends the block to the board's draw pool
	'''

	board.regions[find_location(board,block.blockID).regionID].blocks_present.pop(block)

	board.scot_pool.blocks_present.append(block)

	print ("Disbanded " + str(block) + "!")	

def initialize_winter(board,block_list,computer_role):

	'''
	takes a board object, list of all blocks in game, and which side the computer is playing
	moves every block to correct location -- random for computer, user input for human
	'''

	for block in block_list:

		if block in board.english_roster or block in board.scot_roster:

			if find_location(board,block.blockID).regionID == 22:

				disband(board,block)
			
			else:

				if type(block) == blocks.Noble():

					if block.name == "MORAY":

						int1 = random.randint(1)

						if int1 == 1:

							if len(board.regions[find_location(board,block.blockID).regionID].blocks_present) <= board.regions[find_location(board,block.blockID).regionID].castle_points:

								pass

								print ("Moray stayed!")

							else:

								go_home(board,block)

								print ("Sent Moray Home!")	

						else:

							go_home(board,block)

							print ("Sent Moray Home!")			 

					else:

						go_home(board,noble)

						print ("Sent " + str(noble) + " home!")

				elif block.type_men == "KING":

					if block.allegiance == "SCOTLAND":

						possible_locations = []

						for region in board.regions:

							if (not region.blocks_present or region.blocks_present[0].allegiance == "SCOTLAND") and region.cathedral and len(region.blocks_present) <= region.castle_points:

								region.append(possible_locations)

						place = choose_location(possible_locations,block.allegiance,computer_role)

						add_to_location(board,block,place)

					elif block.allegiance == "ENGLAND":

						disband(board,block)

				elif block.type_men == "EDWARD":

					add_to_location(board,block,choose_location([find_location(board,block.blockID), board.scot_pool]))

				
				elif block.type_men == "WALLACE":

					wallace_possible_locations = [board.scot_pool]

					if find_location(board,block.blockID).cathedral:

						castle_points = find_location(board,block.blockID).castle_points + 1

					if len(find_location(board,block.blockID).blocks_present) >= castle_points:

						wallace_possible_locations.append(find_location(board,block.blockID))

					if not board.regions[18].blocks_present or board.regions[18].blocks_present[0].allegiance == block.allegiance:

						wallace_possible_locations.append(board.regions[18])

					add_to_location(board,block,choose_location(wallace_possible_locations,block.allegiance,computer_role))

				elif block.type_men == "INFANTRY":

					if find_location(board,27) == find_location(board,block.blockID):

						castle_points = 100

					elif block.allegiance == "SCOTLAND" and find_location(board,block.blockID).cathedral:

						castle_points = find_location(board,block.blockID).castle_points + 1

					else:

						castle_points = find_location(board,block.blockID).castle_points + 1

					if len(find_location(board,block.blockID).blocks_present) > castle_points:

						add_to_location(board,block,choose_location([23,find_location(board,block.blockID)],block.allegiance,computer_role))

					else:

						disband(board,block) 

				else:

					if find_location(board,27) == find_location(board,block.blockID):

						castle_points = 100

					elif block.allegiance == "SCOTLAND" and find_location(board,block.blockID).cathedral:

						castle_points = find_location(board,block.blockID).castle_points + 1

					else:

						castle_points = find_location(board,block.blockID).castle_points + 1

					if block.allegiance == "ENGLAND":

						if castle_points < 100:

							disband(block,board)

					else:

						if len(find_location(board,block.blockID).blocks_present) > castle_points:

							add_to_location(board,block,choose_location([23,find_location(board,block.blockID)],block.allegiance,computer_role))

						else:

							disband(board,block)

	for block in block_list:

		if find_location(board,block.blockID) == None:

			if block.allegiance == computer_role:

				go_home(block)

			else:

				new_bool = True

				while new_bool:

					user_input = input("Where would you like " + str(block) + " to go? ")

					region_choice = board.regionID_dict[user_input.upper()]

					if int(region_choice) in block.home_location:

						new_bool = False

						add_to_location(board,block,region_choice)

					else:

						print ("Not valid!")

	levy(board)

def distribute_rp(board,rp,region,computer_role):

	'''
	takes a board object, a given rp, a region object, and the side the computer plays
	helper function for winter_builds
	assigns rp randomly based on side for computer
	asks for appropriate inputs from the user based on side 
	'''

	if computer_role == "SCOTLAND":

		if region.blocks_present[0].allegiance == "SCOTLAND":

			points = rp

			while points > 0:

				computer_choice = random.randint(1)

				if computer_choice == 0:

					if len(region.blocks_present) < rp:

						draw_block = random.choice(board.scot_pool.blocks_present)

						draw_block.current_strength = 1 

						add_to_location(board,draw_block,region)

						points -= 1

				elif computer_choice == 1:

					potential_blocks = []

					for block in region.blocks_present:

						if block.current_strength < block.attack_strength:

							potential_blocks.append(block)

					if potential_blocks:

						bump_block = random.choice(potential_blocks)

						bump_block.current_strength += 1

						print ("Bumped " + str(bump_block) + " up!")

						points -= 1

					elif not potential_blocks and len(region.blocks_present) >= rp:

						points = 0

		else:

			potential_blocks = []

			for block in region.blocks_present:

				if block.current_strength < block.attack_strength:

					potential_blocks.append(block)

			points = rp

			while points > 0 or potential_blocks:

				try:

					for index,name in enumerate(potential_blocks):

						print (str(index) + ":" + " "*5 + str(name))

					user_choice = input("Which block would you like to bump in " + str(region) + "? \n Type 'done' if you are finished ")

					if user_choice.lower() == 'done':

						points = 0

					else:

						potential_blocks[int(user_choice)].current_strength += 1

						points -= 1

				except (IndexError,ValueError):

					print ("Not a valid option!")

	else:

		if computer_role == "ENGLAND":

			potential_blocks = []

			points = rp

			while points > 0 or potential_blocks:

				for block in region.blocks_present:

					if block.current_strength < block.attack_strength:

						potential_blocks.append(block)

				computer_choice = random.choice(potential_blocks)

				computer_choice.current_strength += 1 

				print ("Bumped " + str(computer_choice) + " up!")

				points -= 1

		else:

			points = rp

			while points > 0:

				user_choice = input("Strengthen a troop (t) or bring in reinforcements (r)? type 'd' for done ")

				if user_choice.lower() == "d":

					points = 0

				elif user_choice.lower() == "r":

					if len(region.blocks_present) < rp:

						draw_block = random.choice(board.scot_pool.blocks_present)

						draw_block.current_strength = 1 

						add_to_location(board,draw_block,region)

						points -= 1

					else:

						print ("Can't put reinforcements here!")

				elif user_choice.lower() == "t":

					potential_blocks = []

					for block in region.blocks_present:

						if block.current_strength < block.attack_strength:

							potential_blocks.append(block)

					if potential_blocks:

						try:

							for index,name in enumerate(potential_blocks):

								print (str(index) + ":" + " "*5 + str(name))

							user_choice2 = input("Which block would you like to bump in " + str(region) + "? ")

							potential_blocks[int(user_choice2)].current_strength += 1

							points -= 1

						except (IndexError,ValueError):

							print ("Not a valid option!")

				else:

					print ("Please type a valid choice!")



def winter_builds(board,computer_role):

	'''
	takes a board object and the side the computer is playing
	assigns rp to each region and then uses the rp
	computer rp is assigned randomly
	human rp is inputed
	'''

	scottish_rp = 0
	english_rp = 0

	for region in board.regions:

		if region.blocks_present[0].allegiance == 'SCOTLAND':

			if region.cathedral:

				scottish_rp = region.castle_points + 1

			else:

				scottish_rp = region.castle_points

			distribute_rp(board,scottish_rp,region,computer_role)

		elif region.blocks_present[0].allegiance == 'ENGLAND':

			english_rp = region.castle_points

			distribute_rp(board,english_rp,region,computer_role)


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
		block_to_get_put_in = random.randint(0, len(board.eng_pool) - 1)
		board.regions[22].add_block(board.eng_pool.pop(block_to_get_put_in))
		print(block_to_get_put_in.name , ' has moved to levy')






