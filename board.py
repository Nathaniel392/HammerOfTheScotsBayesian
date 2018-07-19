
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

NUM_REGIONS = 23

import initialize_blocks

def read_file(file_name):
	'''
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
		Reads in files on borders, cathedrals, coasts, and castle points
		'''
		self.static_borders = read_file('borders.txt')
		#self.cath_coast = read_file('cath_coast.txt')
		#self.castle_points = read_file('castle_points.txt')
		self.regions = []
		self.eng_pool = []
		self.scot_pool = []
		self.initialize_regions()
	def add_to_region(self, block_to_add, regionID):
		'''
		This function takes a block object and adds it to a particular region
		The value of this function is a block object, block_to_add, and a the ID
		of the region it is being added to, regionID
		'''
		self.regions[regionID].blocks_present.append(block_to_add)

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
		

def add_starting_blocks(board, nobles, other_blocks):
	'''
	Adds the blocks that should be present at the beginning of the game
	to the board object in its region list at the specific region that each
	block is located.
	'''
	#Add nobles 
	for x in nobles:
		if x.location != 23:
			board.add_to_region(x, x.location)
	#Add other blocks
	for x in other_blocks:
		if x.location != 23:
			board.add_to_region(x, x.location)
		else:
			if x.allegiance == "SCOTLAND":
				board.scot_pool.append(x)
			elif x.allegiance == "ENGLAND":
				board.eng_pool.append(x)
def main():
	#Create board object
	board = Board()

	#Get the blocks to add to the board
	nobles, other_blocks, static_nobles, static_other_blocks = initialize_blocks.initialize_blocks()
	add_starting_blocks(board, nobles, other_blocks)
	for x in board.pool:
		print(x.name)
if __name__ == '__main__':
	main()

