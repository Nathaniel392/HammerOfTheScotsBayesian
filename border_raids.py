import board
import random
import blocks
import search
def border_raid(current_board, computer_role):
	"""
	does a border raid if necessayr
	else return false
	"""



	if len(current_board.regions[22].blocks_present) != 0 and current_board.regions[22].blocks_present[0].allegiance == 'SCOTLAND':



		english_non_nobles = list()
		for block in current_board.eng_roster:
			if type(block) == blocks.Noble and block.allegiance == 'ENGLAND':
				english_non_nobles.append(block)


		if len(english_non_nobles) == 0:
			print('no english non nobles to kill')
			return False


		if computer_role == 'SCOTLAND':
			print('ENGLAND is raided!')
			print('Which non_noble do you want to kill from the list below (type number)!')
			print('possible blocks to kill:')



			for i, block in enumerate(english_non_nobles):
				print(block.name, '[' + i + ']', end = ' ')

			bad_input = True
			while bad_input:
				try:

					option = int(input('>'))
				except ValueError:
					continue

				if option in range(len(english_non_nobles)):
					bad_input = False
					block_to_remove = english_non_nobles[option]
					current_board.eng_pool.append(current_board.remove_from_region(block_to_remove, \
						find_location(current_board, block_to_remove).regionID))
					print(block_to_move.name, 'got moved to pool')

		else:

			print('ENGLAND is raided')

			block_to_remove = random.randint(0, len(english_non_nobles) - 1)
			current_board.eng_pool.append(current_board.remove_from_region(block_to_remove, \
				find_location(current_board, block_to_remove).regionID))
			print(block_to_move.name, 'got moved to pool')





	else:
		return False

