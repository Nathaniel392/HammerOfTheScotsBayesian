
import copy
import blocks

#creates an array
#each row of the array represents a block ID
#each column of the array represents a region ID
#the values of the matrix are the probability that a particular block is in a region

SCOT_POOL_ID = 23
ENG_POOL_ID = 24
EDWARD_ID = 27


def print_table(board, block_list, loc_probabilities, names=False):
	'''
	Prints the location probability table.
	board:  the board
	block_list:  List of every block in the game
	prob_table:  table of block location probabilities: list with rows indeces as blockIDs, column indeces as regionIDs
		and filled with probabilities that a given block is in a given region.
	names:	If the table should be titled with names or IDs.
	'''

	#Format and print the title
	title_row = ''
	for regionID, region in enumerate(board.regions):
		if names:
			title_row += '\t\t' + region.name[:3]
		else:
			title_row += '\t\t' + str(regionID)

	print(title_row)

	#Print table
	for row_num, row in enumerate(loc_probabilities):
		#Format and print title
		if names:
			print(block_list[row_num].name[:3], end='\t\t')
		else:
			print(row_num, end='\t\t')
		#Print data
		for data in row:
			print('{:.2f}'.format(data), end='\t')
		print()


def init_probability_table(self):
	'''
	Initialize and return a table with row indeces representing blockIDs and column indeces representing regionIDs.
		Table is filled with probability that a block is in a given region.
	board:  The board
	block_list:  List of all block objects in the game
	'''

	# Initialize the table, with 0 as all probabilities
	loc_probabilities = []

	for row_num in range(len(self.all_blocks)):
		temp_list = []

		for col_num in range(len(self.regions)):
			temp_list.append(0.0)
		loc_probabilities.append(temp_list)

	#Loop through blocks
	for blockID, block in enumerate(self.all_blocks):

		#Loop through regions
		for regionID, region in enumerate(self.regions):

			#If it's not england, assign blocks as 100% certain
			if regionID != 22:
				if block in region.blocks_present:
					loc_probabilities[blockID][regionID] = 1.0

			#In england, check if a block is available in the pool
			elif block in self.eng_pool:
				prob = 4.0 / len(self.eng_pool)
				loc_probabilities[blockID][regionID] = prob

	self.prob_table = copy.deepcopy(loc_probabilities)



	#print_table(board, block_list, loc_probabilities)

def update_prob_table_given_move(self, block, start_region, end_region):
	"""
	updates the table after a move.
	please call this function before the move is actually made on the real board
	block is the block to move
	start_region is the start region
	end_region is the end region
	doesn't retunr anything
	"""
	prob_to_start = self.prob_table[block.blockID][start_region.regionID]


	#find number of blocks in region just using actual board
	num_blocks_in_start = len(self.regions[start_region.regionID].blocks_present)

	#search through table to find who is possibly in the original region
	#find the probabilites that they are in there

	#possible_blocks_dict has blockID key and probability in start_region as being a value
	possible_blocks_dict = dict()
	for blockID, block_probabilites in enumerate(self.prob_table):
		for regionID, probability in enumerate(self.prob_table[blockID]):
			if regionID == start_region.regionID:
				possible_blocks_dict[blockID] = probability


	#updates probabilities in end_region
	for blockID, block_probabilities in enumerate(self.prob_table):
		if blockID in possible_blocks_dict:
			self.prob_table[blockID][end_region.regionID] = possible_blocks_dict[blockID]

	#updates probabilites in start_region	
	updated_probabilities = dict()

	for blockID, probability in possible_blocks_dict.items():
		updated_probabilities[blockID] = probability * ((num_blocks_in_start - 1) / num_blocks_in_start)
	for blockID, block_proabilities in enumerate(self.prob_table):
		for regionID, probabilities in enumerate(self.prob_table[blockID]):
			if regionID == start_region.regionID:
				self.prob_table[blockID][start_region.regionID] = updated_probabilities[blockID]

def update_prob_table_given_blocks_seen(self, block_ids_seen, regionid):
	"""
	updates the probabilities if blocks are seen (usually combat)
	block_ids_seen is a set of blocks seen
	region is the regionid that they are seen in 
	returns nothing
	"""

	#check people not using the function right
	if type(block_ids_seen) != set:
		raise Exception('block_ids_seen is a set')
	for block_id in block_ids_seen:
		if type(block_id) != int:
			raise Exception('block_ids_seen is a set of block_ids (int)')
	if type(regionid) != int:
		raise Exception('regionid is a regionid (int)')


	#reset all the probabilities to 0 in regions that it could have been in
	#for blocks in block_ids_seen
	for blockID, block_probabilities in enumerate(self.prob_table):
		for regionID, probability in enumerate(self.prob_table[blockID]):
			if blockID in block_ids_seen:
				self.prob_table[blockID][regionID] = 0

	#put the probability to 1 where the block is seen
	for blockID in block_ids_seen:
		self.prob_table[blockID][regionid] = 1

def update_prob_table_given_disbanding(self, regionid, num_blocks_disbanding):
	"""
	updates probabilites after disbanding in a certain region
	regionid is the region that ppl are disbanding from
	num_blocks_disbanding is the number of blocks disbanding
	returns None unless the region is empty (returns 'no blocks are disbanding here, sir')
	"""

	#check ppl not using the function correctly
	if type(regionid) != int:
		raise Exception('regionid is a regionid (int)')
	if type(num_blocks_disanding) != int:
		raise Exception('num_blocks_disbanding is the number of blocks disbanding (int)')


	
	#find num_blocks not using nobles but including moray (he can disband)
	for block in self.regions[regionid].blocks_present:
		if type(block) != blocks.Noble or block.name == 'MORAY':
			num_blocks_in_region += 1


	if num_blocks_in_region == 0:
		return 'no blocks are disbanding here, sir'


	#find out the allegiance of who is disbanding
	disbanding_allegiance = self.regions[regionid].blocks_present[0].allegiance


	#find possible blocks that could be in the region
	possible_blockids_in_region = dict()
	for blockID, block_probabilities in enumerate(self.prob_table):
		for regionID, probability in enuemrate(self.prob_table[blockID]):
			if probability > 0.0:
				possible_blockids_in_region[blockID] = probability



	#scotland first
	if disbanding_allegiance == 'SCOTLAND':
		for blockID in possible_blockids_in_region:
			type_of_block = board.all_blocks[blockID].type
			if type_of_block != 'COMYN' and type_of_block != 'BRUCE' or search.block_id_to_name(board.all_blocks, blockID) == 'MORAY':
				self.prob_table[blockID][SCOT_POOL_ID] += (num_blocks_disbanding / num_blocks_in_region) * possible_blockids_in_region[blockID]
				self.prob_table[blockID][regionid] -= (num_blocks_disbanding / num_blocks_in_region) * possible_blockids_in_region[blockID]


	#england next
	elif disbanding_allegiance == 'ENGLAND':
		if EDWARD_ID not in possible_blockids_in_region:
			for blockID in possible_blockids_in_region:
				type_of_block = board.all_blocks[blockID].type
				if type_of_block == 'KNIGHT' or type_of_block == 'ARCHER':
					self.prob_table[blockID][ENG_POOL_ID] = 1
					self.prob_table[blockID][regionid] = 0
		elif type_of_block != 'COMYN' and type_of_block != 'BRUCE':
			for blockID in possible_blockids_in_region:
				self.prob_table[blockID][ENG_POOL_ID] += (num_blocks_disbanding / num_blocks_in_region) * possible_blockids_in_region[blockID]
				self.prob_table[blockID][regionid] -= (num_blocks_disbanding / num_blocks_in_region) * possible_blockids_in_region[blockID]





	else:
		raise Exception('block allegiance is neither "ENGLAND" or "SCOTLAND"')

def update_prob_table_nobles(self, noble_set = None, home_location = None):
	"""
	updates all the probabilites after the nobles move for not bruce or comyn and of course not moray
	noble_set not equals none when calling from bruce or comyn
	"""

	#find all nobles
	if noble_set == None:
		noble_set = set()
		for block in board.all_blocks:
			#no moray or bruce or comyn
			if type(block) == blocks.Noble and block.name != 'MORAY' and type(noble.home_location) == int:
				noble_set.add(block)

	noble_id_set = set()
	for noble in noble_set:
		noble_id_set.add(noble.blockID)


	#update home location probabilites for not bruce or comyn
	for noble in noble_set:
		self.prob_table[blockID][noble.home_location] = 1


	#reset their old probabilites to 0
	for blockID, block_probabilities in enumerate(self.prob_table):
		for regionID, probability in enumerate(self.prob_table[blockID]):
			if blockID in noble_id_set:
				self.prob_table[blockID][regionID] = 0


	#fix the other block's probabilities

	region_prob_sum_lst = [0] * 22
	for blockID, block_probabilities in enumerate(self.prob_table):
		for regionID, probability in enumerate(self.prob_table[blockID]):
			region_prob_sum_lst[regionID] += probability


	for region_prob in region_prob_sum_lst:
		for blockID, block_probabilites in enumerate(self.prob_table):
			for regionID, probability in enumerate(self.prob_table[blockID]):
				self.prob_table[blockID][regionID] /= region_prob
	for blockID, block_probabilities in enumerate(self.prob_table):
		if sum(block_probabilities) != 1:
	
			sum_block_probabilities = 0
			for regionID, probability in enumerate(self.prob_table[blockID]):		
				if region_prob[regionID] == 1:
					
					sum_block_probabilities += 1
			for regionID, probability in enumerate(self.prob_table[blockID]):
				if region_prob[regionID] == 1:
					self.prob_table[blockID][regionID] /= sum_block_probabilities

	if len(noble_set) == 1:
		noble_set[0].home_location = home_location


				






def update_prob_table_bruce_comyn(self):
	"""
	updates the probability tables of bruce and comyn
	please call this method after nobles are gone home
	"""
	bruce = None
	comyn = None
	for block in self.all_blocks:
		if block.name == 'COMYN':
			comyn = block
		elif block.name == 'BRUCE':
			bruce = block


	#bruce first
	bruce_allegiance = bruce.allegiance
	enemy_regions = list()
	for home_location in bruce.home_location:
		if board.regions.is_enemy(bruce.allegiance): 
			enemy_regions.append(home_location)
	if len(enemy_regions) == 1:
		home_location_tuple = bruce.home_location
		bruce.home_location = enemy_regions[0]
		self.update_prob_table_nobles(noble_set = [bruce], home_location = home_location_tuple)



	comyn_allegiance = comyn.allegiance
	enemy_regions = list()
	for home_location in comyn.home_location:
		if board.regions.is_enemy(comyn.allegiance): 
			enemy_regions.append(home_location)
	if len(enemy_regions) == 1:
		home_location_tuple = bruce.home_location
		comyn.home_location = enemy_regions[0]
		self.update_prob_table_nobles(noble_set = [comyn], home_location = home_location_tuple)

	

	













def main():
    board = board.Board()
    location_prob_table = init_probability_table(board)

if __name__ == '__main__':
	main()
