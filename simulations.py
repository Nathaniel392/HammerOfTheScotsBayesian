import combat
import blocks
import copy
def battle(attack, defense, attack_reinforcements = list(), defense_reinforcements = list()):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	returns what happens


	TAKES NO INPUT



	'''

	# Divide each side into letter groups (dictionary)
	attackers = combat.organize(attack)
	defenders = combat.organize(defense)
	
	attacker_is_dead = False
	defender_is_dead = False

	#print_situation(attack, defense)
#run through the combat rounds
	for combat_round in range(3):

		if combat_round == 1:

			attack += attack_reinforcements
			defense += defense_reinforcements
			
			attackers = combat.organize(attack)
			defenders = combat.organize(defense)



		for letter in 'ABC':
			#defenders first
			for letter2 in defenders:
				if letter2 == letter:
					for attacking_block in defenders[letter2]:
						combat.attack_block(attacking_block, attack)
						#print_situation(attack, defense)
						attacker_is_dead, defender_is_dead = combat.check_if_dead(attack, defense)
					
						if attacker_is_dead:
							
							return 'defender wins'
						

			for letter2 in attackers:
				if letter2 == letter:
					for attacking_block in attackers[letter2]:
						combat.attack_block(attacking_block, defense)
						#print_situation(attack, defense)
						attacker_is_dead, defender_is_dead = combat.check_if_dead(attack, defense)
					
						if defender_is_dead:

							return 'attacker wins'

	return 'attacker retreats'

def simulation(attack, defense, num_times, attack_reinforcements = list(), defense_reinforcements = list()):
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


	


		totals_dict[battle(attack, defense, attack_reinforcements, defense_reinforcements)] += 1
	
		attack, defense = copy.deepcopy(original_attack), copy.deepcopy(original_defense)

		attack_reinforcements, defense_reinforcements = copy.deepcopy(original_attack_reinforcements), copy.deepcopy(original_defense_reinforcements)

	for situation in totals_dict:
		totals_dict[situation] /= num_times

	return totals_dict


	

def make_block_lists():
	"""
	makes blocks
	"""
	block_list1 = []
	block_list2 = []
	block_list1.append(blocks.Block(name = 'hi', attack_number = 2, attack_letter = 'A', initial_attack_strength = 4))
	block_list2.append(blocks.Block(name = 'hey', attack_number = 2, attack_letter = 'A', initial_attack_strength = 4))
	

	return block_list1, block_list2

def print_situation(attack, defense):
	"""
	for testing purposes
	prints health
	"""
	print('attackers:')
	for block in attack:
		print(block.current_strength, end = ' ')
	print('\n')
	print('defenders:')
	for block in defense:
		print(block.current_strength, end = ' ')
	print('\n')


def main():
	attack, defense = make_block_lists()
	attack_reinforcements2, defense_reinforcements = make_block_lists()
	print(simulation(attack,defense, 1000, attack_reinforcements = attack_reinforcements2 ))
main()