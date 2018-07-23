import dice
import random
import blocks
import initialize_blocks
import copy
import board
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




def check_if_dead(attackers_lst, defenders_lst):
	"""
	checkers if attackers and defenders are alive
	"""
	attacker_is_dead = True
	defender_is_dead = True
	for block in attackers_lst:
		if (type(block) == blocks.Edward or type(block) == blocks.Edward2 or type(block) == blocks.ScottishKing) and block.is_dead():
			return True, False
		elif type(block) == blocks.Noble and block.is_dead():
			block.change_allegiance()
		if not block.is_dead():
			attacker_is_dead = False

	for block in defenders_lst:
		if (type(block) == blocks.Edward or type(block) == blocks.Edward2 or type(block) == blocks.ScottishKing) and block.is_dead():
			return False, True
		elif type(block) == blocks.Noble and block.is_dead():
			
			block.change_allegiance()
			

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

	#print_situation(attack, defense)
#run through the combat rounds
	for combat_round in range(3):
		if not number_found and combat_round != before_number:
	
			pass
		else:
			number_found = True

			if combat_round >= 1:

				for i, block in enumerate(attack):
					if block.allegiance != attackers_allegiance:
						defense_reinforcements.append(attack.pop(i))
				for i, block in enumerate(defense):
			 		if block.allegiance != defenders_allegiance:
			 			attack_reinforcements.append(defense.pop(i))


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
									if type(attacking_block) == blocks.Celtic:
										attacking_block.check_loyalty()

									attack_block(attacking_block, attack)

								


									#print_situation(attack, defense)
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense)
								
									if attacker_is_dead and combat_round != 0:
										
										return 'defender wins'
								
					if not turn_found and 'attacker' != turn:
						pass
					else:
						turn_found = True
						for letter2 in attackers:
							if letter2 == letter:
								for attacking_block in attackers[letter2]:
									if type(attacking_block) == blocks.Celtic:
										attacking_block.check_loyalty()

									attack_block(attacking_block, defense)
									#print_situation(attack, defense)
									attacker_is_dead, defender_is_dead = check_if_dead(attack, defense)
								
									if defender_is_dead and combat_round != 0:

										return 'attacker wins'

	return 'attacker retreats'

	def update_roster(attack,defense, current_board):
		"""
		updates allegiance roster after a battle
		receives attacking and defending blocks as lists
		"""
		pass





