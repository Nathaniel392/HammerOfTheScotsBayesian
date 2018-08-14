import blocks
import combat
import random
def find_location(board, blok):
	for region in board.regions:
		for bllock in region.blocks_present:
			if bllock.name == blok.name:
				return region
	raise Exception('cannot find block')

def can_king(current_board):
	"""
	returns if the scots can king
	given that they have an event card
	returns map of booleans balliol, bruce comyn
	"""

	
	wallace_found = False
	
	bruce_found = False
	comyn_found = False

	wallace_found = False

	can_crown_bruce = False
	can_crown_comyn = False
	can_crown_balliol = False

	for block in current_board.scot_roster + current_board.scot_pool:
		if type(block) == blocks.Noble and block in current_board.scot_roster:
			
			if block.name == 'BRUCE':
				bruce_found = True
				bruce_location = find_location(current_board, block)

			elif block.name == 'COMYN':	
				comyn_found = True
				comyn_location = find_location(current_board, block)
		
		elif block.name == 'WALLACE' and not block.is_dead():
			wallace_found = True
		elif block.name == 'FRENCH' and block in current_board.scot_roster:
			can_crown_balliol = True

		#king has already been crowned
		try:
			if block.name == 'KING' and block.kinged_before:
				return {'BALLIOL': False, 'BRUCE': False, 'COMYN': False}
		except AttributeError:
			if block.name != 'KING':
				raise Exception("something wrong with the block's name with the king")
			

	if not wallace_found: 
		if bruce_found and bruce_location.name == 'FIFE':
			can_crown_bruce = True
		if comyn_found and comyn_location.name == 'FIFE':
			can_crown_comyn = True


	return {'BALLIOL': can_crown_balliol, 'BRUCE': can_crown_bruce, 'COMYN': can_crown_comyn}



def defect_nobles(current_board, loyalty_to_defect):
	"""
	defeccts nobles
	"""


	for region in current_board.regions:
		for block in region.blocks_present:
			if type(block) == blocks.Noble and block.loyalty == loyalty_to_defect and block.allegiance == 'SCOTLAND':
				if block.name != 'MORAY':
					block.change_allegiance()

			
			
				
		if region.is_contested():
			for block in region.blocks_present:
				if block.allegiance == 'ENGLAND':
					region.combat_dict['Attacking'].append(block)
				else:
					region.combat_dict['Defending'].append(block)

def fight(current_board, eng_type, scot_type):
	"""
	does all the fights in contested regions
	computer_role is scottish or english
	"""



	contested_regions = list()
	for region in current_board.regions:
		if region.is_contested():
			contested_regions.append(region)
	
	first_played = current_board.who_goes_first
	
	if first_played == 'ENGLAND':
		order_decider_type = eng_type
	elif first_played == 'SCOTLAND':
		order_decider_type = scot_type


			
	if order_decider_type == 'comp':

		while len(contested_regions) > 0:
			

			try:
				region_index_to_fight = random.randint(0, len(contested_regions) - 1)
				'''
				if current_board.who_goes_first == 'SCOTLAND':

					region_index_to_fight = random.randint(0, len(contested_regions) - 1)
				else:
					print('contested regions:')
					for i, region in enumerate(contested_regions):
						print(region.name + '[' + str(i) + ']', end = '\t')

					bad_input = True
					while bad_input:
						try:
							region_index_to_fight = int(input('Which region do you want to fight now (type index)'))
						except ValueError:
							print('type a number')
							continue
						if region_index_to_fight not in range(len(contested_regions)):
							print('type a valid index')
						else:
							bad_input = False
				'''
			except AttributeError:
				raise Exception('error in cardplay not assigning who_goes_first to board')



			attack = contested_regions[region_index_to_fight].combat_dict['Attacking']
			defense = contested_regions[region_index_to_fight].combat_dict['Defending']

			if type(attack) != list or type(defense) != list:
				raise Exception('attack and defense are not lists')
			combat.battle(attack, defense, list(), list(), current_board, computer_role)

			contested_regions = list()
			for region in current_board.regions:
				if region.is_contested():
					contested_regions.append(region)
	else:	#Human picks which regions to contest first
		
		while len(contested_regions) > 0:
			
			try:
				
				if current_board.who_goes_first == 'SCOTLAND':
					
					print('contested regions:')
					for i, region in enumerate(contested_regions):
						print(region.name + '[' + str(i) + ']', end = '\t')

					bad_input = True
					while bad_input:
						try:
							region_index_to_fight = int(input('Which region do you want to fight now (type index)'))
						except ValueError:
							print('type a number')
							continue
						if region_index_to_fight not in range(len(contested_regions)):
							print('type a valid index')
						else:
							bad_input = False
				else:
					region_index_to_fight = random.randint(0, len(contested_regions) - 1)
			except AttributeError:
				raise Exception('error in cardplay not assigning who_goes_first to board')

					
				
				
			attack = contested_regions[region_index_to_fight].combat_dict['Attacking']
			defense = contested_regions[region_index_to_fight].combat_dict['Defending']

			if type(attack) != list or type(defense) != list:
				raise Exception('attack and defense are not lists')
			combat.battle(attack, defense, list(), list(), current_board, computer_role)

			contested_regions = list()
			for region in current_board.regions:
				if region.is_contested():
					contested_regions.append(region)

def make_king(current_board, type_of_king):
	"""
	puts the king on the board
	"""
	
	for region in current_board.regions:
		for block in region.blocks_present:
			if block.name == 'FRENCH':
				french_location = region


	if type_of_king == 'BALLIOL':
		kinging_location = french_location
		for i, block in enumerate(current_board.scot_pool):
			if block.name == 'KING':
				king = current_board.scot_pool.pop(i)
				break
		current_board.scot_roster.append(king)
		current_board.add_to_region(king, kinging_location.regionID)
		print(king.name + ' is now king of scotland')
		king.kinged_before = True
	elif type_of_king == 'BRUCE' or type_of_king == 'COMYN':
		kinging_location_id = 11
		for i, block in enumerate(current_board.scot_pool):
			if block.name == 'KING':
				king = current_board.scot_pool.pop(i)
				break
		current_board.scot_roster.append(king)
		current_board.add_to_region(king, kinging_location_id)
		print(king.name + ' is now king of scotland')
		king.kinged_before = True


def run_king(current_board, eng_type, scot_type):
	"""
	runs through input
	returns False if don't want to king
	else run through program and return True
	"""


	
	can_king2 = False
	my_dict = can_king(current_board)

	
	for key in my_dict:
		if my_dict[key]:
			can_king2 = True
			break
	if not can_king2:
		return False

	possible_kings = list()
	for key in my_dict:
		if my_dict[key]:
			possible_kings.append(key)


	if scot_type == 'opp':
		bad_input = True
		while bad_input:
			want_to_king = input('Would you like to make a king (y) or (n): ')
			if want_to_king == 'n':
				return False
			elif want_to_king != 'y':
				print('type y or n')
				
			else:
				bad_input = False
		print('which king? (type name)')
		for king in possible_kings:
			print(king, end = '; ')

		

		good_input = False
		while not good_input:
			type_of_king = input('>').upper()
			if type_of_king != 'BALLIOL' and type_of_king != 'BRUCE' and type_of_king != 'COMYN':
				print('type BALLIOL or BRUCE or COMYN')
				
			elif not my_dict[type_of_king]:
				print('you cannot crown that king')

			else:
				good_input = True
	else:
		want_to_king = True
		possible_kings = list()
		if want_to_king:
			print('computer will king')
			for key in my_dict:
				if my_dict[key]:
					possible_kings.append(key)
		type_of_king = random.choice(possible_kings)



	if type_of_king == 'BALLIOL' or type_of_king == 'COMYN':
		loyalty_to_defect = 'BRUCE'
	elif type_of_king == 'BRUCE':
		loyalty_to_defect = 'COMYN'



	make_king(current_board, type_of_king)

	defect_nobles(current_board, loyalty_to_defect)
	fight(current_board, eng_type, scot_type)





	return True












