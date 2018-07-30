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

NUM_REGIONS = 23

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

		#Create dictionary referencing region names to regionsIDs
		self.regionID_dict = {}
		for regionID, region in enumerate(self.regions):
			self.regionID_dict[region.name] = regionID

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

		for region in board.regions:

	        #Fill the list with IDs of friendly regions
	        if region.is_friendly():
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
			if bllock is block:
				self.regions[regionID].blocks_present.pop(i)
				return True
		return False

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

	def find_all_borders(self,regionID):
		'''
		returns a list of all bordering regions of a particular regionID
		'''

		return_list = [self.regions[regionID]]
		for element in regionID:
			for i,border in enumerate(self.static_borders[element]):

				if border == "B" or border == "R":
					return_list.append(i)

		return return_list

	def find_black_borders(self,regionID,friendly = False):
		'''
		regionID:  ID of a region to be checked
		friendly:  
		Returns a list of regionIDs of regions that share a black border with the given region
		'''

		if friendly:
			return_list = [self.regions[regionID]]

			for element in regionID:
				for i, border in enumerate(self.static_borders[element]):

					if border == "B" and (self.regions[i].blocks_present[0].allegiance == self.regions[element].blocks_present[0].allegiance or not self.regions[i].blocks_present):
						return_list.append(i)

			return return_list

		else:
			return_list = []

			for element in regionID:
				for i,border in enumerate(self.static_borders[element]):

					if border == "B":
						return_list.append(i)

			return return_list



	def check_path(self,num_moves,startID,endID):
		'''
		takes a block's movement points, starting location ID, ending location ID, and a board object and
		checks to see if it can move from one location to another
		'''

		check_list = [startID]

		for i in range(num_moves):

			if endID in self.find_black_borders(check_list):
				return True

			else:
				check_list = self.find_black_borders(check_list,True)

		return False

	def move_block(self, block, start, end, is_truce = False):
		'''
		Changes a block's location on the board, assuming that all conditions are legal. 
		Adds them to appropriate dictionaries if in a combat or attack scenario
		block:  
		start:  starting location (Region ID)
		end:  end location (Region ID)
		'''

		if self.static_borders[start][end] == 'R':

			if self.regions[end].is_contested():

				self.regions[start].blocks_present.remove(block)

				if self.regions[end].blocks_present[0].allegiance == block.allegiance:
					self.regions[end].combat_dict['Attacking Reinforcements'].append(block)
					self.regions[end].blocks_present.append(block)

				else:
					self.regions[end].combat_dict['Defending Reinforcements'].append(block)
					self.regions[end].blocks_present.append(block)

			else:
				self.regions[start].blocks_present.remove(block)

				if len(self.regions[end].blocks_present) != 0 and self.regions[end].blocks_present[0].allegiance != block.allegiance:
          			
          			if is_truce:
          				return False

					for block in self.regions[end].blocks_present:
						self.regions[end].combat_dict['Defending'].append(block)

					self.regions[end].combat_dict['Attacking'].append(block)
					self.regions[end].blocks_present.append(block)

				else:
					self.regions[end].blocks_present.append(block)

		
		elif self.check_path(block.movement_points,start,end):

			if self.regions[end].is_contested():

				self.regions[start].blocks_present.remove(block)

				if self.regions[end].blocks_present[0].allegiance == block.allegiance:
					self.regions[end].combat_dict['Attacking Reinforcements'].append(block)
					self.regions[end].blocks_present.append(block)

				else:
					self.regions[end].combact_dict['Defending Reinforcements'].append(block)
					self.regions[end].blocks_present.append(block)

			else:
				self.regions[start].blocks_present.remove(block)

				if len(self.regions[end].blocks_present) != 0 and self.regions[end].blocks_present[0].allegiance != block.allegiance:

					if is_truce:
						return False
          
					for block in self.regions[end].blocks_present:
						self.regions[end].combat_dict['Defending'].append(block)

					self.regions[end].combat_dict['Attacking'].append(block)
					self.regions[end].blocks_present.append(block)

				else:
					self.regions[end].blocks_present.append(block)

		else:
			return False

	def __repr__(self):
		'''
		Terminal representation of the board
		'''
		output = str(self.regions)
		return output

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
        return len(self.blocks_present) > 0 and self.blocks_present[0].allegiance == role

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



