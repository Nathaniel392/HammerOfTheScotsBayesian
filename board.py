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
		Reads in files on borders, cathedrals, coasts, and castle points
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
		
		self.initialize_regions()

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



	def add_to_region(self, block_to_add, regionID):
		'''
		This function takes a block object and adds it to a particular region
		The value of this function is a block object, block_to_add, and a the ID
		of the region it is being added to, regionID
		'''
		self.regions[regionID].blocks_present.append(block_to_add)

	def initialize_regions(self):
		'''
		This function initializes a list of region objects within the board class
		'''
		data = []
		data = read_file("region_info.txt")

		specific_data = []
		
		for i in range(23):
			specific_data = data[i].split()
			self.regions.append(Region(specific_data[0], int(specific_data[1]), specific_data[2], specific_data[3], int(specific_data[4])))

	def find_all_borders(self,regionID):

		'''
		returns a list of all bordering regions of a particular regionID
		'''

		return_list = []

		for element in regionID:

			for i,border in enumerate(self.static_borders[element]):

				if border == "B" or border == "R":

					return_list.append(i)

		return return_list

	def find_black_borders(self,regionID,friendly = False):

		'''
		returns a list of all black bordering regions of a particular region ID
		'''

		if friendly:

			return_list = []

			for element in regionID:

				for i,border in enumerate(self.static_borders[element]):

					if border == "B" and (self.regions[i].blocks_present[0].allegiance == self.regions[regionID].blocks_present[0].allegiance or not self.regions[i].blocks_present):

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

			if endID in find_black_borders(self,check_list):

				return True

			else:

				check_list = find_black_borders(self,check_list,True)

		else:

			return False

	def move_block(self,block, start, end):
		'''
		Changes a block's location on the board, assuming that all conditions are legal. 
		Adds them to appropriate dictionaries if in a combat or attack scenario
		block:  
		start:  starting location (Region ID)
		end:  end location (Region ID)
		'''

		if self.static_borders[start][end] == 'R':

			if self.regions[end].is_contested():

				self.regions[start].blocks_present.pop(block)

				if self.regions[end].blocks_present[0].allegiance == block.allegiance:

					self.regions[end].combat_dict['Attacking Reinforcements'].append(block)

					self.regions[end].blocks_present.append(block)

				else:

					self.regions[end].combact_dict['Defending Reinforcements'].append(block)

					self.regions[end].blocks_present.append(block)

			else:

				self.regions[start].blocks_present.pop(block)

				if self.regions[end].blocks_present[0].allegiance != block.allegiance:
					
					self.regions[end].combat_dict['Defending'].append(block) for block in self.regions[end].blocks_present

					self.regions[end].combat_dict['Attacking'].append(block)

					self.regions[end].blocks_present.append(block)

				else:

					self.regions[end].blocks_present.append(block)

		
		elif check_path(self,block.movement_points,start,end):

			if self.regions[end].is_contested():

				self.regions[start].blocks_present.pop(block)

				if self.regions[end].blocks_present[0].allegiance == block.allegiance:

					self.regions[end].combat_dict['Attacking Reinforcements'].append(block)

					self.regions[end].blocks_present.append(block)

				else:

					self.regions[end].combact_dict['Defending Reinforcements'].append(block)

					self.regions[end].blocks_present.append(block)

			else:

				self.regions[start].blocks_present.pop(block)

				if self.regions[end].blocks_present[0].allegiance != block.allegiance:
					
					self.regions[end].combat_dict['Defending'].append(block) for block in self.regions[end].blocks_present

					self.regions[end].combat_dict['Attacking'].append(block)

					self.regions[end].blocks_present.append(block)

				else:

					self.regions[end].blocks_present.append(block)

class Region(object):

	def __init__(self, name, regionID, cathedral, coast, castle_points,):
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
		Prints a region object as the string 'name-ID'
		'''
		return self.name + '-' + str(self.regionID)
	def __repr__(self):
		'''
		same as __str__
		'''
		return self.name + '-' + str(self.regionID)

	def activate_movement(self):
		'''
		use 1 movement point to activate movement for blocks in a region
		used only during movement phase
		'''

		#Loop through blocks in the region
		for index, block in enumerate(self.blocks_present):
			pass
		

def add_starting_blocks(board, nobles, other_blocks):
	'''
	Adds the blocks that should be present at the beginning of the game
	to the board object in its region list at the specific region that each
	block is located.
	'''
	#Add nobles 
	for x in nobles:
		if x.location != 23:
			#Add to region
			board.add_to_region(x, x.location)
			#Add to roster based on allegiance
			if x.allegiance == "SCOTLAND":
				board.scot_roster.append(x)
			elif x.allegiance == "ENGLAND":
				board.eng_roster.append(x)
	#Add other blocks
	for x in other_blocks:
		if x.location != 23:
			#Add to region
			board.add_to_region(x, x.location)
			#Add to roster based on allegiance
			if x.allegiance == "SCOTLAND":
				board.scot_roster.append(x)
			elif x.allegiance == "ENGLAND":
				board.eng_roster.append(x)
		else:
			#Add to pool based on allegiance
			if x.allegiance == "SCOTLAND":
				board.scot_pool.append(x)
			elif x.allegiance == "ENGLAND":
				board.eng_pool.append(x)

def should_retreat(attacking, defending, attacking_reinforcement):
	pass

def main():
	#Create board object
	board = Board()



if __name__ == '__main__':
	main()



