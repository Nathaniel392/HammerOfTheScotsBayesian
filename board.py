
'''
0	Ross
1 	Garmoran
2	Moray
3	Strathspey
4	Buchan
5	Lochaber
6	Badenoch
7	Mar
8	Angus
9	Argyll
10	Atholl
11	Fife
12	Lennox
13	Mentieth
14	Carrick
15	Lanark
16	Lothian
17	Dunbar
18	Selkirk Forest
19	Galloway
20	Annan
21	Teviot
22	England
'''

NUM_REGIONS = 23


def read_file(file_name):
	'''

	'''

	# Open the file
	#try:
	fp = open(file_name, 'r')
	#except FileNotFoundError:
	#	print('File not found')
	
	output = []

	for line in fp:
		info = line.strip('\n')

		if file_name == 'castle_points.txt':
			output.append(int(info))

		else:	#borders or cath_coast
			row = info.strip().split()
			output.append(row)
	
	#List of information
	print(output)
	return output


class Board(object):
	
	def __init__(self):
		'''
		Reads in files on borders, cathedrals, coasts, and castle points
		'''
		self.static_borders = read_file('borders.txt')
		self.cath_coast = read_file('cath_coast.txt')
		self.castle_points = read_file('castle_points.txt')



def main():
	board = Board()


if __name__ == '__main__':
	main()









