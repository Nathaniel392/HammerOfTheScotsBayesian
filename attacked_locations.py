def make_attacked_locations():
	attacked_locations = list()
	for i in range(23):
		for j in range(23):
			attacked_locations.append(False)
	return attacked_locations