def make_attacked_borders():
	"""
	makes attacked borders
	set them all to False
	"""
	attacked_borders = list()
	for i in range(23):
		attacked_borders.append(list())
		for j in range(23):
			attacked_borders[i].append(False)
	return attacked_borders

def reset_attacked_borders(attacked_borders):
	"""
	resets all attacked borders to False
	"""
	for i in range(23):
		for j in range(23):
			attacked_borders[i][j] = False
	
