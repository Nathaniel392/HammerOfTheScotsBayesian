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
			pass

		# End of combat
		if combat_round == 3:

			#Check if any defenders remain
			if success(defense):





def main():
	battle([], [])


if __name__ == '__main__':
	main()