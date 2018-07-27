import board
import blocks
import random

def go_home(board,noble):

	homeless_nobles = []

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

	return homeless_nobles


def add_to_location(board,block,location):

	'''
	takes a board, block, and region object
	removes block from its current region 
	puts it into the new location
	'''

	board.regions[find_location(board,block.blockID).regionID].blocks_present.pop(block)

	board.regions[location.regionID].blocks_present.append(block)	

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

	board.regions[23].blocks_present.append(block)	

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

						if int1 = 1:

							if len(board.regions[find_location(board,block.blockID).regionID].blocks_present) <= board.regions[find_location(board,block.blockID).regionID].castle_points:

								pass

							else:

								go_home(board,block)	

						else:

							go_home(board,block)			 

					else:

						go_home(board,noble)

				elif block.type_men == "KING":

					if block.allegiance == "SCOTLAND":

						possible_locations = []

						for region in board.regions:

							if (not region.blocks_present or region.blocks_present[0].allegiance == "SCOTLAND") and region.cathedral and len(region.blocks_present) <= region.castle_points:

								region.append(possible_locations)

						add_to_location(board,block,choose_location(possible_locations,block.allegiance,computer_role))

					elif block.allegiance == "ENGLAND":

						disband(board,block)

				elif block.type_men == "EDWARD":

					add_to_location(board,block,choose_location([find_location(board,block.blockID), board.regions[23]]))

				
				elif block.type_men == "WALLACE":

					wallace_possible_locations = [board.regions[23]]

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

def distribute_rp(board,rp,region,computer_role):

	if computer_role == "SCOTLAND":

		for i in range(rp):

			computer_choice = random.randint(2)

			if computer_choice == 0:

				if len(region.blocks_present) < rp:

					add_to_location(board,random.choice(board.regions[23].blocks_present),region)

			elif computer_choice == 1:

				potential_blocks = []

				for block in region.blocks_present:

					if block.current_strength < block.attack_strength:

						potential_blocks.append(block)

				if potential_blocks:

					bump_block = random.choice(potential_blocks)

					bump_block.current_strength += 1

		


def winter_builds(board,computer_role)

		scottish_rp = 0
		english_rp = 0

		for region in board.regions:

			if region.blocks_present[0].allegiance == 'SCOTLAND':

				if region.cathedral:

					scottish_rp = region.castle_points + 1

				else:

					scottish_rp = region.castle_points

			elif region.blocks_present[0].allegiance == 'ENGLAND':

				english_rp = region.castle_points



#threat to wallace


