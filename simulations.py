import combat
import blocks
import copy
import random

def battle(attack, defense, attack_reinforcements = list(), defense_reinforcements = list(), before_letter = 'A', before_number = 0, turn = 'defender'):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	returns what happens


	TAKES NO INPUT



	'''

	# Divide each side into letter groups (dictionary)
	letter_found = False
	number_found = False
	turn_found = False


	attackers = combat.organize(attack)
	defenders = combat.organize(defense)

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
				
			
				
				attackers = combat.organize(attack)
				defenders = combat.organize(defense)


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

									combat.attack_block(attacking_block, attack)



					
									attacker_is_dead, defender_is_dead = combat.check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements)
							
									if attacker_is_dead and combat_round != 0:
										
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

									combat.attack_block(attacking_block, defense)

				
									attacker_is_dead, defender_is_dead = combat.check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements)
			
									if defender_is_dead and combat_round != 0:

										return 'attacker wins'

	return 'attacker retreats'

def simulation(attack, defense, num_times, attack_reinforcements = list(), defense_reinforcements = list(), before_letter = 'A', before_number = 0, turn = 'defender'):
	"""
	attack is list of attacking blocks
	defense is list of defending blocks
	num_times is number of simulations
	returns dictionary with estimated probabilities
	"""
	original_attack = copy.deepcopy(attack)
	original_defense = copy.deepcopy(defense)
	original_attack_reinforcements = copy.deepcopy(attack_reinforcements)
	original_defense_reinforcements = copy.deepcopy(defense_reinforcements)

	totals_dict = {'attacker wins':0, 'defender wins':0, 'attacker retreats':0}
	for j in range(num_times):


	
		for i, element in enumerate(attack):
			if len(element) != 1:
				attack[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)


		for i, element in enumerate(defense):
			if len(element) != 1:
				defense[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)


		totals_dict[battle(attack, defense, attack_reinforcements, defense_reinforcements, before_letter, before_number, turn)] += 1
	
		attack, defense = copy.deepcopy(original_attack), copy.deepcopy(original_defense)

		attack_reinforcements, defense_reinforcements = copy.deepcopy(original_attack_reinforcements), copy.deepcopy(original_defense_reinforcements)

	for situation in totals_dict:
		totals_dict[situation] /= num_times

	return totals_dict


def pick_random_block(block_tuple, attack, defense, attack_reinforcements, defense_reinforcements):
	"""
	if multiple blocks unkonwn
	send all possible blocks in tuple
	then it will pick a random one
	"""
	repeat_block = True

	while repeat_block:
		block_to_be_attacked = block_tuple[random.randint(0, len(block_tuple) - 1)]
		repeat_block = False
		for block in attack:
			if block is block_to_be_attacked:
				repeat_block = True
				break
		if not repeat_block:
			for block in defense:
				if block is block_to_be_attacked:
					repeat_block = True
					break
		if not repeat_block:
			for block in attack_reinforcements:
				if block is block_to_be_attacked:
					repeat_block = True
					break
		if not repeat_block:
			for block in defense_reinforcements:
				if block is block_to_be_attacked:
					repeat_block = True
					break

	return block_to_be_attacked

def should_retreat(board, attacking = None, defending = None, attacking_reinforcement = list(), defending_reinforcement = list(), is_attacking = None,\
	combat_letter = 'A', combat_round = 0):
	'''
	This function takes in all the group that are involved in a battle and a boolean about whether the computer is attacking or not. 
	The should_retreat function will return either False, meaning the computer should not retreat, or a location in which the computer should
	retreat its blocks to.
	'''
	attacking_copy = copy.deepcopy(attacking)
	defending_copy = copy.deepcopy(defending)
	attacking_rein_copy = copy.deepcopy(attacking_reinforcement)
	defending_rein_copy = copy.deepcopy(defending_reinforcement)

	simulation_dict = simulation(attacking_copy, defending_copy, 1000, attacking_reinforcement, defending_reinforcement, combat_letter, combat_round)
	win_percentage = 0
	#Calculate the win percentage based on if you are attacking or defending in the simulation
	if is_attacking:
		win_percentage = float(simulation_dict['attacker wins'])/1000
	else:
		win_percentage = float(simulation_dict['defender wins'])/1000

	retreat_constant = .3	
	#Insert code to check to see if it should retreat
	if win_percentage > retreat_constant:
		return False
	else:
	#Check to see where the blocks should retreat to
		current_location = find_location(attacking[0])
		possible_locations = []
		#Create list of possible locations to retreat to
		for x, border in enumerate(board.static_borders[current_location.regionID]):
			if is_attacking == False and attacking[0].allegiance != board.regions[x].blocks_present.allegiance and border != 'X':
				possible_locations.append(board.regions[x])
			elif is_attacking == True and defending[0].allegiance != board.regions[x].blocks_present.allegiance and border != 'X':
				possible_locations.append(board.regions[x])


		num = random.randint(0, len(possible_locations)-1)
		return possible_locations[num]

def print_situation(attack,defense):
	print('attack:')
	for block in attack:
		print(block.current_strength, end = ' ')
	print('\n')
	print('defense:')
	for block in defense:
		print(block.current_strength, end = ' ')
	print('\n')









