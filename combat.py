import dice
import random
import blocks
import initialize_blocks
import copy
import update_roster
import simulations
def find_location(board, blok):

	for region in board.regions:
		for bllock in region.blocks_present:
			
			if bllock.name == blok.name:
				return region
		
	raise Exception('cannot find block')

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


def attack_block(attack_block_block, defending_blocks, computer_role = 'ENGLAND'):
	"""
	attacks blocks
	uses random in case where everyone same health
	attack_block_block is the block attacking
	defending_blocks is the list of all defending blocks to be attacked
	"""
	attacking_allegiance = attack_block_block.allegiance

	if defending_blocks == []:
		return False
	dice_lst = dice.roll(attack_block_block.current_strength)
	print(attack_block_block.name, ' rolled ' , dice_lst)



	for num in dice_lst:

		strong_blocks = find_max_strength(defending_blocks)

		if num <= attack_block_block.attack_number:
			if computer_role != attacking_allegiance:
				block_to_get_hurt = strong_blocks[random.randint(0, len(strong_blocks) - 1)]
			else:
				bad_input = True
				while bad_input:
					print('Who do you want to get hurt? (Type number)')
					for i, block in enumerate(defending_blocks):
						print(block.name, '[', i, ']', end = ' ')
					index = input('>')
					if type(index) != int:
					
						print('type in a number')
					elif index not in range(len(defending_blocks) - 1):
						print('not valid index')
					else:
						bad_input = False
						block_to_get_hurt = defending_blocks[index]


			
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
	
	for i, block in enumerate(attackers_lst):
	

		if block.type == 'KING' and block.is_dead():
		
			return True, False
		elif block.has_cross and block.is_dead():
			if current_board == None:
				attackers_lst.pop(i)
			else:
				attackers_lst.pop(i)
				
		
		elif type(block) == blocks.Noble and block.is_dead():
			block.change_allegiance()
	
			defense_reinforcements.append(attackers_lst.pop(i))
		elif type(block) != blocks.Noble and block.is_dead():
			if block.allegiance == 'ENGLAND':
				eng_pool.append(attackers_lst.pop(i))
			else:
				scot_pool.append(attackers_lst.pop(i))
		
			
		if not block.is_dead():
	
			attacker_is_dead = False


	for i, block in enumerate(defenders_lst):


		
		if block.type == 'KING' and block.is_dead():
	
			return False, True

		elif block.has_cross and block.is_dead():

			defenders_lst.pop(i)
			

		elif type(block) == blocks.Noble and block.is_dead():
			
			block.change_allegiance()

			attack_reinforcements.append(defenders_lst.pop(i))
		elif type(block) != blocks.Noble and block.is_dead():
			if block.allegiance == 'ENGLAND':
				eng_pool.append(defenders_lst.pop(i))
			else:
				scot_pool.append(defenders_lst.pop(i))
			

		if not block.is_dead():
	
			defender_is_dead = False

	return attacker_is_dead, defender_is_dead


def retreat_locations(board, attacking, defending, is_attacking):
	'''
	This function is passed a board object, list of attackers, list of defenders and a boolean that is true
	if the computer is attacking and false if the computer is defending.
	It returns a list of all the locations where a block can retreat to
	'''

	current_location = find_location(board, attacking[0])
	possible_locations = []
	#Create list of possible locations to retreat to
	for x, border in enumerate(board.static_borders[current_location.regionID]):

		
		for i, block in enumerate(board.regions[x].blocks_present):
			if i == 0:
				region_allegiance = board.regions[x].blocks_present[i]
			elif region_allegiance != board.regions[x].blocks_present[i]:
				region_allegiance = 'fight is going on'
				break

		if is_attacking == False and attacking[0].allegiance != region_allegiance and border != 'X':
			possible_locations.append(board.regions[x])
		elif is_attacking == True and defending[0].allegiance != region_allegiance and border != 'X':
			possible_locations.append(board.regions[x])

	return possible_locations

def should_retreat(board, attacking = None, defending = None, attacking_reinforcement = list(), defending_reinforcement = list(), is_attacking = None,\
	combat_letter = 'A', combat_round = 0, retreat_constant = .3):
	'''
	This function takes in all the group that are involved in a battle and a boolean about whether the computer is attacking or not. 
	The should_retreat function will return either False, meaning the computer should not retreat, or a location in which the computer should
	retreat its blocks to.
	'''

	attacking_copy = copy.deepcopy(attacking)
	defending_copy = copy.deepcopy(defending)
	attacking_rein_copy = copy.deepcopy(attacking_reinforcement)
	defending_rein_copy = copy.deepcopy(defending_reinforcement)

	simulation_dict = simulations.simulation(attacking_copy, defending_copy, 1000, attacking_reinforcement, defending_reinforcement, combat_letter, combat_round)
	win_percentage = 0
	#Calculate the win percentage based on if you are attacking or defending in the simulation
	if is_attacking:
		win_percentage = float(simulation_dict['attacker wins'])/1000
	else:
		win_percentage = float(simulation_dict['defender wins'])/1000
	
	#Insert code to check to see if it should retreat

	if win_percentage > retreat_constant:
		return False
	else:
		possible_locations = retreat_locations(board, attacking, defending, is_attacking)
		num = random.randint(0, len(possible_locations)-1)
		return possible_locations[num]

def print_situation(attack, defense, attack_reinforcements, defense_reinforcements):
	"""
	does nothing but print stuff
	"""
	print('\n\n')
	print('attack:', end = ' ')
	for block in attack:
		print(block.name, ':', block.current_strength, end = '\t')
	print('\n\n')
	print('defense:', end = ' ')
	for block in defense:
		print(block.name, ':', block.current_strength, end = '\t')
	print('\n\n')
	print('attacking reinforcements:', end = ' ')
	for block in attack_reinforcements:
		print(block.name, ':', block.current_strength, end = '\t')
	print('\n\n')
	print('defending reinforcements:', end = ' ')
	for block in defense_reinforcements:
		print(block.name, ':', block.current_strength, end = '\t')

def battle(attack, defense, attack_reinforcements = list(), defense_reinforcements = list(), current_board = None, before_letter = 'A', before_number = 0, turn = 'defender', computer_role = 'ENGLAND'):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	can start battle in the middle
	
	returns what happens

	
	TAKES NO INPUT



	'''
	print(type(current_board))
	# Divide each side into letter groups (dictionary)
	letter_found = False
	number_found = False
	turn_found = False


	attackers = organize(attack)
	defenders = organize(defense)

	attackers_allegiance = attack[0].allegiance
	defenders_allegiance = defense[0].allegiance
	
	attacker_is_dead = False
	defender_is_dead = False

#run through the combat rounds

	for combat_round in range(3):

		if not number_found and combat_round != before_number:
	
			pass
		else:
			number_found = True

			if combat_round >= 1:
				

				attack += attack_reinforcements
				defense += defense_reinforcements

				attack_reinforcements = list()
				defense_reinforcements = list()
				
			
				
				attackers = organize(attack)
				defenders = organize(defense)


			for letter in 'ABC':
				if not letter_found and letter != before_letter:
					
					pass
				else:
					letter_found = True
					#defenders first
					if not turn_found and 'defender' != turn:
						pass
					else:
						turn_found = True
						for letter2 in defenders:
							if letter2 == letter:
								for attacking_block in defenders[letter2]:
									if attacking_block.name == 'WALES' or attacking_block.name == 'ULSTER':
										if random.randint(0,2) == 0:
											attacking_block.current_strength = 0
											print(attacking_block.name, 'has run away!')
											


									print_situation(attack, defense, attack_reinforcements, defense_reinforcements)
									if not attacking_block.is_dead():
										if computer_role != defenders_allegiance:
											print('What does ', attacking_block.name, 'do? (r) retreat (f) fight')
											option = input('>')
											bad_input = True
											while bad_input:
												if option == 'r':
													bad_input = False
													valid_location = False
													while not valid_location:
														regionID_to_retreat_to = input('What regionID to retreat to: ')
														possible_locations = should_retreat(current_board, attack, defense, attack_reinforcements, defense_reinforcements, False, 'A', 0, -1.0)
														
														for location in possible_locations:
															if location.regionID == regionID_to_retreat_to:
																valid_location = True
																break
														if not valid_location:
															print('please type in a valid location')


													current_board.move_block(attacking_block, find_location(current_board, attacking_block).regionID, regionID_to_retreat_to)
													print(attacking_block, ' retreated to ', current_board.regions[regionID_to_retreat_to].name)

												elif option != 'f':
													attack_block(attacking_block, defense, computer_role)
													
												bad_input = False
										else:
											option = should_retreat(current_board, attack, defense, attack_reinforcements, defense_reinforcements, False, 'A', 0)
											regionID_to_retreat_to = option.regionID
												
											if option != False:
												current_board.move_block(attacking_block, find_location(current_board, attacking_block).regionID, option.regionID)
												print(attacking_block, ' retreated to ', current_board.regions[regionID_to_retreat_to].name)
											else:
												attack_block(attacking_block, defense, computer_role)
								
										
										



					
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements, current_board.eng_pool, current_board.scot_pool)
							
									if attacker_is_dead and combat_round != 0:
										update_roster.update_roster(current_board = current_board)
										return 'defender wins'
								
					if not turn_found and 'attacker' != turn:
						pass
					else:
						turn_found = True
						for letter2 in attackers:
							if letter2 == letter:
								for attacking_block in attackers[letter2]:
									if attacking_block.name == 'WALES' or attacking_block.name == 'ULSTER':
										if random.randint(0,2) == 0:
											attacking_block.current_strength = 0
											print(attacking_block.name, 'has run away!')
											
									
									print_situation(attack, defense, attack_reinforcements, defense_reinforcements)
									if not attacking_block.is_dead():
										if computer_role != defenders_allegiance:
											print('What does ', attacking_block.name, 'do? (r) retreat (f) fight')
											option = input('>')
											bad_input = True
											while bad_input:
												if option == 'r':
													bad_input = False
													valid_location = False
													while not valid_location:
														regionID_to_retreat_to = input('What regionID to retreat to: ')
														possible_locations = should_retreat(current_board, attack, defense, attack_reinforcements, defense_reinforcements, False, 'A', 0, -1.0)
														
														for location in possible_locations:
															if location.regionID == regionID_to_retreat_to:
																valid_location = True
																break
														if not valid_location:
															print('please type in a valid location')
													current_board.move_block(attacking_block, find_location(current_board, block).regionID, regionID_to_retreat_to)
													print(attacking_block, ' retreated to ', current_board.regions[regionID_to_retreat_to].name)
												elif option != 'f':
													attack_block(attacking_block, defense, computer_role)
													
												bad_input = False
										else:

											option = should_retreat(current_board, attack, defense, attack_reinforcements, defense_reinforcements, True, 'A', 0)
											regionID_to_retreat_to = option.regionID
											if option != False:
												current_board.move_block(attacking_block, find_location(current_board, attacking_block).regionID, option.regionID)
												print(attacking_block, ' retreated to ', current_board.regions[regionID_to_retreat_to].name)
											else:
												attack_block(attacking_block, defense)
									
										attack_block(attacking_block, defense, computer_role)

				
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements, current_board.eng_pool, current_board.scot_pool)
			
									if defender_is_dead and combat_round != 0:
										update_roster.update_roster(current_board = current_board)
										return 'attacker wins'
	update_roster.update_roster(current_board = current_board)
	return 'attacker retreats'


def main():
	blocks1 = initialize_blocks.initialize_blocks()

	print(simulations.simulation([blocks.Block(attack_number = 2, attack_letter = 'A', initial_attack_strength = 4)], [blocks.Block(attack_number = 2, attack_letter = 'A', initial_attack_strength = 4)], 1000))

if __name__ == '__main__':
	main()








