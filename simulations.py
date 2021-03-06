
import blocks
import copy
import random
import dice
import math
import search
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


	indexes_to_pop = list()

	
	for i, block in enumerate(attackers_lst):
	

		if block.type == 'KING' and block.is_dead():

			return True, False
		elif block.has_cross and block.is_dead():

			


			
			
			indexes_to_pop.append(i)
	
				
		
		elif type(block) == blocks.Noble and block.is_dead():


			block.change_allegiance()
			
			defense_reinforcements.append(attackers_lst[i])
			indexes_to_pop.append(i)

			
		elif type(block) != blocks.Noble and block.is_dead():

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
	
			return False, True

		elif block.has_cross and block.is_dead():

	
	
				
			indexes_to_pop.append(i)
			

		elif type(block) == blocks.Noble and block.is_dead():
			
			block.change_allegiance()

			attack_reinforcements.append(defenders_lst[i])
			indexes_to_pop.append(i)

		
		elif type(block) != blocks.Noble and block.is_dead():


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

def battle(attack, defense, attack_reinforcements = list(), defense_reinforcements = list(), before_letter = 'A', before_number = 0, turn = 'defender'):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	returns what happens


	TAKES NO INPUT



	'''

	if len(attack) < 0 or len(defense) < 0:

		attack += attack_reinforcements
		defense += defense_reinforcements


	# Divide each side into letter groups (dictionary)

	if attack == list():
		attack = attack_reinforcements
		attack_reinforcements = list()
	elif defense == list():
		defense = defense_reinforcements
		defense_reinforcements = list()
		
	letter_found = False
	number_found = False
	turn_found = False


	attackers = organize(attack)
	defenders = organize(defense)

	if len(attack) < 0 or len(defense) < 0:

		attack += attack_reinforcements
		defense += defense_reinforcements



	attackers_allegiance = attack[0].allegiance
	defenders_allegiance = defense[0].allegiance
	
	attacker_is_dead = False
	defender_is_dead = False


#run through the combat rounds

	for combat_round in range(3):


		if not number_found and combat_round != before_number:
	
			pass
		else:
			for block in attack + defense:
				try:
					if block.checked:
						pass
				except AttributeError:
					if block.name == 'ULSTER' or block.name == 'WALES-INFANTRY' or block.name == 'WALES-ARCHER':
						loyalty = random.randint(1, 6)
						
						if loyalty in range(1, 5):
							pass
						else:
							
							block.checked = True
							block.current_strength = 0
							if block in attack:
								attack.remove(block)
							else:
								defense.remove(block)
					
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
									if attack == list():
										break
									

									attack_block(attacking_block, attack)



					
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements)
							
									if (attacker_is_dead and combat_round != 0) or (attacker_is_dead and attack_reinforcements == []):
										
							
										
										
										return 'defender wins'
									if (defender_is_dead and combat_round != 0) or (defender_is_dead and defense_reinforcements == []):
									
										
										
										return 'attacker wins'
								
					if not turn_found and 'attacker' != turn:
						pass
					else:
						turn_found = True
						for letter2 in attackers:
							if letter2 == letter:
								for attacking_block in attackers[letter2]:
									

									attack_block(attacking_block, defense)

				
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense, attack_reinforcements, defense_reinforcements)
			
									if (attacker_is_dead and combat_round != 0) or (attacker_is_dead and attack_reinforcements == []):
										
							
										
										
										return 'defender wins'
									if (defender_is_dead and combat_round != 0) or (defender_is_dead and defense_reinforcements == []):
									
										
										
										return 'attacker wins'

	return 'attacker retreats'
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

def using_weights_find_tuple(prob_dict, rounding = 1000):
	"""
	prob_dict: value is blocks (set), key is probability (tuple)
	rounding is how much one will round(max number of blocks to pick from)
	picks random blocks based on weights
	"""
	if len(prob_dict) == 0:
		raise Exception('nothing in probability dictionary')

	if len(prob_dict) == 1:
		return (prob_dict[0])
	weight_lst = list()

	#find probabilites
	for prob in prob_dict:
		weight_lst.append(int(rounding * prob))

	#reduce fractions




	prev_gcd = math.gcd(weight_lst[0], weight_lst[1])

	for i in range(2, len(weight_lst)):
		prev_gcd = math.gcd(prev_gcd, weight_lst[i])

	

	block_lst = list()

	for weight, block_set in prob_dict.items():
		for block in block_set:


			for j in range(int((weight * rounding) // prev_gcd)):
				block_lst.append(block)


	return tuple(block_lst)








	
def simulation(attack, defense, num_times, attack_reinforcements = list(), defense_reinforcements = list(), before_letter = 'A', before_number = 0, turn = 'defender', rounding = 100):
	"""
	attack is list of attacking blocks
	defense is list of defending blocks
	num_times is number of simulations
	returns dictionary with estimated probabilities
	"""

	# print('**************************************')
	# print('-ATTACK-')
	# for i in attack:
	# 	print(i.name, i.allegiance)
	# print('**************************************')

	# print('**************************************')
	# print('-DEFEND-')
	# for i in defense:
	# 	print(i.name, i.allegiance)
	# print('**************************************')

	# print('**************************************')
	# print('-ATTACK R-')
	# for i in attack_reinforcements:
	# 	print(i.name, i.allegiance)
	# print('**************************************')

	# print('**************************************')
	# print('-DEFEND R-')
	# for i in defense_reinforcements:
	# 	print(i.name, i.allegiance)
	# print('**************************************')


	#temporary
	

	original_attack = copy.deepcopy(attack)
	original_defense = copy.deepcopy(defense)
	original_attack_reinforcements = copy.deepcopy(attack_reinforcements)
	original_defense_reinforcements = copy.deepcopy(defense_reinforcements)

	before_attack_strength = 0
	before_defense_strength = 0

	for block in original_attack + original_attack_reinforcements:
		before_attack_strength += block.current_strength
	for block in original_defense + original_defense_reinforcements:
		before_defense_strength += block.current_strength

	totals_dict = {'attacker wins':0, 'defender wins':0, 'attacker retreats':0, 'Attacker strength lost':0, 'Defender strength lost':0}

	if original_attack == list() or original_defense == list():
		return {'attacker wins': .25, 'defender wins': .25, 'attacker retreats': .5, 'Attacker strength lost': 1.0, 'Defender strength lost': 1.0}
	count = 0
	for j in range(num_times):


		attack = copy.deepcopy(original_attack)
		defense = copy.deepcopy(original_defense)
		attack_reinforcements = copy.deepcopy(original_attack_reinforcements)
		defense_reinforcements = copy.deepcopy(original_defense_reinforcements)
	
		if not(attack) and not attack_reinforcements:
			return totals_dict


		for i, element in enumerate(attack):
			if type(element) == tuple:
				attack[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)
			elif type(element) == dict:
				attack[i] = using_weights_find_tuple(element, rounding)
				attack[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)


		for i, element in enumerate(defense):
			if type(element) == tuple:
				defense[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)
			elif type(element) == dict:
				defense[i] = using_weights_find_tuple(element, rounding)
				defense[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)

		for i, element in enumerate(attack_reinforcements):
			if type(element) == tuple:
				attack_reinforcements[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)
			elif type(element) == dict:
				attack_reinforcements[i] = using_weights_find_tuple(element, rounding)
				attack_reinforcements[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)


		for i, element in enumerate(defense_reinforcements):
			if type(element) == tuple:
				defense_reinforcements[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)
			elif type(element) == dict:
				defense_reinforcements[i] = using_weights_find_tuple(element, rounding)
				defense_reinforcements[i] = pick_random_block(element, attack, defense, attack_reinforcements, defense_reinforcements)

		battle_result = battle(attack, defense, attack_reinforcements, defense_reinforcements, before_letter, before_number, turn)

		totals_dict[battle_result] += 1

		after_attack_strength = 0
		after_defense_strength = 0
		for block in attack + attack_reinforcements:
			after_attack_strength += block.current_strength
		for block in defense + defense_reinforcements:
			after_defense_strength += block.current_strength

		totals_dict['Attacker strength lost'] += before_attack_strength - after_attack_strength
		totals_dict['Defender strength lost'] += before_defense_strength - after_defense_strength
	
		attack, defense = copy.deepcopy(original_attack), copy.deepcopy(original_defense)

		attack_reinforcements, defense_reinforcements = copy.deepcopy(original_attack_reinforcements), copy.deepcopy(original_defense_reinforcements)

	for situation in totals_dict:
		totals_dict[situation] /= num_times

	#print(totals_dict)

	return totals_dict















