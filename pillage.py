import search
def sum_health(board, region):

	"""
	region is regionid
	"""

	region = search.region_id_to_object(board, region)
	health_sum = 0
	for block in region.blocks_present:
		health_sum += block.current_strength
	return health_sum
def max_health(region):
	"""
	region is regionid
	"""

	region = search.region_id_to_object(board, region)
	health_sum = 0
	for block in region.blocks_present:
		health_sum += block.attack_strength
	return health_sum
def value_blocks(regionid):
	valuable_blocks = {'WALLACE':18, 'KING':22, 'EDWARD':16, 'HOBELARS':13}
	value = 0
	region = search.region_id_to_object(regionid)
	for block in region.blocks_present:
		if block.name in valuable_blocks:
			value += valuable_blocks[block.name]
	return value


			
def pillage_utility(board, region_options):
	
	utility_dict = dict()

	for region_id, friendly_region_tuple in region_options.items():
		for region_friendly in friend_region_tuple:
			utility_dict[(region_id, region_friendly)] = 0



			#if enough things to pillage good
		
			if sum_health(board, region) >= 2:
				utility_dict[(region_id, region_friendly)] += .5
			elif sum_health(board, region) == 1: 
				utility_dict[(region_id, region_friendly)] += .1


			#takes friendly health into account
			if max_health(board, region_friendly) - sum_health(board,region_friendly) >= 2:
				utility_dict[region_id, region_friendly] += .5
			elif sum_health(board, region) == 1:
				utility_dict[(region_id, region_friendly)] += .1

			#value of enemy blocks and friendly blocks
			utility_dict[(region_id, region_friendly)] += value_blocks(region_id)
			utility_dict[(region_id, region_friendly)] += value_blocks(region_friendly)

	return utility_dict




		
		


	


