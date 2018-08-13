import dice
import random
import blocks
import initialize_blocks
import copy
import update_roster
import simulations
import search
import regroup_util
import retreat
import exceptions
import weighted_prob

def find_location(board, blok):
	'''
	This function takes a board object and the name of a block
	and returns a region object where the block is
	'''

	
	for i,region in enumerate(board.regions):
		for bllock in region.blocks_present:
			
			if bllock.name == blok.name:
				return board.regions[i]
	
	return False
	#print('CANNOT FIND BLOCK WITH BLOCK NAME', blok.name)
	#raise Exception('cannot find block')

def organize(blocks):
	'''
	Separates list of blocks into a, b, and c
	blocks:  List of blocks
	Returns:  Dictionary of a-list, b-list, and c-list
	'''
	ordered = {'A':[], 'B':[], 'C':[]}

	for block in blocks:
		if block.attack_letter == 'A':
			ordered['A'].append(block)
		elif block.attack_letter == 'B':
			ordered['B'].append(block)
		elif block.attack_letter == 'C':
			ordered['C'].append(block)

	return ordered
def find_max_strength(block_lst):
	"""
	finds max strength
	returns list blocks with max strength
	"""
	max_strength = 0
	not_found = True
	while(not_found):
		for block in block_lst:
			not_found = False
			if block.current_strength > max_strength:
				max_strength = block.current_strength
				not_found = True
	strong_blocks = list()
	for block in block_lst:
		if block.current_strength == max_strength:
			strong_blocks.append(block)
	return strong_blocks


def attack_block(attack_block_block, defending_blocks, eng_type, scot_type):
	"""
	attacks blocks
	uses random in case where everyone same health
	attack_block_block is the block attacking
	defending_blocks is the list of all defending blocks to be attacked
	"""


	attacking_allegiance = attack_block_block.allegiance
	
	if attacking_allegiance == 'ENGLAND':
		attacker_type = eng_type
		defender_type = scot_type
	elif attacking_allegiance == 'SCOTLAND':
		attacker_type = scot_type
		defender_type = eng_type
	
	if defending_blocks == []:
		return False
	dice_lst = dice.roll(attack_block_block.current_strength)
	print(attack_block_block.name, ' rolled ' , dice_lst)



	for num in dice_lst:

		strong_blocks = find_max_strength(defending_blocks)

		if num <= attack_block_block.attack_number:
			if defender_type == 'comp':

				block_to_get_hurt = strong_blocks[random.randint(0, len(strong_blocks) - 1)]
				block_to_get_hurt.get_hurt(1)
				print(block_to_get_hurt.name, 'got hurt!')
			else: #if defender is a human ('opp')
				bad_input = True
				index = 0
				while bad_input:
					print('Who do you want to get hurt? (Type index in list below:)')
					for i, block in enumerate(strong_blocks):
						print(block.name + '[' + str(i) + ']', end = '; ')
					try:
						index = int(input('>'))
					except ValueError:
						print('type a number')
						continue
						
					
					if index not in range(len(strong_blocks)):
						print('not valid index')
					else:
						bad_input = False


				block_to_get_hurt = strong_blocks[index]
				block_to_get_hurt.get_hurt(1)
				print(block_to_get_hurt.name, 'got hurt!')




			
			
	
			





def check_if_dead(attackers_lst, defenders_lst, attack_reinforcements, defense_reinforcements, eng_pool = list(), scot_pool = list()):
	"""
	checkers if attackers and defenders are alive
	moves nobles to different reinforcements
	moves dead to the roster
	if king dies then returns stuff
	"""
	attacker_is_dead = True
	defender_is_dead = True


	indexes_to_pop = list()

	
	for i, block in enumerate(attackers_lst):
	

		if block.type == 'KING' and block.is_dead():
			print('\n', block.name , ' has died and the game is over')
			if block.allegiance == 'ENGLAND':
				raise exceptions.EnglishKingDeadException()
			else:
				raise exceptions.ScottishKingDeadException()
		elif block.has_cross and block.is_dead():

			print('\n', block.name, ' has died and will never come back')

			if block.name == 'EDWARD':
				print('However, his son is in the pool and will save the day')
			
			indexes_to_pop.append(i)
	
				
		
		elif type(block) == blocks.Noble and block.is_dead():


			block.change_allegiance()
			
			defense_reinforcements.append(attackers_lst[i])
			indexes_to_pop.append(i)

			print('\n', block.name, ' has changed sides and has been added to defense reinforcements')
		elif type(block) != blocks.Noble and block.is_dead():

			print('\n', block.name, ' has died and goes to the pool')
			indexes_to_pop.append(i)
		
			
		if not block.is_dead():
	
			attacker_is_dead = False


	for index in indexes_to_pop:
		attackers_lst[index] = 'dead'

	all_alive = False
	while not all_alive:
		try:
			attackers_lst.remove('dead')
		except ValueError:
			all_alive = True


	indexes_to_pop = list()





	for i, block in enumerate(defenders_lst):


		
		if block.type == 'KING' and block.is_dead():
			print('\n', block.name , ' has died and the game is over')
			if block.allegiance == 'ENGLAND':
				raise exceptions.EnglishKingDeadException()
			else:
				raise exceptions.ScottishKingDeadException()

		elif block.has_cross and block.is_dead():

			print('\n', block.name, ' has died and will never come back')
			if block.name == 'EDWARD':
				print('However, his son is in the pool and will save the day')
			indexes_to_pop.append(i)
			

		elif type(block) == blocks.Noble and block.is_dead():
			
			block.change_allegiance()

			attack_reinforcements.append(defenders_lst[i])
			indexes_to_pop.append(i)

			print('\n', block.name, ' has changed sides and has been added to attack reinforcements')
		
		elif type(block) != blocks.Noble and block.is_dead():

			print('\n', block.name, ' has died and goes to the pool')
			indexes_to_pop.append(i)
			

		if not block.is_dead():
			
			defender_is_dead = False

	for index in indexes_to_pop:
		defenders_lst[index] = 'dead'

	all_alive = False
	while not all_alive:
		try:
			defenders_lst.remove('dead')
		except ValueError:
			all_alive = True


	

	if attackers_lst == []:
		attacker_is_dead = True
	if defenders_lst == []:
		defender_is_dead = True

		
	return attacker_is_dead, defender_is_dead


def retreat_locations(board, attacking, defending, is_attacking):
	'''
	This function is passed a board object, list of attackers, list of defenders and a boolean that is true
	if the computer is attacking and false if the computer is defending. ####NOPE NOT ANYMORE
	It returns a list of all the locations where a block can retreat to
	'''
	

	if len(attacking) != 0:
		is_attacking = True
		current_location = find_location(board, attacking[0])
	else:
		is_attacking = False
		current_location = find_location(board, defending[0])
		attacking = defending

	
	
	possible_locations = []
	region_allegiance = None
	#Create list of possible locations to retreat to

	if current_location:

		for x, border in enumerate(board.dynamic_borders[current_location.regionID]):

			went_through_loop = False
			
			for i, block in enumerate(board.regions[x].blocks_present):
				went_through_loop = True

				if block.name == 'FRENCH':
					block.movement_points = 1


				region_allegiance = board.regions[x].blocks_present[0].allegiance


				if is_attacking == False and defending[0].allegiance == region_allegiance and border != 0 and \
				(board.attacked_borders[x][current_location.regionID] != 'attack') and (defending[0].name != 'NORSE' or board.regions[x].coast)\
				and (defending[0].allegiance == 'ENGLAND' or x != 22) and (defending[0].allegiance == 'SCOTLAND' or x == 22 or current_location.regionID)\
				and (not board.regions[x].is_contested()):
					possible_locations.append(board.regions[x])
				elif is_attacking == True and attacking[0].allegiance == region_allegiance and border != 0 and \
				(attacking[0].name != 'NORSE' or board.regions[x].coast) and (attacking[0].allegiance == 'ENGLAND' or x != 22) \
				and (attacking[0].allegiance == 'SCOTLAND' or x == 22 or current_location.regionID != 22) \
				and (not board.regions[x].is_contested()) and (board.attacked_borders[x][current_location.regionID] != 'defense'):
					possible_locations.append(board.regions[x])

			#print("Is", x, "and", current_location.regionID, "attacked border updated?", board.attacked_borders[x][current_location.regionID])
			if not went_through_loop and border != 0 and (attacking[0].allegiance == 'ENGLAND' or x != 22) and (attacking[0].allegiance == 'SCOTLAND' or x == 22\
				or current_location.regionID != 22) and (is_attacking == True and (board.attacked_borders[x][current_location.regionID] != 'defense') or (is_attacking == False and board.attacked_borders[x][current_location.regionID] != 'attack')):
				
				possible_locations.append(board.regions[x])

	return possible_locations

def regroup_locations(board, attacking, defending, is_attacking):
	'''
	This function is passed a board object, list of attackers, list of defenders and a boolean that is true
	if the computer is attacking and false if the computer is defending.
	It returns a list of all the locations where a block can retreat to


	THIS FUNCTION WAS ORIGINALLY RETREAT LOCATIONS SO IT'S WRITTEN VERY BADLY BUT SHOULD WORK IN THEORY

	defending is an empty list
	is_attacking is always false
	'''



	if len(attacking) != 0:
		print(attacking[0].name)
		current_location = find_location(board, attacking[0])
		is_attacking = True
	else:
		is_attacking = False
		print(defending[0].name)
		current_location = find_location(board, defending[0])
		attacking = defending
	possible_locations = []
	#Create list of possible locations to retreat to
	region_allegiance = None
	for x, border in enumerate(board.dynamic_borders[current_location.regionID]):
		went_through_loop = False
		
		for i, block in enumerate(board.regions[x].blocks_present):
			went_through_loop = True
			if block.name == 'FRENCH':
				block.movement_points = 1
		
			




			if i == 0:
				region_allegiance = board.regions[x].blocks_present[i].allegiance
			elif region_allegiance != board.regions[x].blocks_present[i].allegiance:
				region_allegiance = 'fight is going on'
				break
			

			'''
			if border != 0:
				print(board.regions[x].name , '\n\n\n\n')
				print(attacking[0].allegiance, region_allegiance)
				print(border)
				print(block.name != 'NORSE' or board.regions[x].coast)
				print(block.allegiance == 'ENGLAND' or x != 22)
				print(block.allegiance == 'SCOTLAND' or x == 22 or find_location(board, block).regionID != 22)
			'''

			if attacking[0].allegiance == region_allegiance and border != 0 \
		    	and (block.name != 'NORSE' or board.regions[x].coast) \
					and (attacking[0].allegiance == 'ENGLAND' or x != 22) and \
					(attacking[0].allegiance == 'SCOTLAND' or x == 22 or find_location(board, block).regionID != 22)\
					and (not board.regions[x].is_contested()):
				possible_locations.append(board.regions[x])
		if not went_through_loop and border != 0 and (attacking[0].allegiance == 'ENGLAND' or x != 22) and (attacking[0].allegiance == 'SCOTLAND' or x == 22\
			or current_location.regionID != 22):
			possible_locations.append(board.regions[x])
	possible_locations.append(current_location)
	return possible_locations

def should_retreat(board, attacking = None, defending = None, attacking_reinforcement = list(), defending_reinforcement = list(), is_attacking = None,\
	combat_letter = 'A', combat_round = 0, turn = 'defender', retreat_constant = 0.3, attacking_block = None):
	'''
	This function takes in all the group that are involved in a battle and a boolean about whether the computer is attacking or not. 
	The should_retreat function will return either False, meaning the computer should not retreat, or a location in which the computer should
	retreat its blocks to.
	'''

	attacking_copy = copy.deepcopy(attacking)
	defending_copy = copy.deepcopy(defending)
	attacking_rein_copy = copy.deepcopy(attacking_reinforcement)
	defending_rein_copy = copy.deepcopy(defending_reinforcement)

	simulation_dict = simulations.simulation(attacking_copy, defending_copy, 1000, attacking_rein_copy, defending_rein_copy, combat_letter, combat_round, turn)
	win_percentage = 0
	#Calculate the win percentage based on if you are attacking or defending in the simulation

	
	if is_attacking:
		win_percentage = simulation_dict['attacker wins']
	else:
		win_percentage = simulation_dict['defender wins'] + simulation_dict['attacker retreats']
	
	#Insert code to check to see if it should retreat

	possible_locations = []

	if is_attacking:
		
		possible_locations = list(retreat_locations(board, [attacking_block], [], is_attacking))
	else:
		
		possible_locations = list(retreat_locations(board, [], [attacking_block], is_attacking))


	if len(possible_locations) == 0:
		return False


	if len(attacking) > 0:
		found_location = find_location(board, attacking[0])
		if found_location:
			current_location = found_location.regionID
		else:
			current_location = None
	elif len(attacking_reinforcement) > 0:
		current_location = find_location(board, attacking_reinforcement[0]).regionID

	possible_locations_id = list()
	for location in possible_locations:
		possible_locations_id.append(location.regionID)
	choice_dictionary = retreat.retreat(board, current_location, possible_locations_id, simulation_dict, is_attacking, board.turn)
	choice = weighted_prob.weighted_prob(choice_dictionary)
	

	if choice == 'Staying value ':
		return False
	else:
		choice = board.regions[int(choice)]
	
		return choice
	
def print_situation(attack, defense, attack_reinforcements, defense_reinforcements):
	"""
	does nothing but print stuff
	"""
	print()
	print('attack:', end = ' ')
	for block in attack:
		print(block.name, '-', block.current_strength, end = '\t')
	print()
	print('defense:', end = ' ')
	for block in defense:
		print(block.name, '-', block.current_strength, end = '\t')
	print()
	print('attacking reinforcements:', end = ' ')
	for block in attack_reinforcements:
		print(block.name, '-', block.current_strength, end = '\t')
	print()
	print('defending reinforcements:', end = ' ')
	for block in defense_reinforcements:
		print(block.name, '-', block.current_strength, end = '\t')
	print('\n')

def regroup(winner_blocks, current_board, eng_type, scot_type):
	"""
	regroups after someone wins
	winner_blocks is a list of winning blocks
	current_board is board
	"""
	
	if winner_blocks:

		if winner_blocks[0].allegiance == 'ENGLAND':
			winner_type = eng_type
		elif winner_blocks[0].allegiance == 'SCOTLAND':
			winner_type = scot_type

		if winner_type == 'comp':
			for block in winner_blocks:

				original_location = find_location(current_board, block)
				#print(original_location)
				#print('111111111')

				possible_locations = regroup_locations(current_board, [block], [], False)

				possible_locations_id = list()
				for location in possible_locations:
					possible_locations_id.append(location.regionID)

				current_location = find_location(current_board, winner_blocks[0])
				#Call the regrouping utility function which returns the ID of a region that the block should regroup to
				place_to_go_to = search.region_id_to_object(current_board, regroup_util.regroup_utility(current_board, current_location.regionID, possible_locations_id))

				if len(possible_locations) == 1:
					print(block.name, ' stays')
					continue
				else:

					#place_to_go_to is now a regionID, now a Region
					place_to_go_to = place_to_go_to.regionID
					#print(place_to_go_to)
					current_board.add_to_location(block, place_to_go_to)

					current_board.dynamic_borders[original_location.regionID][place_to_go_to] -= 1

					if block.name == 'FRENCH':
						block.movement_points = 0
					print(block.name, ' moved to ', search.region_id_to_name(current_board, place_to_go_to))
		elif winner_type == 'opp':
			for block in winner_blocks:

				original_location = find_location(current_board, block)
				bad_input = True
				#print('22222222')
				possible_locations = regroup_locations(current_board, [block], [], False)

				for i, region in enumerate(possible_locations):
					print(region.name, region.regionID, end = '; ')

				while bad_input:
					place_to_go_to_str = input('Which location to regroup to? (type number) >')
					if not place_to_go_to_str.isdigit():
						print('type a number')
						
					else:
						place_to_go_to = int(place_to_go_to_str)

						for region in possible_locations:
							if place_to_go_to == region.regionID:
								bad_input = False
							else:
								print('Enter a valid region ID.')


				place_to_go_to = region.regionID
					


				if not bad_input:
					if place_to_go_to != -1:

						current_board.add_to_location(block, place_to_go_to)

						current_board.dynamic_borders[original_location.regionID][place_to_go_to] -= 1

					if block.name == 'FRENCH':
						block.movement_points = 0
						print(block.name, ' moved to ', search.region_id_to_name(current_board, place_to_go_to))

	current_board.reset_borders()
	current_board.reset_attacked_borders()


def retreat_block(board, block_to_retreat, is_attacking, eng_type, scot_type, attack, defense, a_rein, d_rein, letter, round, turn, have_to_retreat = False):
	"""
	does actual retreating
	returns False if no locations
	"""
	#find possible locations
	possible_retreat_locations = list()
	if is_attacking:
		possible_retreat_locations = retreat_locations(board, [block_to_retreat], [], True)
	else:
		possible_retreat_locations = retreat_locations(board, [], [block_to_retreat], False)


	#remove duplicates
	possible_retreat_locations = list(set(possible_retreat_locations))


	if len(possible_retreat_locations) == 0:
		return False


	#find computer role
	role = 'opp'
	if block_to_retreat.allegiance == 'ENGLAND':
		role = eng_type
	else:
		role = scot_type


	#find where to retreat to 
	if role == 'opp':
		print('possible retreat locations:')
		for i, location in enumerate(possible_retreat_locations):
			print(location.name + '[' + str(i) + ']', end = ' ')
		print('Where you would like to rereat to? (type number)')
		bad_input = True
		while bad_input:
			location_index_str = input('>')
			if not location_index_str.isdigit():
				bad_input = True
			else:
				location_index = int(location_index_str)
				if location_index not in range(len(possible_retreat_locations)):
					bad_input = True
				else:
					bad_input = False
		region_to_retreat_to = possible_retreat_locations[location_index]
	else:
		region_to_retreat_to = should_retreat(board, attacking = attack, defending = defense, attacking_reinforcement = a_rein, defending_reinforcement = d_rein, is_attacking = is_attacking,\
	combat_letter = letter, combat_round = round, turn = turn, retreat_constant = 0.3, attacking_block = block_to_retreat)
		if region_to_retreat_to == False:
			if have_to_retreat:
				region_to_retreat_to = random.choice(possible_retreat_locations)
			else:
				return False




	#retreat block
	proper_list = list()
	if block_to_retreat in attack:
		proper_list = attack
	elif block_to_retreat in defense:
		proper_list = defense
	elif block_to_retreat in a_rein:
		proper_list = a_rein
	else:
		proper_list = d_rein

	retreat_block_to_location(board, block_to_retreat, region_to_retreat_to, proper_list)
	return True



def retreat_block_to_location(board, block_to_retreat, region, proper_list):
	"""
	actually moves the block
	prints that it moves the block
	proper_list is like defense or attack or reinforcements
	returns nothing
	"""
	original_location = find_location(board, block_to_retreat)
	board.add_to_location(block_to_retreat, region)
	proper_list.remove(block_to_retreat)

	
	
	
	
	board.dynamic_borders[original_location.regionID][region.regionID] -= 1
	print(block_to_retreat.name + ' has retreated to ' + region.name)


	

	
def battle(attack, defense, attack_reinforcements = list(), defense_reinforcements = list(), current_board = None, eng_type='opp', scot_type='comp'):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	can start battle in the middle
	
	returns what happens

	
	TAKES NO INPUT


	
	'''
	if attack == list():
		attack = attack_reinforcements
		attack_reinforcements = list()
	elif defense == list():
		defense = defense_reinforcements
		defense_reinforcements = list()


	attacking_allegiance = attack[0].allegiance
	
	if attacking_allegiance == 'ENGLAND':
		attacker_type = eng_type
		defender_type = scot_type
	elif attacking_allegiance == 'SCOTLAND':
		attacker_type = scot_type
		defender_type = eng_type
		
		

	
	
	print_situation(attack, defense, attack_reinforcements, defense_reinforcements)
	

	# Divide each side into letter groups (dictionary)

	letter_found = False
	number_found = False
	turn_found = False


	for block in defense + defense_reinforcements:
		if type(block) == blocks.Noble and type(block.home_location) == tuple and find_location(current_board, block).regionID in block.home_location:
			block.b2_to_b3()
		elif type(block) == blocks.Noble and find_location(current_board, block).regionID == block.home_location:
			block.b2_to_b3()

	attackers = organize(attack)
	defenders = organize(defense)



	attackers_allegiance = attack[0].allegiance
	defenders_allegiance = defense[0].allegiance
	
	attacker_is_dead = False
	defender_is_dead = False


	

#run through the combat rounds

		
	for combat_round in range(3):



		current_board.reset_borders()
		

		if combat_round != 0:

			
			attack += attack_reinforcements
			defense += defense_reinforcements


			attackers = organize(attack)
			defenders = organize(defense)


			attack_reinforcements = list()
			defense_reinforcements = list()
			print_situation(attack, defense, attack_reinforcements, defense_reinforcements)


		for block in attack + defense:
			try:
				if block.checked:
					pass
			except AttributeError:
				if block.name == 'ULSTER' or block.name == 'WALES-INFANTRY' or block.name == 'WALES-ARCHER':
					loyalty = random.randint(1, 6)
					print(block.name, 'has rolled a', loyalty, 'to check for loyalty')
					if loyalty in range(1, 5):
						print(block.name, 'is loyal')
					else:
						print(block.name, 'has run away!')
						block.checked = True
						block.current_strength = 0
						if block in attack:
							attack.remove(block)
						else:
							defense.remove(block)
						
			
		for letter in 'ABC':
			
			input()
					
				
			for attacking_block in defenders[letter]:
				if attacking_block.allegiance != defenders_allegiance:
					break
				print_situation(attack, defense, attack_reinforcements, defense_reinforcements)

				if attack == list():
					break

			
				
				



				if not attacking_block.is_dead():

					if defender_type == 'opp':

						
						bad_input = True

						while bad_input:
							#attack or retreat
							print('What does ', attacking_block.name, 'do? (r) retreat (f) fight (p) pass')
							option = input('>')
							possible_locations = retreat_locations(current_board, [],[attacking_block], False)
							if option == 'r':

								if retreat_block(current_board, attacking_block, False, eng_type, scot_type, attack, defense, attack_reinforcements, defense_reinforcements, letter, combat_round, 'defender') == False:
									print('you have no locations to retreat')
									continue
								else:
									bad_input = False
							

							elif option == 'f':
								#fight
								attack_block(attacking_block, attack, eng_type, scot_type)

							
								bad_input = False
							elif option == 'p':
								bad_input = False

							else:
								print('type in a proper letter (r) or (f) or (p)')
								bad_input = True
					else:   #if defender_type == 'comp'


						if retreat_block(current_board, attacking_block, False, eng_type, scot_type, attack, defense, attack_reinforcements, defense_reinforcements, letter, combat_round, 'defender') == False:
							attack_block(attacking_block, attack, eng_type, scot_type)


			
					
					



			
				attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements, current_board.eng_pool, current_board.scot_pool)


				if (attacker_is_dead and combat_round != 0) or (attacker_is_dead and attack_reinforcements == []):
				
					regroup(defense + defense_reinforcements, current_board, eng_type, scot_type)
					current_board = update_roster.update_roster(current_board = current_board)
		
					print('defender wins')
					
				

					return 'defender wins'
				if (defender_is_dead and combat_round != 0) or (defender_is_dead and defense_reinforcements == []):
		
					regroup(attack + attack_reinforcements, current_board, eng_type, scot_type)
					current_board = update_roster.update_roster(current_board = current_board)
					print('attacker wins')
			


					return 'attacker wins'
						
			
		
			for attacking_block in attackers[letter]:
				if attacking_block.allegiance != attackers_allegiance:
					break
				print_situation(attack, defense, attack_reinforcements, defense_reinforcements)

				if defense == list():
					break

			


						
				


				if not attacking_block.is_dead():
					
					if attacker_type == 'opp':

						
						bad_input = True
						possible_locations = retreat_locations(current_board, [attacking_block], [], True)
						while bad_input:
							print('What does ', attacking_block.name, 'do? (r) retreat (f) fight (p) pass')
							option = input('>')
							if option == 'r':

								if retreat_block(current_board, attacking_block, True, eng_type, scot_type, attack, defense, attack_reinforcements, defense_reinforcements, letter, combat_round, 'attacker') == False:
									print('you have no locations to retreat')
									continue
								else:
									bad_input = False

							elif option == 'f':
								#print(1)
								attack_block(attacking_block, defense, eng_type, scot_type)
								
								bad_input = False
							elif option == 'p':
								bad_input = False

							else:
								print('type in a proper letter (r) or (f) or (p)')
								bad_input = True
					else:   #if attacker_type == 'comp'



						if retreat_block(current_board, attacking_block, True, eng_type, scot_type, attack, defense, attack_reinforcements, defense_reinforcements, letter, combat_round, 'attacker') == False:
							attack_block(attacking_block, defense, eng_type, scot_type)
							

				
						
							

				
					
					

				attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements, current_board.eng_pool, current_board.scot_pool)
				
				
				if (defender_is_dead and combat_round != 0) or (defender_is_dead and defense_reinforcements == []):
					regroup(attack + attack_reinforcements, current_board, eng_type, scot_type)
					current_board = update_roster.update_roster(current_board = current_board)
					
					print('attacker wins')
			
					
					return 'attacker wins'
				if (attacker_is_dead and combat_round != 0) or (attacker_is_dead and attack_reinforcements == []):
					regroup(defense + defense_reinforcements, current_board, eng_type, scot_type)
					current_board = update_roster.update_roster(current_board = current_board)
		
					print('defender wins')
				



					
					return 'defender wins'

	
	print('attacker retreats')

	attack += attack_reinforcements
	defense += defense_reinforcements
	for attacking_block in attack + attack_reinforcements:
		
		if retreat_block(current_board, attacking_block, True, eng_type, scot_type, attack, defense, attack_reinforcements, \
			defense_reinforcements, letter, combat_round, 'attacker', True) == False:

		
			print(attacking_block.name, 'cannot retreat!')
			attacking_block.current_strength = 0

			if block.type == 'KING' and block.is_dead():
				print('\n', block.name , ' has died and the game is over')
			

			elif block.has_cross and block.is_dead():

				print('\n', block.name, ' has died and will never come back')
				if block.name == 'EDWARD':
					print('However, his son is in the pool and will save the day')
				
				

			elif type(block) == blocks.Noble and block.is_dead():
				
				block.change_allegiance()

				

				print('\n', block.name, ' has changed sides and has been added to attack reinforcements')
			
			elif type(block) != blocks.Noble and block.is_dead():

				print('\n', block.name, ' has died and goes to the pool')
				

		


	regroup(defense + defense_reinforcements, current_board, eng_type, scot_type)
	current_board = update_roster.update_roster(current_board = current_board)

	return 'attacker retreats'






def main():
	blocks1 = initialize_blocks.initialize_blocks()

	print(simulations.simulation([blocks.Block(attack_number = 2, attack_letter = 'A', initial_attack_strength = 4)], [blocks.Block(attack_number = 2, attack_letter = 'A', initial_attack_strength = 4)], 1000))

if __name__ == '__main__':
	main()








