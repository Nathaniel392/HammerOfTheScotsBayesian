import board
import blocks

new_board = board.Board()

def find_borders(regionID):

	return_list = []

	for element in regionID:

		for i,border in enumerate(board.new_board.static_borders[element]):

			print (board.new_board.static_borders[element])

			if border == "B":

				return_list.append(i)

	return return_list


def check_path(num_moves,startID,endID):

	check_list = [startID]

	for i in range(num_moves):

		if endID in find_borders(check_list):

			return True

		else:

			check_list = find_borders(check_list)

	else:

		return False

print(check_path(3,2,3))




