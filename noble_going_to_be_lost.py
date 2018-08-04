import search

def noble_going_to_be_lost(board, noble_object, turn):
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
		home_location_tuple = (noble_object.home_location, )
	else:
		home_location_tuple = noble.object.home_location

	#checking who occupies it
	for home_location_id in home_location_tuple:
		if current_board.regions[home_location_id].is_enemy():
			lost_flt += 0.7
		elif current_board.regions[home_location_id].is_friendly():
			lost_flt += 0.03
		else:
			lost_flt += 0.2

		#checking who is around the noble_home_location

		for regionID, border in enumerate(board.dynamic_borders[current_location.regionID]):
			if border != 0:
				if board.regions[regionID].is_enemy():
					lost_flt += 0.3
				elif board.regions[regionID].is_friendly():
					lost_flt += .01
				else:
					lost_flt += .07

	return lost_flt * close_to_winter
def noble_going_to_be_kept(board, noble_object, turn):
	"""
	returns between 0.0 and 1.0
	1.0 more likely to be kept
	"""
	return (1 - noble_going_to_be_lost(board, noble_object, turn))

def noble_not_going_to_be_occupied(board, noble_object, turn):
	"""
	returns between 0.0 and 1.0
	1.0 home locatino more likely to be not occupied
	"""
	lost_flt = 0.0
	if type(noble_object.home_location) == int:
		home_location_tuple = (noble_object.home_location, )
	else:
		home_location_tuple = noble.object.home_location

	#checking who occupies it
	for home_location_id in home_location_tuple:
		if current_board.regions[home_location_id].is_enemy():
			lost_flt += 0.05
		elif current_board.regions[home_location_id].is_friendly():
			lost_flt += 0.05
		else:
			lost_flt += 0.7

		#checking who is around the noble_home_location

		for regionID, border in enumerate(board.dynamic_borders[current_location.regionID]):
			if border != 0:
				if board.regions[regionID].is_enemy():
					lost_flt += 0.13
				elif board.regions[regionID].is_friendly():
					lost_flt += 0.13
				else:
					lost_flt += 0.3
	return lost_flt * close_to_winter



