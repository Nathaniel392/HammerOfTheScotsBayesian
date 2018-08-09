import retreat
import regroup
import simulations
import search

def move_utility(board, block, start_regionid, end_regionid, is_stay, turn):
	"""
	returns between 0 and 1
	probability that it will choose again
	"""
	start_region = search.region_id_to_object(board, start_regionid)
	end_region = search.region_id_to_object(board, end_regionid)


	move_utility = 0
	if regroup.noble_home_to_object(board, start_regionid):
		if is_stay:
			move_utility += .4

	simulation_dict = simulations.simulation([block], end_region.blocks_present, list(), list())
	move_utility += retreat.retreat(board, end_regionid, [], simulation_dict, True, turn)['Staying value'] / 150


	if move_utility >= 1:
		move_utility = 0.8
	elif move_utility == 0:
		move_utility = 0.2



	return move_utility



	




	

	