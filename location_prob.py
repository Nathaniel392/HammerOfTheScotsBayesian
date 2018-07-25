#creates an array
#each row of the array represents a block ID
#each column of the array represents a region ID
#the values of the matrix are the probability that a particular block is in a region

def create_static_locations():

	fp = open('block_info.txt','r')

	fp.readline()

	static_locations = []

	for line in fp:

		block_locations = []

		line.strip()

		block_info = line.split()

		for i in range(25):

			if int(block_info[6]) == i:

				block_locations.append(1)

			else:

				block_locations.append(0)

		static_locations.append(block_locations) 

	fp.close()

	return static_locations


def main():
	create_static_locations()

if __name__ == '__main__':
	main()