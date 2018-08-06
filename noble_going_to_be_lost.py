import search

def noble_going_to_be_lost(board, noble_object, role, turn):
	"""
	returns float
	1.0 means better chances of being lost
	0.0 means lower chances of being lost
	very arbitrary numbers
	not very good indication
	"""

	close_to_winter = .2 * turn
	lost_flt = 0.0
	if type(noble_object.home_location) == int:
		home_location_tuple = (noble_object.home_location,)
	else:
		home_location_tuple = noble_object.home_location

	#checking who occupies it
	for home_location_id in home_location_tuple:
		if board.regions[home_location_id].is_enemy(role):
			lost_flt += 0.7
		elif board.regions[home_location_id].is_friendly(role):
			lost_flt += 0.03
		else:
			lost_flt += 0.2

		#checking who is around the noble_home_location
		current_location = find_location(board, noble_object)
		for regionID, border in enumerate(board.dynamic_borders[current_location.regionID]):
			if border != 0:
				if board.regions[regionID].is_enemy(role):
					lost_flt += 0.3
				elif board.regions[regionID].is_friendly(role):
					lost_flt += .01
				else:
					lost_flt += .07

	return lost_flt * close_to_winter
def noble_going_to_be_kept(board, noble_object, turn, role):
	"""
	returns between 0.0 and 1.0
	1.0 more likely to be kept
	"""
	return (1 - noble_going_to_be_lost(board, noble_object, turn, role))

def noble_not_going_to_be_occupied(board, noble_object, turn, role):
	"""
	returns between 0.0 and 1.0
	1.0 home locatino more likely to be not occupied
	"""
	lost_flt = 0.0
	close_to_winter = .2 * turn
	if type(noble_object.home_location) == int:
		home_location_tuple = (noble_object.home_location, )
	else:
		home_location_tuple = noble_object.home_location

	#checking who occupies it
	for home_location_id in home_location_tuple:
		if board.regions[home_location_id].is_enemy(role):
			lost_flt += 0.05
		elif board.regions[home_location_id].is_friendly(role):
			lost_flt += 0.05
		else:
			lost_flt += 0.7

		#checking who is around the noble_home_location
		current_location = find_location(board, noble_object)
		for regionID, border in enumerate(board.dynamic_borders[current_location.regionID]):
			if border != 0:
				if board.regions[regionID].is_enemy(role):
					lost_flt += 0.13
				elif board.regions[regionID].is_friendly(role):
					lost_flt += 0.13
				else:
					lost_flt += 0.3
	return lost_flt * close_to_winter

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
		value_lst[i] = value_lst[i] / 60
		if value_lst[i] < 0:
			value_lst[i] = 0
	#print('VALUE ' + str(value_lst[regionID]))
	return value_lst[regionID]



