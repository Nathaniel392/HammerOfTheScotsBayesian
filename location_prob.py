import board
import copy

#creates an array
#each row of the array represents a block ID
#each column of the array represents a region ID
#the values of the matrix are the probability that a particular block is in a region

def certain_prob(table,row,index):
    '''
    takes a list of lists and a row of that list
    makes everything in that list except a specified index 0
    '''
    
    for item in table[row]:
        
        item = 0
        
    table[row][index] = 1

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

def update_prob_table_move(board,player,path,block):
    '''
    takes a board object, an opponent player,
    the path of a block (region IDs), and a block object
    updates opponent's probability table based on the movement of the block
    if using for enemy regrouping, path is just a list of starting regionID and 
    regrouping location regionID
    '''
    
    #based on the movement of the blocks, all blocks from its starting region
    #that could move in a similar path
    possible_blocks = [block]
    start = path[0]
    end = path[-1]
    
    #iterates through all blocks left in starting region to see if they could
    #move in a similar fashion as the block that moved
    for start_block in board.regions[start].blocks_present:
        
        #only blocks that have 3 movement pts are added
        if len(path) == 4:
        
            if start_block.name == 'ETTERICK' or start_block.name == 'KEITH' or start_block.name == 'HOBELARS' \
            or start_block.name == 'EDWARD' or start_block.name == 'WALLACE'\
            or start_block.type == 'KING':
                
                possible_blocks.append(start_block)
        #only Norse are added     
        elif block.name == 'NORSE':
            
            if start_block.name == 'NORSE':
                
                possible_blocks.append(start_block)
        
        #only non-French added
        else:
            
            if start_block.name != 'FRENCH':
                
                possible_blocks.append(start_block)
                
    #updates probabilities for all possible blocks
    for pos_block in possible_blocks:
        
        for i,row in enumerate(player.location_prob_table):
            
            if i == pos_block.blockID:
                
                player.location_prob_table[i][end] = player.location_prob_table[i][start]*(1/len(possible_blocks))
                player.location_prob_table[i][start] -= player.location_prob_table[i][end]
                
def update_prob_table_init_combat(attacking_player,defending_player,region):
    
    '''
    takes an attacking player object,defending player object
    and the region object with the battle
    intended to be used before a round starts -- initializes with new info
    about locations about enemy blocks
    throws an error if either reinforcement dict empty
    '''
    
    for block in region.combat_dict['Attacking']:

        certain_prob(defending_player.location_prob_table,block.blockID,region.regionID)
        
    for block in region.combat_dict['Defending']:
        
        certain_prob(attacking_player.location_prob_table,block.blockID,region.regionID)
        
def update_prob_table_round2_combat(attacking_player,defending_player,region):
    
    '''
    tales an attacking player and defending player object
    and the region object where the battle is
    used after round 1 when reinforcements can come into battle
    updates both players' probability tables with new info
    throws an error if either reinforcement dict empty
    '''
    
    for block in region.combat_dict['Attacking Reinforcements']:
        
        certain_prob(defending_player.location_prob_table,block.blockID,region.regionID)
        
    for block in region.combat_dict['Defending']:
        
        certain_prob(attacking_player.location_prob_table,block.blockID,region.regionID)
        
def update_prob_table_retreat(player1,player2,block,start_region,end_region):
    '''
    takes two player objects, a block object, and starting and ending region objects
    for that block. it is to be used for a block retreating where you know the block and
    starting and ending region. updates probability table for whichever player did not 
    retreat the block. 
    '''
    
    if block.allegiance == player1.role:
        
        player2.location_prob_table[block.blockID][start_region.regionID] = 0
        player2.location_prob_table[block.blockID][end_region.regionID] = 1
        
    else:
        
        player1.location_prob_table[block.blockID][start_region.regionID] = 0
        player1.location_prob_table[block.blockID][end_region.regionID] = 1
        
def update_prob_table_winter_noble(player1,player2,noble,location):
    
    '''
    takes two player objects, a block object of subclass noble, and a region 
    object. updates the probability table based on the fact each noble can 
    only go home to certain regions
    '''
    
    if noble.allegiance == player1.role:
        
        certain_prob(player2.location_prob_table,noble.blockID,location.regionID)
            
    elif noble.allegiance == player2.role:
        
        certain_prob(player1.location_prob_table,noble.blockID,location.regionID)
                
def update_prob_table_winter_block(player1,player2,board,block,region):
    
    '''
    for all non-noble blocks on board that have special functions during winter
    takes a board object, a block object, a region object (that the block moved to) and two player objects
    calculates probabilities for wallace and the kings
    can be used after Edward I chooses to winter in scotland with troops exceeding castle limits
    '''
    
    if region.name == 'SELKIRK-FOREST':
        
        if player1.role == 'SCOTLAND':
            
            certain_prob(player2.location_prob_table,26,18)
            
        else:
            
            certain_prob(player1.location_prob_table,26,18)
     
    #only call this function if Scottish King doesn't stay where he is
    elif block.name == 'KING':
        
        if player1.role == 'ENGLAND':
            
            certain_prob(player1.location_prob_table,27,region.regionID)
            
        else:
            
            certain_prob(player2.location_prob_table,27,region.regionID)
            
    #pass block as edward I
    elif block.name == 'EDWARD':
        
        if len(region.blocks_present) > region.castle_points + 1:
        
            if player1.role == 'SCOTLAND':
                
                certain_prob(player1.location_prob_table,block.blockID,region.regionID)
                
            else:
                
                certain_prob(player2.location_prob_table,block.blockID,region.regionID)
            
    
    
    

        
    
        
        
    
    
        
            
            

def main():
    board = board.Board()
    location_prob_table = init_probability_table(board)

if __name__ == '__main__':
	main()
