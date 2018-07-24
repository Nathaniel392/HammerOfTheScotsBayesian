import dice
import random
import blocks
import initialize_blocks
import copy

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

	if defending_blocks == []:
		return False
	dice_lst = dice.roll(attack_block_block.current_strength)




	for num in dice_lst:

		strong_blocks = find_max_strength(defending_blocks)

		if num <= attack_block_block.attack_number:
			block_to_get_hurt = strong_blocks[random.randint(0, len(strong_blocks) - 1)]
		  
			
			block_to_get_hurt.get_hurt(1)
			
			





def check_if_dead(attackers_lst, defenders_lst, attack_reinforcements, defense_reinforcements, eng_roster = list(), scot_roster = list()):
	"""
	checkers if attackers and defenders are alive
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
		elif block.is_dead():
			if block.allegiance == 'ENGLAND':
				eng_roster.append(attackers_lst.pop(i))
			else:
				scot_roster.append(attackers_lst.pop(i))
		
			
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
		
			

		if not block.is_dead():
			if block.allegiance == 'ENGLAND':
				eng_roster.append(defenders_lst.pop(i))
			else:
				scot_roster.append(defenders_lst.pop(i))
			defender_is_dead = False
	
	return attacker_is_dead, defender_is_dead
def battle(attack, defense, attack_reinforcements = list(), defense_reinforcements = list(), eng_roster = list(), scot_roster = list(), before_letter = 'A', before_number = 0, turn = 'defender'):
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






