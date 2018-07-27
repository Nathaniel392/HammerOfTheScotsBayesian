def region_name_to_object(board, region_name):
	'''Takes a region name and returns the Region object associated with it.'''
	for region in board.regions:
		if region_name == region.name:
			return region
	return False

def region_name_to_id(board, region_name):
	'''Takes a region name and returns its id'''
	for region in board.regions:
		if region_name == region.name:
			return region.regionID
	return False

def region_object_to_name(region):
	'''Takes a Region object and returns its name'''
	return region.name

def region_object_to_id(region):
	'''Takes a Region object and returns its id'''
	return region.regionID

def region_id_to_object(board, regionID):
	'''Takes a regionID and returns the Region object'''
	return board.regions[regionID] 

def region_id_to_name(board, regionID):
	'''Takes a regionID and returns the name'''
	return board.regions[regionID].name

def block_name_to_object(block_list, block_name):
	'''Takes a block name and returns a block object'''
	for block in block_list:
		if block.name == block_name:
			return block
	return False

def block_name_to_id(block_list, block_name):
	'''Takes a block name and returns its id'''
	for block in block_list:
		if block.name == block_name:
			return block.blockID
	return False

def block_object_to_id(block):
	'''Takes a Block object and returns its id'''
	return board.blockID

def block_object_to_name(block):
	'''Takes a Block object and returns its name'''
	return block.name

def block_id_to_object(block_list, blockID):
	'''Takes a blockID and returns a Block object'''
	for block in block_list:
		if block.blockID == blockID:
			return block
	return False

def block_id_to_name(block_list, blockID):
	'''Takes a blockID ans returns its name'''
	for block in block_list:
		if block.blockID == blockID:
			return block.name
	return False