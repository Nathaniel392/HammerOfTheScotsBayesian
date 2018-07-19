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
	returns blocks with max strength
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
		if block.current_strength == max_strength
			strong_blocks.append(block)
	return strong_blocks

def battle(attack, defense):
	'''
	Manages combat
	attack:  list of attacking blocks
	defense:  list of defending blocks
	'''

	# Divide each side into letter groups (dictionary)
	attackers = organize(attack)
	defenders = organize(defense)

	


	# Loop for 3 combat rounds
	for combat_round in range(3):
		combat_round += 1

		for round in 'ABC':
			for block in attackers:
				if block.attack_letter == round:
					dice_roll_lst = list(dice.roll(block.current_strength))
					for num in dice_roll_list:
						if num <= block.attack_number:
							strong_blocks = find_max_strength(defenders)
							strong_blocks[0].get_hurt(1)
							for block in defenders:
								if block.current_strength == 0:
									;alsdkfj;alsdjkf;laksjdf;lkasdjfl;kajsd;flkasjdkf

		# End of combat
		if combat_round == 3:

			#Check if any defenders remain
			if success(defense):





def main():
	battle([], [])


if __name__ == '__main__':
	main()
