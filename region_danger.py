import board

def table(current_board, role):
	'''
	This function creates a table which stores the number of 
	enemy strength points that are within 1 movement of each region
	on the board. The table is arranged by region ID.
	The parameter role is the side in which the computer is playing.
	If the region is not controlled by the computer then its danger value
	is -1
	'''
	danger_values = list()
	role = role.upper()
	for i,region in enumerate(current_board.regions):

		danger_num = 0
		if role == region.blocks_present[0].allegiance and role == region.blocks_present[len(region.blocks_present-1)].allegiance:
			for j,other_region in enumerate(current_board.regions):

				for block in other_region.blocks_present:

					if block.allegiance != region.blocks_present[0].allegiance and current_board.checkpath(block.movement_points, y, x):

						danger_num += block.current_strength

			danger_values.append(danger_num)
			
		else:

			danger_values.append(-1)

	return danger_values
