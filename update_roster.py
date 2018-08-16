import blocks
import board
import attacked_borders
def find_location(board, blok):
	for region in board.regions:
		for bllock in region.blocks_present:
			if bllock.name == blok.name:
				return region
	return False

	
def update_roster(all_blocks_lst = None, current_board = None):
	"""
	updates allegiance roster after a battle
	updates dead pool too
	receives attacking and defending blocks as lists
	"""
	all_blocks_lst = current_board.scot_roster + current_board.eng_roster
	for block in all_blocks_lst:
		

		try:
			if block.checked:
				block.checked = False
		except AttributeError:
			pass

		try:	
			if type(block) == blocks.Noble:

				if block.has_cross and block.is_dead():
			
					
					current_board.scot_roster.remove(block)

					current_board.remove_from_region(block, find_location(current_board,block).regionID)
					
				else:


					block.b2_to_b3(2)
					if block.allegiance == 'SCOTLAND':
						#if block.allegiace is SCOTLAND and can't find it then put it from the english one and into the scotland one for nobles
						block_found_bool = False
						for block2 in current_board.scot_roster:
							if block is block2:
								block_found_bool = True
								break

						if not block_found_bool:
							for i, block2 in enumerate(current_board.eng_roster):
								if block is block2:
									current_board.scot_roster.append(current_board.eng_roster.pop(i))

									break
					elif block.allegiance == 'ENGLAND':
						block_found_bool = False
						for block2 in current_board.eng_roster:
							if block is block2:
								block_found_bool = True
								break
						if not block_found_bool:
							for i, block2 in enumerate(current_board.scot_roster):
								if block is block2:
									current_board.eng_roster.append(current_board.scot_roster.pop(i))
									break
			elif block.is_dead() and not block.has_cross and (block in current_board.eng_roster or block in current_board.scot_roster):	
				#print(block.name, ' is dead and we are looking for him')
				if block.allegiance == 'SCOTLAND':
					
					if find_location(current_board, block):
						current_board.scot_pool.append(current_board.remove_from_region(block, \
							find_location(current_board, block).regionID))
					elif block not in current_board.scot_pool:
						current_board.scot_pool.append(block)
					if block in current_board.scot_roster:
						current_board.scot_roster.remove(block)

				elif block.allegiance == 'ENGLAND':
					if find_location(current_board, block):
						current_board.eng_pool.append(current_board.remove_from_region(block, \
							find_location(current_board, block).regionID))
					elif block not in current_board.eng_pool:
						current_board.eng_pool.append(block)
					if block in current_board.eng_roster:
						current_board.eng_roster.remove(block)

			elif block.is_dead() and block.has_cross:

				if block.type == 'EDWARD':
					block.type = 'KING'
					current_board.eng_pool.append(current_board.remove_from_region(block, \
						find_location(current_board, block).regionID))
					current_board.eng_roster.remove(block)

				else:
					if find_location(current_board, block):
						current_board.remove_from_region(block, find_location(current_board, block).regionID)
					if block.allegiance == 'ENGLAND':
						current_board.eng_roster.remove(block)
					elif block.allegiance == 'SCOTLAND':
						current_board.scot_roster.remove(block)
		except AttributeError:
			#someone not found because they're dead or something or ghost idk 
			continue


	
	current_board.reset_borders()

	for region in current_board.regions:
		if not region.is_contested():

			region.combat_dict = {'Attacking': [], 'Defending': [], 'Attacking Reinforcements': [], 'Defending Reinforcements': []}
		else:
			current_board.reset_attacked_borders()



	return current_board


