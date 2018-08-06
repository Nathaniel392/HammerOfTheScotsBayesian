import blocks
import search

def regroup(board, regionID, locations):

	return_dict = {}

	role = board.regions[regionID].blocks_present[0].allegiance

	for location in locations:

		location_utility = 0

		if len(board.regions[location].blocks_present) == 0 and noble_home_to_object(board, location) and noble_homt_to_object(board, location).allegiance != role:
			location_utility += value_of_location(board, location, role) * 3

		elif len(board.regions[location].blocks_present) == 0 and noble_home_to_object(board, location):
			location_utility += value_of_location(board, location, role) * 2

		elif len(board.regions[location].blocks_present) == 0:
			location_utility += value_of_location(board, location, role) * 1.4

		else:
			location_utility += value_of_location(board, location, role)

		return_dict[location] = location_utility
		
	return return_dict








def noble_home_to_object(board, regionID):
	'''
	This function is meant to change a region based on its ID to the
	object of its noble in which the region is the home to.
	It return a noble block object
	'''
	if regionID == 0:

		return search.block_name_to_object(board.all_blocks, 'ROSS')

	elif regionID == 2:

		return search.block_name_to_object(board.all_blocks, 'MORAY')

	elif regionID == 4:

		return search.block_name_to_object(board.all_blocks, 'BUCHAN')

	elif regionID == 5:

		return search.block_name_to_object(board.all_blocks, 'COMYN')

	elif regionID == 6:

		return search.block_name_to_object(board.all_blocks, 'COMYN')

	elif regionID == 7:

		return serach.block_name_to_object(board.all_blocks, 'MAR')

	elif regionID == 8:

		return search.block_name_to_object(board.all_blocks, 'ANGUS')

	elif regionID == 9:

		return search.block_name_to_object(board.all_blocks, 'ARGYLL')

	elif regionID == 10:

		return search.block_name_to_object(board.all_blocks, 'ATHOLL')

	elif regionID == 12:

		return search.block_name_to_object(board.all_blocks, 'LENNOX')

	elif regionID == 13:

		return search.block_name_to_object(board.all_blocks, 'MENTIETH')

	elif regionID == 14:

		return search.block_name_to_object(board.all_blocks, 'CARRICK')

	elif regionID == 15:

		return search.block_name_to_object(board.all_blocks, 'STEWARD')

	elif regionID == 17:

		return search.block_name_to_object(board.all_blocks, 'DUNBAR')

	elif regionID == 19:

		return search.block_name_to_object(board.all_blocks, 'GALLOWAY')

	elif regionID == 20:

		return search.block_name_to_object(board.all_blocks, 'BRUCE')
	return False
