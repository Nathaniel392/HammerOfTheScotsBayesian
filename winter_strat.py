import search
import blocks

def moray_util(player,board,noble):

	'''
	returns a dictionary with the utility of three choices for moray
	staying, going home, or disbanding
	takes a player object, board object, and moray's object
	'''

	util_dict = {'disband':0.001}

	stay_loc = find_location(board,noble)

	if board.regions[noble.home_location].blocks_present[0].allegiance == noble.allegiance:

		util_dict['home'] = 0

	elif stay_loc.cathedral:

		if len(stay_loc.blocks_present) <= stay_loc.castle_points + 1:

			util_dict['stay'] = 0

	else:

		if len(stay_loc.blocks_present) <= stay_loc.castle_points:

			util_dict['stay'] = 0


	for i,border in enumerate(board.dynamic_borders[noble.home_location]):

		if border != 'X':

			if board.regions[i].blocks_present.allegiance == 'ENGLAND':

				if 'stay' in util_dict:

					util_dict['stay'] += 1
				
				util_dict['disband'] += 1

	for i,border in enumerate(board.dynamic_borders[stay_loc.regionID]):

		if border != 'X':

			if board.regions[i].blocks_present.allegiance == 'ENGLAND':

				if 'home' in util_dict:

					util_dict['home'] += 1
				
				util_dict['disband'] += 1


	moray_missing_strength = noble.attack_strength - noble.current_strength

	for health in range(moray_missing_strength):

		if 'home' in util_dict:

			util_dict['home'] += 2

	return util_dict

def edward_util(player,board,block,edward_prev_winter = False):

	util_dict = {'disband':0.001}

	if not edward_prev_winter:

		stay_loc = find_location(board,block)

		util_dict['stay'] = 0

	strength_missing = block.attack_strength - block.current_strength

	for health in range(strength_missing):

		util_dict['disband'] += 1

	for i,border in enumerate(board.dynamic_borders[stay_loc.regionID]):

		if border != 'X':

			if board.regions[i].blocks_present.allegiance == 'SCOTLAND':

				util_dict['disband'] += 1

	for support_block in stay_loc.blocks_present:

		if block.type != 'INFANTRY' or type(block) != blocks.Noble:

			if 'stay' in util_dict:

				util_dict['stay'] += 2

	return util_dict

def scot_king_util(player,board,block):

	'''
	returns all possible locations for scot king to move to
	as a dictionary with utilities as values and location names as keys
	'''

	util_dict = {'disband':1}

	for region in board.regions:

		if (region.blocks_present[0].allegiance == "SCOTLAND") and region.cathedral and len(region.blocks_present) <= region.castle_points:

			util_dict[region.name] = 0

			for i,border in enumerate(board.dynamic_borders[region.regionID]):

				if border != 'X' and board.regions[i].blocks_present[0].allegiance == 'SCOTLAND':

					util_dict[region.name] += 1

	return util_dict


def disband_block_util(player,board,region):
	'''
	used when all important pieces have moved for winter
	checks to see if castle limits are infringed
	takes a player object,board object, and a region object
	returns a utility dictionary where more utility means higher
	chance of disbanding. also returns the number of keys that 
	need to be returned by the chancing function.
	'''



	util_dict = {}

	display_blocks = {}

	if region.blocks_present[0].allegiance == 'SCOTLAND':

			if region.cathedral:

				castle_points = region.castle_points + 1

			else:

				castle_points = region.castle_points

	else:

		if find_location(board,search.block_name_to_object(board.all_blocks,'EDWARD')) == region:

			castle_points = 100

		else:

			castle_points = region.castle_points

	for region_block in region.blocks_present:

		if type(region_block) != blocks.Noble:

			display_blocks.append(region_block)

	have_to_move = len(region.blocks_present) - castle_points

	if have_to_move > 0:
	
		for block in display_blocks:

			util_dict[block.blockID] = 0

			for i in range(4-block.current_strength):

				util_dict[block.blockID] += 1

			if block.attack_letter == 'A':

				util_dict[block.blockID] += 1

			elif block.attack_letter == 'B':

				util_dict[block.blockID] += 2

			elif block.attack_letter == 'C':

				util_dict[block.blockID] += 3

	return util_dict,have_to_move


def choose_what_to_do_util(player,board,region,rp):

	'''
	if computer is scottish, adss utility to bump up a troop or add reinforcement
	takes a player object,board object, region object, and replacement points integer for that region
	returns utility dictionary
	'''

	util_dict = {'b':0.01,'r':0.01}

	if len(region.blocks_present) > rp:

		util_dict['r'] += 1

	if search.block_name_to_object(board,'WALLACE') in region.blocks_present and search.block_name_to_object(board,'WALLACE').current_strength < search.block_name_to_object(board,'WALLACE').attack_strength:

		util_dict['b'] += 1

	if search.block_name_to_object(board,'KING') in region.blocks_present and search.block_name_to_object(board,'KING').current_strength < search.block_name_to_object(board,'KING').attack_strength:

		util_dict['b'] += 1

	if search.block_name_to_object(board,'EDWARD') in region.blocks_present and search.block_name_to_object(board,'EDWARD').current_strength < search.block_name_to_object(board,'EDWARD').attack_strength:

		util_dict['b'] += 1

	return util_dict


def choose_what_to_bump_util(player,block_list):

	util_dict = {}

	for block in block_list:

		util_dict[block.name] = 0

		if type(block) == blocks.Noble:

			util_dict[block.name] += 4

		elif block.name == 'WALLACE' or block.name == 'EDWARD' or block.name == 'KING':

			util_dict[block.name] += 1

		util_dict[block.name] += (block.attack_strength-block.current_strength)

	return util_dict
























