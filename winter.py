import math
import random
import search



def go_home(board,noble,computer_role):

	'''
	takes a noble from the location that they are at and then transports them
	home. also takes board object and the side that the computer is playing
	if there is more than 1 home location, it randomly picks one.
	changes allegiance based on who controls home area
	'''

	if type(noble.home_location) == int:

		
		if not board.regions[noble.home_location].blocks_present or board.regions[noble.home_location].blocks_present[0].allegiance == noble.allegiance:

			board.regions[find_location(board,noble.blockID).regionID].blocks_present.remove(noble)

			board.regions[noble.home_location].blocks_present.append(noble)

		else:

			noble.allegiance = board_regions[noble.home_location].blocks_present[0].allegiance

			board.regions[find_location(board,noble.blockID).regionID].blocks_present.remove(noble)

			board.regions[noble.home_location].blocks_present.append(noble)


	else:

		possible_locations = []

		new_locations = []
		
		for home in noble.home_location:

			new_locations.append(home)

			if not board.regions[home].blocks_present or board.regions[home].blocks_present[0].allegiance == noble.allegiance:

				possible_locations.append(home)

		else:

			if not possible_locations:

				board.regions[home].blocks_present.remove(noble)

				if noble.allegiance == "SCOTLAND":

					noble.allegiance == "ENGLAND"

				else:

					noble.allegiance == "SCOTLAND"

				add_to_location(board,noble,choose_location(new_locations,noble.allegiance,computer_role))

			else:

				board.regions[find_location(board,noble.blockID).regionID].blocks_present.remove(noble)

				board.regions[random.choice(possible_locations)].blocks_present.append(noble)


def add_to_location(board,block,location):

	'''
	takes a board, block, and region object
	removes block from its current region 
	puts it into the new location
	'''

	if location == 'scottish pool':
		board.regions[find_location(board, block.blockID).regionID].blocks_present.remove(block)

		board.scot_pool.append(block)
	elif location == 'english pool':
		board.regions[find_location(board, block.blockID).regionID].blocks_present.remove(block)
		board.eng_pool.append(block)
		print("Sent" + block.name + ' to ' + location.name)

	else:

		board.regions[find_location(board,block.blockID).regionID].blocks_present.remove(block)

		board.regions[location.regionID].blocks_present.append(block)

		print ("Sent " + block.name + " to " + location.name)	

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

			print("Where would you like " + block.name + " to go? ")
			print('Type pool to disband')
			user_input = input('>')
			if user_input == 'pool' and user_input in location_list:
				if allegiance == 'SCOTLAND':
					return 'scottish pool'
				else:
					return 'english pool'
			try:
				region_choice = board.regionID_dict[user_input.upper()]

				if int(region_choice) in location_list:

					new_bool = False

					return region_choice


				else:

					print ("Not valid!")

			except ValueError:
				print('Not valid')

def disband(board,block):

	'''
	takes a board object and block object
	sends the block to the board's draw pool
	'''

	board.regions[find_location(board,block.blockID).regionID].blocks_present.remove(block)


	if block.allegiance == 'SCOTLAND':
		board.scot_pool.blocks_present.append(block)
	else:
		board.eng_pool.blocks_present.append(block)

	print ("Disbanded " + block.name + "!")	

def initialize_winter(board,block_list,computer_role, edward_prev_winter = [False]):

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

			if find_location(board,block.blockID).regionID == 22:

				disband(board,block)
			
			else:

				if type(block) == blocks.Noble():

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
		
		go_home(board,noble,computer_role)

		print ("Sent " + noble.name + " home!")

	for noble in scot_nobles:

		if block.name == "MORAY":

			int1 = random.randint(0,1)

			if int1 == 1:

				if len(board.regions[find_location(board,block.blockID).regionID].blocks_present) <= board.regions[find_location(board,block.blockID).regionID].castle_points:

					print ("Moray stayed!")

				else:

					go_home(board,block)

					print ("Sent Moray Home!")	

			else:

				go_home(board,block)

				print ("Sent Moray Home!")			 

		else:

			go_home(board,noble,computer_role)

			print ("Sent " + noble.name + " home!")

	if eng_edward:

		if not edward_prev_winter[0]:
			add_to_location(board,eng_edward[0],choose_location([find_location(board,block.blockID), 'english pool'],'ENGLAND',computer_role))
			edward_prev_winter[0] = True
		else:
			disband(board, eng_king[0])

	if eng_king:

		disband(board,eng_king[0])

	if scot_king:

		possible_locations = []

		block = scot_king[0]

		for region in board.regions:

			if (region.blocks_present[0].allegiance == "SCOTLAND") and region.cathedral and len(region.blocks_present) <= region.castle_points:

				region.append(possible_locations)

		place = choose_location(possible_locations,block.allegiance,computer_role)

		add_to_location(board,block,place)

	for region in board.regions:

		for block in region.blocks_present:

			if block.type == "WALLACE":

				wallace_possible_locations = ['scottish pool']

				if find_location(board,block.blockID).cathedral:

					castle_points = find_location(board,block.blockID).castle_points + 1

				if len(find_location(board,block.blockID).blocks_present) >= castle_points:

					wallace_possible_locations.append(find_location(board,block.blockID))

				if not board.regions[18].blocks_present or board.regions[18].blocks_present[0].allegiance == block.allegiance:

					wallace_possible_locations.append(board.regions[18])

				add_to_location(board,block,choose_location(wallace_possible_locations,block.allegiance,computer_role))

			elif block.type == "INFANTRY":

				if find_location(board,27) == find_location(board,block.blockID):

					castle_points = 100

				elif block.allegiance == "SCOTLAND" and find_location(board,block.blockID).cathedral:

					castle_points = find_location(board,block.blockID).castle_points + 1

				else:

					castle_points = find_location(board,block.blockID).castle_points + 1

				if len(find_location(board,block.blockID).blocks_present) > castle_points:

					if block.allegiance == "SCOTLAND":

						pool = 'scottish pool'

					else:

						pool = 'english pool'

					add_to_location(board,block,choose_location([pool,find_location(board,block.blockID)],block.allegiance,computer_role))

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

						if block.allegiance == "SCOTLAND":

							pool = 'scottish pool'

						else:

							pool = 'english pool'

							add_to_location(board,block,choose_location([pool,find_location(board,block.blockID)],block.allegiance,computer_role))

					else:

						disband(board,block)


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

						print ("Bumped " + bump_block.name + " up!")

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

					user_choice = input("Which block would you like to bump in " + region.name + "? \n Type 'done' if you are finished ")

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

				print ("Bumped " + computer_choice.name + " up!")

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

							user_choice2 = input("Which block would you like to bump in " + region.name + "? ")

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
		block_to_get_put_in_num = random.randint(0, len(board.eng_pool) - 1)
		block_to_get_put_in = board.eng_pool[block_to_get_put_in_num]
		board.eng_pool.remove(block_to_get_put_in)
		board.regions[22].blocks_present.append(block_to_get_put_in)
		print(block_to_get_put_in.name , ' has moved to levy')






