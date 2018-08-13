import blocks
import search
import weighted_prob
import region_danger

def regroup_utility(board, regionID, locations):

	return_dict = {}

	role = board.regions[regionID].blocks_present[0].allegiance

	for location in locations:

		location_utility = 0

		if len(board.regions[location].blocks_present) == 0 and noble_home_to_object(board, location) and noble_home_to_object(board, location).allegiance != role:
			location_utility += value_of_location(board, location, role) * 3

		elif len(board.regions[location].blocks_present) == 0 and noble_home_to_object(board, location):
			location_utility += value_of_location(board, location, role) * 2

		elif noble_home_to_object(board, location) and location == regionID:
			location_utility += value_of_location(board, location, role) * 1.8

		elif len(board.regions[location].blocks_present) == 0:
			location_utility += value_of_location(board, location, role) * 1.4

		else:
			location_utility += value_of_location(board, location, role)

		return_dict[location] = location_utility

	print(return_dict)

	return_value = weighted_prob.weighted_prob(return_dict)

	return int(return_value)








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

		return search.block_name_to_object(board.all_blocks, 'MAR')

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


def value_of_location(current_board, regionID, role):
	"""
	returns float between 0.0 and 1.0
	ROSS            0  F T 1
GARMORAN        1  F T 0
MORAY           2  F T 2
STRATHSPEY      3  T T 1 
BUCHAN          4  F T 2
LOCHABER        5  F T 1 
BADENOCH        6  F F 2
MAR             7  F F 1
ANGUS           8  F T 2
ARGYLL          9  F T 2
ATHOLL          10 F F 1
FIFE            11 T T 2
LENNOX          12 T T 1 
MENTIETH        13 F T 3
CARRICK         14 F T 1
LANARK          15 F F 2
LOTHIAN         16 F T 2
DUNBAR          17 F T 2
SELKIRK-FOREST  18 F F 0
GALLOWAY        19 F T 1
ANNAN           20 F T 2
TEVIOT          21 F F 1
ENGLAND         22 F T 0
	"""
	enemy_strength_lst = region_danger.table(current_board, role)
	value_lst = [22, 5, 14, 10, 30, 11, 15, 18, 37, 17, 21, 42, 27, 50, 11, 26, 13, 17, 5, 19, 15, 12, 11]

	for i, number in enumerate(enemy_strength_lst):
		if number != -1:
			value_lst[i] -= number
		value_lst[i] = value_lst[i] / 50
		if value_lst[i] <= 0:
			value_lst[i] = 0.0000001

	return value_lst[regionID]
