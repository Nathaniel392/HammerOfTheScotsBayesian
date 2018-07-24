
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

import random
import copy
import initialize_blocks
import simulations

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

	fp = open(file_name, 'r')
	
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
		print(self.static_borders)
		self.reset_borders()
		#self.cath_coast = read_file('cath_coast.txt')
		#self.castle_points = read_file('castle_points.txt')
		self.regions = []
		self.eng_pool = []
		self.scot_pool = []
		self.scot_roster = []
		self.eng_roster = []
		
		self.initialize_regions()

	def reset_borders(self):
		'''

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

	def remove_from_region(self, block_to_remove):
		"""
		removes a block from a region and returns the block
		"""
		for block in self.regions.blocks_present:
			if block is block_to_remove:
				return self.regions.blocks_present.pop(block_to_remove)
				

	def initialize_regions(self):
		'''
		This function iniliazes a list of region objects within the board class
		'''
		data = []
		data = read_file("region_info.txt")

		specific_data = []
		
		for i in range(23):
			specific_data = data[i].split()
			self.regions.append(Region(specific_data[0], int(specific_data[1]), specific_data[2], specific_data[3], int(specific_data[4])))

	def find_borders(self,regionID):

		'''
		returns a list of all bordering regions of a particular region ID
		'''

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

			if endID in find_borders(self,check_list):

				return True

			else:

				check_list = find_borders(self,check_list)

		else:

			return False

	def move_block(self,block, start, end):
		'''
		Changes a block's location on the board, assuming that all conditions are legal.
		block:  
		start:  starting location (Region)
		end:  end location (Region)
		'''

		if check_path(self,block.movement_points,start,end):

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
		self.castle_points = castle_points
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
		

def add_starting_blocks(current_board, nobles, other_blocks):
	'''
	Adds the blocks that should be present at the beginning of the game
	to the board object in its region list at the specific region that each
	block is located.
	'''
	#Add nobles 
	for x in nobles:
		if x.location != 23 and x.location != 99:
			#Add to region
			current_board.add_to_region(x, x.location)
			#Add to roster based on allegiance
			if x.allegiance == "SCOTLAND":
				current_board.scot_roster.append(x)
			elif x.allegiance == "ENGLAND":
				current_board.eng_roster.append(x)
	#Add other blocks
	for x in other_blocks:
		if x.location != 23:
			#Add to region
			current_board.add_to_region(x, x.location)
			#Add to roster based on allegiance
			if x.allegiance == "SCOTLAND":
				current_board.scot_roster.append(x)
			elif x.allegiance == "ENGLAND":
				current_board.eng_roster.append(x)
		
		elif x.location != 99:
			#Add to pool based on allegiance
			if x.allegiance == "SCOTLAND":
				current_board.scot_pool.append(x)
			elif x.allegiance == "ENGLAND":
				current_board.eng_pool.append(x)

def get_comp_blocks(current_board, computer_role):
	'''
	This function is meant to determine which set of lists is the set that the computer
	can control. The function returns 2 lists, one with the computer's pool and the 
	other with the computer's roster
	'''
  
	if computer_role.lower() == 'scottish':
		comp_pool = copy.deepcopy(current_board.scot_pool)
		comp_roster = copy.deepcopy(current_board.scot_roster)
	else:
		comp_pool = copy.deepcopy(current_board.eng_pool)
		comp_roster = copy.deepcopy(current_board.eng_roster)

	return comp_roster, comp_pool

def find_location(current_board, block):
	'''
	Takes a block from the current battle and searches the regions
	to find a region that has that block present in its blocks_present
	list. Return the region in which it is found
	'''
	for x in current_board.regions:
		for y in x.blocks_present:
			if y.name == block.name:
				return x

def go_home(board,noble):

	'''
	takes a noble from the location that they are at and then transports them
	home. if there is more than 1 home location, it randomly picks one.
	changes allegiance based on who controls home area
	'''

	if type(noble.home_location) == int:

		
		if not board.regions[noble.home_location].blocks_present or board.regions[noble.home_location].blocks_present[0].allegiance == noble.allegiance:

			board.regions[noble.location].blocks_present.pop(noble)

			board.regions[noble.home_location].blocks_present.append(noble)

		else:

			noble.allegiance = board_regions[noble.home_location].blocks_present[0].allegiance

			board.regions[noble.location].blocks_present.pop(noble)

			board.regions[noble.home_location].blocks_present.append(noble)


	else:

		
		for home in noble.home_location:

			if not board.regions[home].blocks_present or board.regions[home].blocks_present[0].allegiance == noble.allegiance:

				board.regions[noble.location].blocks_present.pop(noble)

				board.regions[noble.home_location].blocks_present.append(noble)
				
				break

		else:

			board.regions[noble.location].blocks_present.pop(noble)

			board.regions[random.choice(noble.home_location)].blocks_present.append(noble) 

			noble.allegiance = board.regions[noble.location].blocks_present[0].allegiance 

class Winter(object):

	def __init__(self,board):

		'''
		all nobles go home for the winter
		scottish and english rp are calculated
		'''

		for noble in nobles:

			go_home(board,noble)

		self.scottish_rp = 0
		self.english_rp = 0

		for region in board.regions:

			if region.blocks_present[0].allegiance == 'SCOTLAND':

				if region.cathedral:

					self.scottish_rp += region.castle_points + 1

				else:

					self.scottish_rp += region.castle_points

			elif region.blocks_present[0].allegiance == 'ENGLAND':

				if region.cathedral:

					self.english_rp += region.castle_points + 1

				else:

					self.english_rp += region.castle_points

def should_retreat(current_board, attacking = None, defending = None, attacking_reinforcement = list(), defending_reinforcement = list(), is_attacking = None,\
	combat_letter = 'A', combat_round = 0):
	'''
	This function takes in all the group that are involved in a battle and a boolean about whether the computer is attacking or not. 
	The should_retreat function will return either False, meaning the computer should not retreat, or a location in which the computer should
	retreat its blocks to.
	'''
	attacking_copy = copy.deepcopy(attacking)
	defending_copy = copy.deepcopy(defending)
	attacking_rein_copy = copy.deepcopy(attacking_reinforcement)
	defending_rein_copy = copy.deepcopy(defending_reinforcement)

	simulation_dict = simulations.simulation(attacking_copy, defending_copy, 1000, attacking_reinforcement, defending_reinforcement, combat_letter, combat_round)
	win_percentage = 0
	#Calculate the win percentage based on if you are attacking or defending in the simulation
	if is_attacking:
		win_percentage = simulation_dict['attacker wins']
	else:
		win_percentage = simulation_dict['defender wins']

	retreat_constant = .3	
	#Insert code to check to see if it should retreat
	if win_percentage > retreat_constant:
		return False
	else:
	#Check to see where the blocks should retreat to
		current_location = find_location(attacking[0])
		possible_locations = []
		#Create list of possible locations to retreat to
		for x, border in enumerate(current_board.static_borders[current_location.regionID]):
			if is_attacking == False and attacking[0].allegiance != current_board.regions[x].blocks_present.allegiance and border != 'X':
				possible_locations.append(current_board.regions[x])
			elif is_attacking == True and defending[0].allegiance != current_board.regions[x].blocks_present.allegiance and border != 'X':
				possible_locations.append(current_board.regions[x])


		num = random.randint(0, len(possible_locations)-1)
		return possible_locations[num]


def main():
	#Create board object
	board = Board()
	#Get the blocks to add to the board
	nobles, other_blocks, static_nobles, static_other_blocks = initialize_blocks.initialize_blocks()
	add_starting_blocks(board, nobles, other_blocks)



if __name__ == '__main__':
	main()
