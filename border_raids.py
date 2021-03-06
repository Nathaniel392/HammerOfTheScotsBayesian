import board
import random
import blocks
import search

def find_location(board, blok):
	'''
	This function takes a board object and the name of a block
	and returns a region object where the block is
	'''

	
	for region in board.regions:
		for bllock in region.blocks_present:
			
			if bllock.name == blok.name:
				return region
	

	print('CANNOT FIND BLOCK WITH BLOCK NAME', blok.name)
	raise Exception('cannot find block')
def border_raid(current_board, eng_type, scot_type):
	"""
	does a border raid if necessayr
	else return false
	"""



	if len(current_board.regions[22].blocks_present) != 0 and current_board.regions[22].blocks_present[0].allegiance == 'SCOTLAND':



		english_non_nobles = list()
		for block in current_board.eng_roster:
			if type(block) != blocks.Noble and block.allegiance == 'ENGLAND':
				english_non_nobles.append(block)


		if len(english_non_nobles) == 0:
			print('no english non nobles to kill')
			return False


		if scot_type == 'comp':
			print('ENGLAND is raided!')
			print('Which non_noble do you want to kill from the list below (type number)!')
			print('possible blocks to kill:')



			for i, block in enumerate(english_non_nobles):
				print(block.name, '[' + str(i) + ']', end = ' ')

			for x in range(len(english_non_nobles)):
				option = x
				break

			bad_input = False
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
					print(block_to_remove.name, 'got moved to pool')

		else:

			print('ENGLAND is raided')

			block_to_remove_index = random.randint(0, len(english_non_nobles) - 1)
			block_to_remove = english_non_nobles[block_to_remove_index]
			current_board.eng_pool.append(current_board.remove_from_region(block_to_remove, \
				find_location(current_board, block_to_remove).regionID))
			print(block_to_remove.name, 'got moved to pool')





	else:
		return False

