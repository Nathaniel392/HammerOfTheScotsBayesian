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
											attack_block.current_strength = 0

									combat.attack_block(attacking_block, attack)

								


									#print_situation(attack, defense)
									attacker_is_dead, defender_is_dead = combat.check_if_dead(attack, defense)
								
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
											attack_block.current_strength = 0

									combat.attack_block(attacking_block, defense)
									#print_situation(attack, defense)
									attacker_is_dead, defender_is_dead = combat.check_if_dead(attack, defense)
								
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
				attack[i] = pick_random_block(element)
		for i, element in enumerate(defense):
			if len(element) != 1:
				attack[i] = pick_random_block(element)


		totals_dict[battle(attack, defense, attack_reinforcements, defense_reinforcements, before_letter, before_number, turn)] += 1
	
		attack, defense = copy.deepcopy(original_attack), copy.deepcopy(original_defense)

		attack_reinforcements, defense_reinforcements = copy.deepcopy(original_attack_reinforcements), copy.deepcopy(original_defense_reinforcements)

	for situation in totals_dict:
		totals_dict[situation] /= num_times

	return totals_dict


def pick_random_block(block_tuple):
	"""
	if multiple blocks unkonwn
	send all possible blocks in tuple
	then it will pick a random one
	"""
	return block_tuple[random.randint(0, len(block_tuple) - 1)]



