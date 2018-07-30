def make_attacked_borders():
	attacked_borders = list()
	for i in range(23):
		for j in range(23):
			attacked_borders.append(False)
	return attacked_borders

def reset_attacked_borders(attacked_borders):
	for i in range(23):
		for j in range(23):
			attacked_borders[i][j] = False
	
