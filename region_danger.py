import board

def table(current_board):
	'''
	This function creates a table which stores the number of 
	enemy strength points that are within 1 movement of each region
	on the board. The table is arranged by region ID
	'''
	danger_values = list()

	for i,region in enumerate(current_board.regions):

		danger_num = 0

		for j,other_region in enumerate(current_board.regions):

			for block in other_region.blocks_present:

				if block.allegiance != region.blocks_present[0].allegiance and current_board.checkpath(block.movement_points, y, x):

					danger_num += block.current_strength

		danger_values.append(danger_num)

	return danger_values
