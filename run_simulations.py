import simulations
import blocks
def main():


	finished = False
	first_time = True
	possible_answers = {'y', 'n'}
	attack_or_defense = ['attack', 'defense']
	index = 0
	attack = list()
	defense = list()
	'''
	while not finished:
		
		if not first_time:
			bad_input = True
			while bad_input:
				input1 = input('do you want to add more blocks (y) or (n): ')
				if input1 not in possible_answers:
					print('Type y or n')
				else:
					bad_input = False
					if input1 == 'n':
						finished = True

		if not finished:
			bad = True
			while bad:
				print('What strength block do you want to add to', attack_or_defense[index])
				strength = input('>')
				if strength.isdigit():
					bad = False
			bad = True
			while bad:
				print('What letter block you want to add to', attack_or_defense[index])
				letter = input('>')
				if letter.isalpha() and len(letter) == 1:
					bad = False
			bad = True
			while bad:
				print('What attack number do you want to add to', attack_or_defense[index])
				attack_number1 = input('>')
				if attack_number1.isdigit():
					bad = False
			new_block = blocks.Block(initial_attack_strength = int(strength), attack_letter = letter, attack_number = int(attack_number1))
			if index == 1:
				defense.append(new_block)
			else:
				attack.append(new_block)
		index = 1 - index

		if not first_time and not finished:
			bad_input = True
			while bad_input:
				input1 = input('do you want to add more blocks (y) or (n): ')
				bad_input = False
				if input1 not in possible_answers:
					print('Type y or n')
				else:
					if input1 == 'n':
						finished = True
		if not finished:
			bad = True
			while bad:
				print('What strength block do you want to add to', attack_or_defense[index])
				strength = input('>')
				if strength.isdigit():
					bad = False
			bad = True
			while bad:
				print('What letter block you want to add to', attack_or_defense[index])
				letter = input('>')
				if letter.isalpha() and len(letter) == 1:
					bad = False
			bad = True
			while bad:
				print('What attack number do you want to add to', attack_or_defense[index])
				attack_number1 = input('>')
				if attack_number1.isdigit():
					bad = False
			new_block = blocks.Block(initial_attack_strength = int(strength), attack_letter = letter, attack_number = int(attack_number1))
			

			if index == 1:
				defense.append(new_block)
			else:
				attack.append(new_block)
		index = 1 - index
		first_time = False
	'''

	attack = [blocks.Block(attack_number = 3, attack_letter = 'A', initial_attack_strength = 4)]
	defense = [blocks.Block(attack_number = 4, attack_letter = 'B', initial_attack_strength = 4)]
	bad_input = True
	while bad_input:
		try:
			num_times = int(input('How many times do you want to run this: '))
			bad_input = False
		except ValueError:
			print('type number')

	print('SIMULATION RUNNING')
	print(simulations.simulation(attack, defense, num_times))





if __name__ == '__main__':
	main()