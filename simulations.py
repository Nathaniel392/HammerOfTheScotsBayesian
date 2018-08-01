
import blocks
import copy
import random
import dice
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

def attack_block(attack_block_block, defending_blocks):
	"""
	attacks blocks
	uses random in case where everyone same health
	attack_block_block is the block attacking
	defending_blocks is the list of all defending blocks to be attacked
	"""

	if defending_blocks == []:
		return False
	dice_lst = dice.roll(attack_block_block.current_strength)
	



	for num in dice_lst:

		strong_blocks = find_max_strength(defending_blocks)

		if num <= attack_block_block.attack_number:
			block_to_get_hurt = strong_blocks[random.randint(0, len(strong_blocks) - 1)]
		  	

			block_to_get_hurt.get_hurt(1)
			

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
									if attacking_block.name == 'WALES-ARCHER' or attacking_block.name == 'WALES-INFANTRY' or attacking_block.name == 'ULSTER':
										if random.randint(0,2) == 0:
											attacking_block.current_strength = 0

									attack_block(attacking_block, attack)



					
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements)
							
									if (attacker_is_dead and combat_round != 0) or (attacker_is_dead and attack_reinforcements == []):
										
										return 'defender wins'
								
					if not turn_found and 'attacker' != turn:
						pass
					else:
						turn_found = True
						for letter2 in attackers:
							if letter2 == letter:
								for attacking_block in attackers[letter2]:
									if attacking_block.name == 'WALES-ARCHER' or attacking_block.name == 'WALES-INFANTRY' or attacking_block.name == 'ULSTER':
										if random.randint(0,2) == 0:
											attacking_block.current_strength = 0

									attack_block(attacking_block, defense)

				
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements)
			
									if (defender_is_dead and combat_round != 0) or (defender_is_dead and defense_reinforcements == []):

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
			if type(element) == tuple:
				attack[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)


		for i, element in enumerate(defense):
			if type(element) == tuple:
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












