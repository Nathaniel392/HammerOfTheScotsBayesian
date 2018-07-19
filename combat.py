import dice
import random
import blocks
import initialize_blocks
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
	"""
	dice_lst = dice.roll(attack_block_block.current_strength)
	for num in dice_lst:
		strong_blocks = find_max_strength(defending_blocks)

		if num <= attack_block_block.attack_number:
			strong_blocks[random.randint(0, len(strong_blocks) - 1)].get_hurt(1)

	#dice_lst = list()


def check_if_dead(attackers_lst, defenders_lst):
	"""
	checkers if attackers and defenders are alive
	"""
	attacker_is_dead = True
	defender_is_dead = True
	for block in attackers_lst:
		if block.current_strength != 0:
			attacker_is_dead = False

	for block in defenders_lst:
		if block.current_strength != 0:
			defender_is_dead = False

	return attacker_is_dead, defender_is_dead
def battle(attack, defense):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	'''

	# Divide each side into letter groups (dictionary)
	attackers = organize(attack)
	defenders = organize(defense)
	
	attacker_is_dead = False
	defender_is_dead = False

	

	for combat_round in range(3):
		for letter in 'ABC':
			for letter2 in defenders:
				if letter2 == letter:
					for attacking_block in defenders[letter2]:
						attack_block(attacking_block, attack)
						
						attacker_is_dead, defender_is_dead = check_if_dead(attack, defense)
						
						if attacker_is_dead or defender_is_dead:
							break
			for letter2 in attackers:
				if letter2 == letter:
					for attacking_block in attackers[letter2]:
						attack_block(attacking_block, defense)
						
						attacker_is_dead, defender_is_dead = check_if_dead(attack, defense)

						if attacker_is_dead or defender_is_dead:
							break

	if attacker_is_dead:
		print('defender wins')
	elif defender_is_dead:
		print('attacker wins')
	else:
		print('attacker retreats')

def make_lists(num1, num2 = None, num3 = None, num4 = None):
	nobles, non_nobles, static_nobles, static_blocks = initialize_blocks.initialize_blocks()
	if num2 == None:
		return [non_nobles[num1]]
	if num3 == None:
		return [non_nobles[num1], nobles[num2]]
	if num4 == None:
		return [non_nobles[num1], nobles[num2], nobles[num3]]
	else:
		return [non_nobles[num1], nobles[num2], nobles[num3], nobles[num4]]


battle(make_lists(0, 6), make_lists(1, 9))

		
				

	






