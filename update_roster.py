import blocks
import board

def update_roster(all_blocks_lst, current_board):
	"""
	updates allegiance roster after a battle
	updates dead pool too
	receives attacking and defending blocks as lists
	"""
	
	for block in all_blocks_lst:
		
		if block.is_dead() and not block.has_cross:	
			if block.allegiance == 'SCOTLAND':
				current_board.scot_roster.append(current_board.remove_from_region(block, \
					find_location(current_board, block).regionID))
			elif block.allegiance == 'ENGLAND':
				current_board.eng_roster.append(current_board.remove_from_region(block, \
					find_location(current_board, block).regionID))
		elif block.is_dead() and block.has_cross:
			if block.type == 'EDWARD':
				block.type = 'KING'
				current_board.eng_roster.append(current_board.remove_from_region(lock, \
					find_location(current_board, block).regionID))
			else:

				current_board.remove_from_region(block, find_location(current_board, block).regionID)


		if block.allegiance == 'SCOTLAND':
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
						current_board.scot_roster.append(current_board.scot_roster.pop(i))
						break
