import blocks
def find_block(name, block_list):
	'''
	returns a block given a name in block_list
	'''
	for block in block_list:
		if block.name == name.upper():
			return block
	raise Exception("cant find block with name: " , name)