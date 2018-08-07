#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug	7 08:54:45 2018

@author: amylvaganam
"""

import search
import blocks
import weighted_prob
import random

def sea_utility(board, role):

	#use move utility function
	return 0.5


def her_utility(board, role):
	'''
	###
	#CONSTANTS
	WINNING_THRESHOLD = .75
	UNSCATHED_UTILITY = 15
	COMBAT_UTILITY = 10
	NUM_SIMULATIONS = 1000
	FRIENDLY_UNITS_SCALAR = 2
	KING_UTILITY = 15
	###

	noble_to_steal = None
	
	#Find enemy regions
	if role == 'ENGLAND':
		enemy_role = 'SCOTLAND'
	else:
		enemy_role = 'ENGLAND'
	enemy_regions = board.get_controlled_regions(enemy_role)

	#Iterate through those regions to find nobles (not Moray)
	enemy_nobles = []
	for enemy_region in enemy_regions:

		#Check every block in the region
		for enemy_block in enemy_region:

			#Append enemy non moray nobles to the noble list
			if type(enemy_block) == blocks.Noble and enemy_block.name != 'MORAY':
				enemy_nobles.append(enemy_block)

	### TEMPORARY									###
	### random choice								###
	###												###
	noble_to_steal = random.choice(enemy_nobles)	###
	return noble_to_steal							###
	###												###
	###												###
	###												###

	###
	# Check each noble for their utility - store it into a dictionary
	###

	# FORMAT noble.name (string) : utility (int)
	utility_dict = {}

	for enemy_noble in enemy_nobles:

		utility = 0

		#Declaring variables here
		battle_outcome_util = 0
		final_position_util = 0
		king_possibility_util = 0


		###
		# Find the region that that noble is most likely to be in
		###

		#List of probabilities that a noble is in a region - indeces are regionIDs - find the most probable one
		noble_region_probability = loc_prob[enemy_noble.regionID]
		most_probable_region_index_list = computer_decisions.find_n_highest_indeces(noble_region_probability)

		likely_region = search.region_id_to_object(most_probable_region_index_list[0])

		#Look at the combat immediately after - run most probable enemies through a simulation
		num_blocks_in_region = len(enemy_noble_region.blocks_present)
		num_other_blocks = num_blocks_in_region - 1

		###
		# Check if you can actually win the fight after flipping the noble
		###

		#That noble is alone in the region -  no battle
		if num_blocks_in_region == 1:
			battle_outcome_util = UNSCATHED_UTILITY

			#Noble will have to fight after flipping
		else:

			#Find the 
			likely_blocks = computer_decisions.likely_blocks(board, region, loc_prob)

			#Possible error in previous calculations - lowers value of choosing this region (?)
			if enemy_noble not in likely_blocks:
				#
				# Do something here
				#
				#
				#
				#
				#
				#
				pass
			else:
				likely_blocks.remove(enemy_noble)


			###
			# Run a simulation with the most probable blocks in the area
			###

			#Temporarily flip the noble for the simulation
			enemy_noble.allegiance = enemy_role

			attack = [enemy_noble]
			defense = likely_blocks

			simulation_results = simulations.simulation(attack, defense, NUM_SIMULATIONS)
			win_rate = simulation_results['attacker wins'] / NUM_SIMULATIONS

			#Flip it back
			enemy_noble.allegiance = role

			#Value from 0-COMBAT_UTILITY, scaled by distance from the WINNING_THRESHOLD
			if win_rate > WINNING_THRESHOLD:
				battle_outcome_util = (win_rate - WINNING_THRESHOLD) / (1.0 - WINNING_THRESHOLD) * COMBAT_UTILITY

		#If the block has a high chance of successfully flipping and winning the battle
		if battle_outcome_util > 0:

			###
			# Look at the surrounding regions to see if it is in danger or in a good position
			###

			adjacent_regions = board.find_adjacent_regions_object(region)

			###
			###
			###	POTENTIAL CHANGES
			### - don't just check adjacent blocks - look at the strategic value of having a noble in that region,
			###	  and check all enemies that could potentially reach the noble's location and take it back
			###
			###

			#Count the friendly and enemy blocks nearby
			num_adjacent_friendly_blocks = 0
			num_adjacent_enemy_blocks = 0


			for adjacent_region in adjacent_regions:
				for block in adjacent_region.blocks_present:
					adjacent_blocks.append(block)

					if role == 'ENGLAND':
						if block.allegiance == 'ENGLAND':
							num_adjacent_friendly_blocks += 1
						else:
							num_adjacent_enemy_blocks += 1

					elif role == 'SCOTLAND':
						if block.allegiance == 'SCOTLAND':
							num_adjacent_friendly_blocks += 1
						else:
							num_adjacent_enemy_blocks += 1

			#More adjacent friends than enemies - set the utility
			final_position_util = (num_adjacent_friendly_blocks - num_adjacent_enemy_blocks) * FRIENDLY_UNITS_SCALAR

		###
		# UNCOMMENT THIS WHEN crown_king() IS FINISHED
		###
		#Check if herald should be used to take a potential king
		if enemy_noble.name == 'BRUCE' or enemy_noble.name == 'COMYN':
			crown_king = crown_king(board, role, hand, prob_info)
			#If this noble should be crowned, add utility
			if enemy_noble == crown_king:
				king_possiblity_util = KING_UTILITY


		###
		# Sum the utility and store it
		###
		utility = battle_outcome_util + final_position_util + king_possibility_util
		utility_dict[enemy_noble.name] = utility


	###
	# Process the utility dictionary
	###

	#Since the dictionary keys are names, store the best noble as a name
	noble_to_steal_name = enemy_nobles[0].name

	#Loop through the dictionary and find the noble with highest utility
	for enemy_noble_name, enemy_noble_utility in utility_dict.items():
		if enemy_noble_utility > utility_dict[noble_to_steal_name]:
			max_utility = enemy_noble_utility
			noble_to_steal_name = enemy_noble_name

	#Convert the noble from name to object
	noble_to_steal = search.block_name_to_object(board.all_blocks, noble_to_steal_name)

	#Final noble object
	return max_utility, noble_to_steal
	'''
	return 0.5


def vic_utility(board, role):
	"""
	evaluates the value of playing the victuals card with the chosen region and blocks
	"""
	
	
	#decide whether you want to play victuals based on chosen region and block list
	region_dict = victuals_region_utility(board, role)

	chosen_region_ID = weighted_prob.weighted_prob(region_dict)
	#convert from id to Region
	chosen_region = search.region_id_to_object(board, chosen_region_ID)
	
	#choosing blocks to victual and adding them to victual_block_list
	victual_block_list = []
	
	for counter in range(3):
		blocks_dict = victuals_block_utility(chosen_region, role)
		victual_block_list.append(weighted_prob.weighted_prob(blocks_dict))
	
	utility_value = 0
	hits_taken = 0
	for block_id in victual_block_list:
		block = search.block_id_to_object(board.all_blocks, block_id)
		#for scotland:
		#if block is king and he needs it
		if block.name == 'KING' and block.current_strength < block.attack_strength:
			utility_value += .5
		#if block is wallace and he needs it
		elif block.name == 'WALLACE' and block.current_strength < block.attack_strength:
			utility_value += .4
		#for england:
		#if block is edward and he needs it
		if block.name == 'EDWARD' and block.current_strength < block.attack_strength:
			utility_value += .45
		#if block is hobelars and he needs it
		elif block.name == 'HOBELARS' and block.current_strength < block.attack_strength:
			utility_value += .3
			
		#if block is type noble and he needs it
		elif type(block) == blocks.Noble and block.current_strength < block.attack_strength:
			utility_value += .25
		#if block is below full health
		elif block.current_strength < block.attack_strength:
			utility_value += .1
		
		hits_taken += block.attack_strength - block.current_strength
		
	#to maximize 3 healing points
	if hits_taken >= 3:
		utility_value += .25
	elif hits_taken == 2:
		utility_value += .1
			
	
	return utility_value, victual_block_list
		

def victuals_region_utility(board, role): #+ prob tables
	'''
	assigns values to different regions for victuals card based on blocks
	present and hits taken
	'''
	
	#list of friendly regions
	friendly_list = board.get_controlled_regions(role)

	# deciding where to play the card

	# assigning regions utilities
	prob_dict = dict()
	for region in friendly_list:
		hits_taken = 0
		region_utility = 0
		for block in region.blocks_present:
			
			#for scotland:
			#if king is below full health
			if block.name == 'KING' and block.current_strength < block.attack_strength:
				region_utility += .5
			#if wallace is below full health
			elif block.name == 'WALLACE' and block.current_strength < block.attack_strength:
				region_utility += .4
			#for england:
			#if edward is below full health
			if block.name == 'EDWARD' and block.current_strength < block.attack_strength:
				region_utility += .45
			#if hobelars is below full health
			elif block.name == 'HOBELARS' and block.current_strength < block.attack_strength:
				region_utility += .3
				
			#if noble is below full health
			elif type(block) == blocks.Noble and block.current_strength < block.attack_strength:
				region_utility += .25
			#if any other block is below full health
			elif block.current_strength < block.attack_strength:
				region_utility += .1
			else:
				region_utility += .00000001
			
			hits_taken += block.attack_strength - block.current_strength
		#to maximize 3 healing points
		if hits_taken >= 3:
			region_utility += .25
		elif hits_taken == 2:
			region_utility += .1
		
		prob_dict[region.regionID] = region_utility


	print('vicuals_region_utility: ' + str(prob_dict))
		
	return prob_dict
				
				
					
def victuals_block_utility(chosen_region, role): #+ prob tables	   
	'''
	assigns values to different blocks for victuals card based on importance of
	block and hits taken
	'''
	
			  
	prob_dict = dict()
	
	for block in chosen_region.blocks_present:
		block_utility = 0
		#if block is below max strength
		if block.current_strength < block.attack_strength:
			if block.name == 'KING':
				block_utility += .5
			elif block.name == 'WALLACE':
				block_utility += .4
			elif block.name == 'EDWARD':
				block_utility += .45
			elif block.name == 'HOBELARS':
				block_utility += .3
			elif type(block) == blocks.Noble:
				block_utility += .25
			else:
				block_utility += .1
		else:
			block_utility += 0.0000001
		prob_dict[block.blockID] = block_utility


	print('victuals_block_utility: ' + str(prob_dict))
		
	return prob_dict


def sum_health(board, region):

	"""
	region is regionid
	"""

	region = search.region_id_to_object(board, region)
	health_sum = 0
	for block in region.blocks_present:
		health_sum += block.current_strength
	return health_sum


def max_health(board, region):
	"""
	region is regionid
	"""

	region = search.region_id_to_object(board, region)
	health_sum = 0
	for block in region.blocks_present:
		health_sum += block.attack_strength
	return health_sum

def value_blocks(board, regionid):
	valuable_blocks = {'WALLACE':18, 'KING':22, 'EDWARD':16, 'HOBELARS':13}
	value = 0
	region = search.region_id_to_object(board, regionid)
	for block in region.blocks_present:
		if block.name in valuable_blocks:
			value += valuable_blocks[block.name]
	return value


			
def pil_utility(board, role):

	#make a list of possible opponent regions to be pillaged
	possible_pill_lst = []
	for region in board.get_controlled_regions(role):
		new_list = []
		new_list.append(region.regionID)
		for neighbor_region in board.find_all_borders(new_list):
			if not neighbor_region.is_friendly(role) and not neighbor_region.is_neutral() and neighbor_region not in possible_pill_lst:
				possible_pill_lst.append(neighbor_region)
				
	region_options = {}
				
	for region in possible_pill_lst:
		
		adjacent_regions = board.find_adjacent_regions_object(region)
		region_options[region.regionID] = tuple(adjacent_regions)
				
	utility_dict = dict()

	for region_id, friendly_region_tuple in region_options.items():
		for region_friendly in friendly_region_tuple:
			utility_dict[(region_id, region_friendly)] = 0



			#if enough things to pillage good
		
			if sum_health(board, region_id) >= 2:
				utility_dict[(region_id, region_friendly)] += .5
			elif sum_health(board, region_id) == 1: 
				utility_dict[(region_id, region_friendly)] += .1


			#takes friendly health into account
			if max_health(board, region_friendly.regionID) - sum_health(board,region_id) >= 2:
				utility_dict[region_id, region_friendly] += .5
			elif sum_health(board, region_id) == 1:
				utility_dict[(region_id, region_friendly)] += .1

			#value of enemy blocks and friendly blocks
			utility_dict[(region_id, region_friendly)] += value_blocks(board, region_id)
			utility_dict[(region_id, region_friendly)] += value_blocks(board, region_friendly.regionID)
		
		
		
	region_id_to_pillage, region_friendly_to_heal = weighted_prob.weighted_prob(utility_dict)

	return utility_dict[(region_id_to_pillage, region_friendly_to_heal)], region_id_to_pillage, region_friendly_to_heal

def tru_utility(board, comp_hand):

	if len(comp_hand) == 1:
		return 1.0
	else:
		return 0.0000001


	

