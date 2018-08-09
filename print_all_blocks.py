import update_roster
def print_all_blocks(current_board):
	print('ENGLISH ROSTER:\n\n')
	for block in current_board.eng_roster:
		print(block.name, update_roster.find_location(current_board, block).name)
	print()
	print('SCOTTISH ROSTER:\n\n')
	for block in current_board.scot_roster:
		print(block.name, update_roster.find_location(current_board, block).name)
	print()
	print('ENGLISH POOL:\n\n')
	for block in current_board.eng_pool:
		print(block.name)
	print()
	print('SCOTTISH POOL:\n\n')
	for block in current_board.scot_pool:
		print(block.name)