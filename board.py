'''
0	Ross
1 	Garmoran
2	Moray
3	Strathspey
4	Buchan
5	Lochaber
6	Badenoch
7	Mar
8	Angus
9	Argyll
10	Atholl
11	Fife
12	Lennox
13	Mentieth
14	Carrick
15	Lanark
16	Lothian
17	Dunbar
18	Selkirk Forest
19	Galloway
20	Annan
21	Teviot
22	England
'''

import copy
import initialize_blocks
import attacked_borders
import random
import search


NUM_REGIONS = 23
def find_location(board, blok):
	'''
	This function takes a board object and the name of a block
	and returns a region object where the block is
	'''
	for region in board.regions:
		for bllock in region.blocks_present:
			
			if bllock.name == blok.name:
				return region
		
	raise Exception('cannot find block')
def border_chars(border_array):
	'''
	function header here
	'''
	
	for row,location in combat_array:
		
		for column,color in row:
			
			if color == 'R':
				
				border_array[row][column] = 2
				
			elif color == 'B':
			
				border_array[row][column] = 6
				
			elif color == 'X':
			
				border_array[row][column] = 0
				
	return border_array


def read_file(file_name):
	'''
	Read a file and store its contents into a list of strings, one string per line
	'''

	# Open the file
	#try:
	fp = open(file_name, 'r')
	#except FileNotFoundError:
	#	print('File not found')
	
	output = []

	for line in fp:
		info = line.strip()

		output.append(info)
	
	#List of information
	fp.close()

	return output


class Board(object):

	def __init__(self):
		'''
		Reads in files on borders, set up lists for regions, pools, and rosters
		'''
		
		self.static_borders = []

		temp = read_file('borders.txt')
		for x in temp:
			self.static_borders.append(x.split())
		self.reset_borders()
		#self.cath_coast = read_file('cath_coast.txt')
		#self.castle_points = read_file('castle_points.txt')
		self.regions = []
		self.eng_pool = []
		self.scot_pool = []
		self.scot_roster = []
		self.eng_roster = []

		#print(self.static_borders)
		
		#fills self.regions
		self.initialize_regions()
		self.reset_borders()
		#Create dictionary referencing region names to regionsIDs
		self.regionID_dict = {}
		for regionID, region in enumerate(self.regions):
			self.regionID_dict[region.name] = regionID

		#Create dictionary referencing region names to regionsIDs
		self.regionID_dict = {}
		for regionID, region in enumerate(self.regions):
			self.regionID_dict[region.name] = regionID
		self.attacked_borders = attacked_borders.make_attacked_borders()


	def reset_attacked_borders(self):
		attacked_borders.reset_attacked_borders(self.attacked_borders)
		
	def reset_borders(self):
		'''
		Reset the max moves over each border in self.dynamic_borders (6, 2, 0)
		'''
		self.dynamic_borders = copy.deepcopy(self.static_borders)
		for row in range(len(self.static_borders)):
			for col in range(len(self.static_borders[0])):
				if self.dynamic_borders[row][col] == 'X':
					self.dynamic_borders[row][col] = 0
				elif self.dynamic_borders[row][col] == 'R':
					self.dynamic_borders[row][col] = 2
				elif self.dynamic_borders[row][col] == 'B':
					self.dynamic_borders[row][col] = 6

	def get_controlled_regions(self, role):
		'''
		role:  'SCOTLAND' or 'ENGLAND'
		Returns a list of Region objects that belong to the given role
		'''

		region_list = []

		for region in self.regions:

			#Fill the list with IDs of friendly regions
			if region.is_friendly(role):
				region_list.append(region)

		return region_list

	def get_contested_regions(self):
		'''
		This function is meant to loop through all the regions in 
		a board object and return a list of all the regions
		that are contested and need to have a resolved battle.
		'''
		contested_regions = []
		#Loop through all regions in board and see if they are contested
		for region in self.regions:
			if region.is_contested():
				contested_regions.append(region)

		return contested_regions

	def get_block(block_name, region):
		list_of_blocks = region.blocks_present
		for block in list_of_blocks:
			if block.name.lower() == block_name.lower():
				return block
	
	def add_to_region(self, block_to_add, regionID):
		'''
		This function takes a block object and adds it to a particular region
		The value of this function is a block object, block_to_add, and a the ID
		of the region it is being added to, regionID
		'''
		self.regions[regionID].blocks_present.append(block_to_add)

	def remove_from_region(self, block, regionID):
		"""
		removes block from region with regionID (pops off)
		returns True if block found in that region
		returns False if block not found in that region
		"""
		for i, bllock in enumerate(self.regions[regionID].blocks_present):
			if bllock == block:
				return self.regions[regionID].blocks_present.pop(i)
				
		raise Exception('cannot find block to remove')

	def fill_board(self, block_list, scenario):
		'''
		Initialize the location and alligiance of blocks
		scenario:  'BRAVEHEART' or 'BRUCE'
		block_list:  list of all block objects, no allegiance assigned
		board:  board object to be filled
		'''

		#Loop through the blocks and assign allegiance according to the init list
		#Pick the scenario based on input
		if scenario == 'BRAVEHEART':
			file = 'braveheart_init.txt'
		elif scenario == 'BRUCE':
			file = 'bruce_init.txt'
		#Take init information from file into a 2d list, same method as initialize_blocks()
		block_init_info = initialize_blocks.read_file(file)

		#Convert number data into int objects
		for row, line in enumerate(block_init_info):
			for col, data in enumerate(line):
				if data.isdigit():
					block_init_info[row][col] = int(data)

		#Set alliegance and location of blocks
		for blockID, line in enumerate(block_init_info):
			#Read information from block_init_info
			allegiance = line[1]
			location = line[2]

			block_list[blockID].allegiance = allegiance  #Alleigance: SCOTLAND or ENGLAND
			block_to_add = block_list[blockID]

			#pool
			if location == 23:
				if allegiance == 'ENGLAND':
					self.eng_pool.append(block_to_add)
				elif allegiance == 'SCOTLAND':
					self.scot_pool.append(block_to_add)

			#put on board
			elif location != 99:
				self.regions[location].add_block(block_to_add)

				if allegiance == 'ENGLAND':
					self.eng_roster.append(block_to_add)
				elif allegiance == 'SCOTLAND':
					self.scot_roster.append(block_to_add)


	def initialize_regions(self):
		'''
		This function initializes a list of region objects within the board class
		'''
		data = []
		#Reusing the read_file in initialize_blocks, returns 2D list
		data = initialize_blocks.read_file("region_info.txt")

		specific_data = []
		
		for line_num, line in enumerate(data):

			#Change data types from string to int, T/F to bool
			for index, item in enumerate(line):
				if item.isdigit():
					data[line_num][index] = int(item)
				if item == 'T':
					data[line_num][index] = True
				elif item == 'F':
					data[line_num][index] = False

			name = line[0]
			regionID = line[1]
			cathedral = line[2]
			coast = line[3]
			castle_points = line[4]

			temp_region = Region(name, regionID, cathedral, coast, castle_points)
			self.regions.append(temp_region)

		#print(self.regions)

	def find_adjacent_regions(self, regionID):
		'''
		Returns a list of all bordering regionIDs of a region, given its regionID
		'''
		
		return_list = []
		for i, border in enumerate(self.static_borders[regionID]):

			if border == "B" or border == "R":
				return_list.append(i)

		return return_list
  
	def find_all_borders(self, regionID_list):
		'''
		returns a list of all bordering regionIDs in a list of regionIDs
		'''
		return_list = list()
		for element in regionID_list:
			for i,border in enumerate(self.static_borders[element]):

				if border == "B" or border == "R":
					return_list.append(search.region_id_to_object(self, i))

		return return_list

	def check_path(self, num_moves, startID, endID, block, path=[], stop=False, all_paths=[], truce=False):
		'''
		Finds all legal paths between two regions
		num_moves:  a block's movement points (int)
		startID:  regionID of the starting region (int)
		endID:  regionID of the ending region (int)
		block:  Block object, for use with checking if the norse is being moved
		path:  temporary stored path for the recursive function - keeps track of where it's been
		stop:  boolean for if the previous move causes the "block" to stop - used in recursion
		all_paths:  list of lists of all legal paths from start to finish - final output.
			stored as the function processes
		truce:  Boolean, if the TRU card was played - restricts movement
		'''

		#Norse block has different movement rules - can move from friendly coastal to friendly coastal, but not england
		if block.type == 'NORSE':

			if self.regions[endID].coast and self.regions[endID].is_friendly(block.allegiance) and endID != 22:
				path = [endID]
				return path

		#Not NORSE block
		else:

			#path is a list of regions the algorithm has traversed to reach its current locaiton
			#store the current location into the path
			path.append(startID)

			#Destination reached - store the path, minus the first region (for convenience)
			if startID == endID:
				all_paths.append(copy.deepcopy(path))
				path.pop()
				return
			#Can't go further - don't search for more borders
			if stop:
				path.pop()
				return

			#Find borders to search for
			borders = self.find_adjacent_regions(startID)

			for borderID in borders:

				#Don't search regions already traversed or border limit is used up, or if it's enemy controlled and truce is True
				if borderID not in path and self.dynamic_borders[startID][borderID] > 0 \
				and not (truce and not self.regions[borderID].is_neutral() and not self.regions[borderID].is_friendly(role)):

					#Set a boolean if this should be the last move in a path
					stop = False
					if self.static_borders[startID][borderID] == 'R' \
					or self.regions[borderID].is_contested() \
					or not self.regions[borderID].is_neutral() and not self.regions[borderID].is_friendly(block.allegiance) \
					or borderID == 22	\
					or num_moves == 1:
						stop = True

					#Take the adjacent border and keep searching
					self.check_path(num_moves-1, borderID, endID, block, path, stop, all_paths, truce)

			#After exhausting all borders, delete the region from memory (path) and move onto the next region
			if path:
				path.pop()

		#Final output
		return all_paths

	def check_all_paths(self, num_moves, startID, block, path=[], stop=False, all_paths=[], truce=False):
		'''
		Finds all legal paths from a region - modified version of check_path
		num_moves:  a block's movement points (int)
		startID:  regionID of the starting region (int)
		path:  temporary stored path for the recursive function - keeps track of where it's been
		block:  Block object, for use with checking if the norse is being moved
		stop:  boolean for if the previous move causes the "block" to stop - used in recursion
		all_paths:  list of lists of all legal paths from start - final output.
			stored as the function processes
		truce:  Boolean, if the TRU card was played - restricts movement
		'''

		#Norse block has different movement rules
		if block.type == 'NORSE':
			
			for region in self.regions:
				if region.coast and region.is_friendly(block.allegiance) and region.regionID != 22:

					path = [region.regionID]
					all_paths.append(path)

			return all_paths

		#Not NORSE block
		else:

			#path is a list of regions the algorithm has traversed to reach its current locaiton
			#store the current location into the path
			path.append(startID)

			#Store the algorithm's current path if it's unique
			if path not in all_paths:
				all_paths.append(copy.deepcopy(path))

			#Can't go further - don't look for more borders
			if stop:
				path.pop()
				return

			#Find borders to search through
			borders = self.find_adjacent_regions(startID)

			for borderID in borders:
				#Don't search regions already traversed
				if borderID not in path and self.dynamic_borders[startID][borderID] > 0 \
				and not (truce and not self.regions[borderID].is_neutral() and not self.regions[borderID].is_friendly(role)):

					#Set a boolean if this should be the last move in a path
					stop = False
					if self.static_borders[startID][borderID] == 'R'	\
					or self.regions[borderID].is_contested()	\
					or not self.regions[borderID].is_neutral() and not self.regions[borderID].is_friendly(block.allegiance)	\
					or borderID == 22	\
					or num_moves == 1:
						stop = True

					#Take the adjacent border and keep searching
					self.check_all_paths(num_moves-1, borderID, block, path, stop, all_paths, truce)

			#After exhausting all borders, delete the region from memory (path) and move onto the next region
			if path:
				path.pop()

		#Final output
		return all_paths
  
	def move_block(self, block, start, end = -1, position = 'comp', prev_paths = [], is_truce = False):
		'''
		Changes a block's location on the board, assuming that all conditions are legal. 
		Adds them to appropriate dictionaries if in a combat or attack scenario

		Takes a list of all previous paths taken in that turn
		Takes a position -- computer or opponent

		block:  
		start:  starting location (Region ID)
		end:  end location (Region ID)
		'''
		


		if position == 'comp':
			print('comp tried to move')

			#Find every path from the start regionID to the end regionID and put them in a list
			paths = self.check_path(block.movement_points,start,end, block, all_paths = list())

			#print(paths)
			#If valid paths exist, keep going
			if paths:
				print(paths)
				computer_path = random.choice(paths)
				print('computer chose ' + str(computer_path))


				path_taken = False

				for path in prev_paths:

					if path == computer_path:

						path_taken = True

						break

				if not path_taken:

					prev_paths.append(computer_path)

				#If the final region in the path is contested
				if self.regions[end].is_contested():
	        
	        		#Remove the block from its starting location
					self.regions[start].blocks_present.remove(block)

					#Move it to the correct dictionary list
					if self.regions[end].blocks_present[0].allegiance != block.allegiance and path_taken: 
						self.regions[end].combat_dict['Attacking'].append(block)

					elif self.regions[end].blocks_present[0].allegiance != block.allegiance:
						self.regions[end].combat_dict['Attacking Reinforcements'].append(block)

					else:
						self.regions[end].combact_dict['Defending Reinforcements'].append(block)

					#Add it to the region's overall block list as well
					self.regions[end].blocks_present.append(block)
					print('Moved into contested region.')
					print(block.name + " was moved from " + self.regions[start].name + " to " + self.regions[end].name)

				#End location is not contested
				else:

					#If it's an enemy controlled region
					if len(self.regions[end].blocks_present) != 0 and self.regions[end].blocks_present[0].allegiance != block.allegiance:

						#Stop the function if it's truce
						if is_truce:
							print("You can't move there fool, issa truce")
							return False
			  
			  			#Set the defending blocks into the defending dictionary
						for defending_block in self.regions[end].blocks_present:
							self.regions[end].combat_dict['Defending'].append(defending_block)

						#Move the attacking into the attacking dictionary
						self.regions[end].combat_dict['Attacking'].append(block)
						self.regions[end].blocks_present.append(block)
						self.regions[start].blocks_present.remove(block)
						print('Moved into enemy region')
						print(block.name + " was moved from " + self.regions[start].name + " to " + self.regions[end].name)

						#Set the border between the last and second to last region in the path to attacked
						self.attacked_borders[computer_path[-2]][end] = True

					#Friendly or neutral
					else:
						self.regions[start].blocks_present.remove(block)
						self.regions[end].blocks_present.append(block)
						print('Moved to friendly or neutral region')
						print(block.name + " was moved from " + self.regions[start].name + " to " + self.regions[end].name)

				#Decrement the border limits of each border in the path
				for i in range(len(computer_path)-2):
					self.dynamic_borders[computer_path[i]][computer_path[i+1]] -= 1

			#No valid paths
			else:
				return False

		#Human player input
		else:	#if position == 'opp'

			taking_input = True

			user_path = [start]

			print ("Enter your path ('done' to stop):")

			counter = 1

			while taking_input:

				print(user_path)

				user_input = input("Location " + str(counter) + ": ")
				user_input_region = search.region_name_to_id(self,user_input.upper())

				#If it's a valid region, add it to the list

				if user_input_region:

					if user_input_region == start:

						print("Don't include starting location!")

					else:

						user_path.append(user_input_region)

						counter += 1

				#Stop taking input
				elif user_input.lower() == 'done':

					taking_input = False

				#Invalid input
				else:

					print ("Not a valid location!")

			end = user_path[-1]
			potential_paths = self.check_path(block.movement_points,user_path[0],user_path[-1], block)
			print(potential_paths)
			if user_path in potential_paths:

				path_taken = False

				for path in prev_paths:

					if path == user_path:

						path_taken = True

						break

				if not path_taken:

					prev_paths.append(user_path)

				#If the final region in the path is contested
				if self.regions[end].is_contested():
	        
	        		#Remove the block from its starting location
					self.regions[start].blocks_present.remove(block)

					#Move it to the correct dictionary list
					if self.regions[end].blocks_present[0].allegiance != block.allegiance and path_taken: 
						self.regions[end].combat_dict['Attacking'].append(block)

					elif self.regions[end].blocks_present[0].allegiance != block.allegiance:
						self.regions[end].combat_dict['Attacking Reinforcements'].append(block)

					else:
						self.regions[end].combact_dict['Defending Reinforcements'].append(block)

					#Add it to the region's overall block list as well
					self.regions[end].blocks_present.append(block)
					print('Moved into contested region.')
					print(block.name + " was moved from " + self.regions[start].name + " to " + self.regions[end].name)

				#End location is not contested
				else:

					#If it's an enemy controlled region
					if len(self.regions[end].blocks_present) != 0 and self.regions[end].blocks_present[0].allegiance != block.allegiance:

						#Stop the function if it's truce
						if is_truce:
							print("You can't move there fool, issa truce")
							return False
			  
			  			#Set the defending blocks into the defending dictionary
						for defending_block in self.regions[end].blocks_present:
							self.regions[end].combat_dict['Defending'].append(defending_block)

						#Move the attacking into the attacking dictionary
						self.regions[end].combat_dict['Attacking'].append(block)
						self.regions[end].blocks_present.append(block)
						self.regions[start].blocks_present.remove(block)
						print('Moved into enemy region')
						print(block.name + " was moved from " + self.regions[start].name + " to " + self.regions[end].name)

						#Set the border between the last and second to last region in the path to attacked
						self.attacked_borders[user_path[-2]][end] = True

					#Friendly or neutral
					else:
						self.regions[start].blocks_present.remove(block)
						self.regions[end].blocks_present.append(block)
						print('Moved to friendly or neutral region')
						print(block.name + " was moved from " + self.regions[start].name + " to " + self.regions[end].name)

				#Decrement border limits on borders crossed in the path
				for i in range(len(user_path)-2):

					self.dynamic_borders[user_path[i]][user_path[i+1]] -= 1

			#No valid paths
			else:

				return False

		#Successfully executed
		return True


	def __repr__(self):
		'''
		Terminal representation of the board
		'''
		output = str(self.regions)
		return output

	def add_to_location(self,block,location):

		'''
		takes a board, block, and region object
		removes block from its current region 
		puts it into the new location
		'''

		if type(location) == int:
			location = search.region_id_to_object(self, location)


		if location == 'scottish pool':
			self.regions[find_location(self,block).regionID].blocks_present.remove(block)

			self.scot_pool.append(block)
		elif location == 'english pool':
			self.regions[find_location(self, block).regionID].blocks_present.remove(block)
			self.eng_pool.append(block)
			print("Sent" + block.name + ' to ' + location.name)

		else:

			self.regions[find_location(self,block).regionID].blocks_present.remove(block)

			self.regions[location.regionID].blocks_present.append(block)

			print ("Sent " + block.name + " to " + location.name)


class Region(object):

	def __init__(self, name, regionID, cathedral, coast, castle_points):
		'''
		This function creates a Region object with characteristics given to it
		The parameters are a string name, int regionID, boolean cathedral, boolean coast,
		and int castle_point
		The function also initializes other values
		'''

		self.name = name
		self.regionID = regionID
		self.cathedral = cathedral
		self.coast = coast
		self.combat_dict = {'Attacking':[], 'Defending':[], 'Attacking Reinforcements':[], 'Defending Reinforcements':[]}
		self.contested = False
		self.blocks_present = []

	def __str__(self):
		'''
		Prints a region object, its characteristics, and blocks
		'''
		output = ''
		output += '-'*20 + '\n'
		output += self.name + ' - ' + str(self.regionID) + '\n'
		
		if self.cathedral:
			output += '\t*Cathedral\n'
		if self.coast:
			output += '\t*Coastal\n'

		block_string = ''
		for block in self.blocks_present:
			block_string += block.name + ' '
		if block_string != '':
			output += '\t' + block_string + '\n'
		output += '-'*20

		return output

	def __repr__(self):
		return str(self)

	def add_block(self, block):
		'''
		Add block to blocks_present - used in game initialization
		block:  Block object to be added to the list of 
		'''
		self.blocks_present.append(block)

	def is_friendly(self, role):
		'''
		role is 'ENGLAND' or 'SCOTLAND'
		Returns True if the region only contains troops of that side
		'''
		for block in self.blocks_present:
			if block.allegiance != role:
				return False
		return True

	def is_neutral(self):
		'''
		Returns True if the region is empty
		'''
		return len(self.blocks_present) == 0
	
	def is_contested(self):
		'''
		Returns True if the region is contested - has blocks of both sides
		'''

		if len(self.blocks_present) == 0:
			return False
		allegiance = self.blocks_present[0].allegiance 

		for block in self.blocks_present:

			if block.allegiance != allegiance:

				return True

		else:
			return False

	def activate_movement(self):
		'''
		use 1 movement point to activate movement for blocks in a region
		used only during movement phase
		'''

		#Loop through blocks in the region
		for index, block in enumerate(self.blocks_present):
			pass

def main():
	#Create board object
	board = Board()



if __name__ == '__main__':
	main()



