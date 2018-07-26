import board
import copy

#creates an array
#each row of the array represents a block ID
#each column of the array represents a region ID
#the values of the matrix are the probability that a particular block is in a region

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


def init_probability_table(board, block_list):
	'''
	Initialize and return a table with row indeces representing blockIDs and column indeces representing regionIDs.
		Table is filled with probability that a block is in a given region.
	board:  The board
	block_list:  List of all block objects in the game
	'''

	# Initialize the table, with 0 as all probabilities
	loc_probabilities = []

	for row_num in range(len(block_list)):
		temp_list = []

		for col_num in range(len(board.regions)):
			temp_list.append(0.0)
		loc_probabilities.append(temp_list)

	#Loop through blocks
	for blockID, block in enumerate(block_list):

		#Loop through regions
		for regionID, region in enumerate(board.regions):

			#If it's not england, assign blocks as 100% certain
			if regionID != 22:
				if block in region.blocks_present:
					loc_probabilities[blockID][regionID] = 1.0

			#In england, check if a block is available in the pool
			elif block in board.eng_pool:
				prob = 4.0 / len(board.eng_pool)
				loc_probabilities[blockID][regionID] = prob

	#print_table(board, block_list, loc_probabilities)


def main():
    board = board.Board()
    location_prob_table = init_probability_table(board)

if __name__ == '__main__':
	main()
