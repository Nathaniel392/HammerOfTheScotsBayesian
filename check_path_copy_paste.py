def check_path(self, num_moves, startID, endID, role, path=[], stop=False, all_paths=[]):
		'''
		Finds all legal paths between two regions
		num_moves:  a block's movement points (int)
		startID:  regionID of the starting region (int)
		endID:  regionID of the ending region (int)
		path:  temporary stored path for the recursive function - keeps track of where it's been
		stop:  boolean for if the previous move causes the "block" to stop - used in recursion
		all_paths:  list of lists of all legal paths from start to finish - final output.
			stored as the function processes
		'''

		path.append(startID)

		#Destination reached
		if startID == endID:
			all_paths.append(copy.deepcopy(path))
			path.pop()
			return
		if stop:
			path.pop()
			return

		borders = self.find_all_borders(startID)

		for borderID in borders:
			if borderID not in path and self.dynamic_borders[startID][borderID] > 0:

				stop = False

				if self.static_borders[startID][borderID] == 'R' \
				or self.regions[borderID].is_contested() \
        or not self.regions[borderID].is_neutral() and not self.regions[borderID].is_friendly(role) \
				or num_moves == 1:
					stop = True

				self.check_path(num_moves-1, borderID, endID, role, path, stop, all_paths)

		if path:
			path.pop()

		return all_paths
