import math
import random
import search
import blocks
import board

def find_location(board, blok):
	for region in board.regions:
		for bllock in region.blocks_present:

			if region.name == "FIFE":

				print (blok.name)

				print (bllock.name)
			
			if bllock.name == blok.name:
				return region
	return False

def choose_location(location_list,allegiance,computer_role, block):

	'''
	takes a list of locations and a block allegiance
	returns a random location from list or a user decision
	can be updated to do a smarter decision
	'''

	if allegiance == computer_role:

		index = random.randint(0,len(location_list)-1)

		return location_list[index]

	else:

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

def go_home(board,noble,computer_role):

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

				find_location(board, noble).blocks_present.remove(noble)

				if noble.allegiance == "SCOTLAND":

					noble.allegiance == "ENGLAND"

				else:

					noble.allegiance == "SCOTLAND"
				
				noble_choice = choose_location(new_locations,noble.allegiance,computer_role,block)
				print(noble.name + ' went home to ' + board.regions[noble_choice].name)
				add_to_location(board,noble,noble_choice)

			else:

				noble_new_home = choose_location(possible_locations,noble.allegiance,computer_role,noble)
				
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

			print (block.name)

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
		
		go_home(board,noble,computer_role)

		print ("Sent " + noble.name + " home!")

	for noble in scot_nobles:

		if noble.name == "MORAY":

			if computer_role == 'SCOTLAND':

				int1 = random.randint(0,1)

				if int1 == 1:

					if len(board.regions[find_location(board,noble).regionID].blocks_present) <= board.regions[find_location(board,noble).regionID].castle_points:

						print ("Moray stayed!")

					else:

						go_home(board,noble,computer_role)

						print ("Sent Moray Home!")	

				else:

					go_home(board,noble,computer_role)

					print ("Sent Moray Home!")	

			else:

				bool21 = True

				while bool21:

					user_decision = input("Where do you want Moray to go? 's' for stay, 'h' for home ")

					if user_decision == 's':

						if len(board.regions[find_location(board,noble).regionID].blocks_present) <= board.regions[find_location(board,noble).regionID].castle_points:

							print ("Moray stayed!")

							bool21 = False

						else:

							print ("Moray cannot stay!")

					elif user_decision == 'h':

						go_home(board,noble,computer_role)

						print ("Sent Moray Home!")	

						bool21 = False

					else:

						print ("invalid input!")	 

		else:

			go_home(board,noble,computer_role)

			print ("Sent " + noble.name + " home!")

	if eng_edward:

		if not edward_prev_winter[0]:
			add_to_location(board,eng_edward[0],choose_location([find_location(board,block), 'english pool'],'ENGLAND',computer_role, block))
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

		place = choose_location(possible_locations,block.allegiance,computer_role, block)

		add_to_location(board,block,place)

	for brit in board.eng_roster:

		if brit.type == 'ARCHER' or brit.type == 'KNIGHT':

			disband(board,brit)

	for region in board.regions:

		if region.blocks_present and region.blocks_present[0].allegiance != computer_role:

			display_blocks = []

			if region.blocks_present[0].allegiance == 'SCOTLAND':

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

								add_to_location(board,block,choose_location(wallace_possible_locations,block.allegiance,computer_role,block))

								display_blocks.remove(user_block)

							else:

								disband(board,user_block)

								display_blocks.remove(user_block)

					except (ValueError,IndexError):

						print ("That is not a valid option!")

				else:

					print ("No blocks to move from " + region.name)

					user_inputting = False

		elif region.blocks_present and region.blocks_present[0].allegiance == computer_role:

			display_blocks = []

			if region.blocks_present[0].allegiance == 'SCOTLAND':

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

			block_valid = True

			while block_valid:

				have_to_move = len(region.blocks_present) - castle_points

				if have_to_move > 0:

					computer_block = random.choice(display_blocks)

					if computer_block.type == "WALLACE":

						wallace_possible_locations = ['scottish pool',board.regions[18]]

						add_to_location(board,computer_block,choose_location(wallace_possible_locations,block.allegiance,computer_role,block))

						display_blocks.remove(computer_block)

					else:

						if computer_block.allegiance == 'ENGLAND':

							pool = 'english pool'

						else:

							pool = 'scottish pool'

						disband(board,computer_block)

						display_blocks.remove(computer_block)

				else:

					block_valid = False

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

	else:

		
		if region.blocks_present[0].allegiance == 'ENGLAND':
			
			potential_blocks = []

			points = rp

			while points > 0 or potential_blocks:

				for block in region.blocks_present:

					if block.current_strength < block.attack_strength and (type(block) == blocks.Noble or block.type == 'INFANTRY'):

						potential_blocks.append(block)

				if potential_blocks:

					computer_choice = random.choice(potential_blocks)

					computer_choice.current_strength += 1 

					print ("Bumped " + computer_choice.name + " up!")

					points -= 1

				else:

					print (region.name + " has nothing to build!")

					points = 0

		else:

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

		if len(region.blocks_present) > 0 and region.blocks_present[0].allegiance == 'SCOTLAND':

			if region.name == 'SELKIRK-FOREST':

				scottish_rp = 2

			elif region.cathedral:

				scottish_rp = region.castle_points + 1

			else:

				scottish_rp = region.castle_points

			distribute_rp(board,scottish_rp,region,computer_role)

		elif len(region.blocks_present) > 0 and region.blocks_present[0].allegiance == 'ENGLAND':

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
		board.eng_roster.append(block_to_get_put_in)
		board.regions[22].blocks_present.append(block_to_get_put_in)
		print(block_to_get_put_in.name , ' has moved to levy')






