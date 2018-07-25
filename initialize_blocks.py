#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:50:03 2018

@author: elliotmoore
"""

"""
initlizes blocks
"""
import copy
import blocks

def read_file(file_name):
	'''
  
	'''

	# Open the file
	#try:
	fp = open(file_name, 'r')
	#except FileNotFoundError:
	#	print('File not found')
	
	output = []
	fp.readline()
	for line in fp:
		info = line.strip().split()
		output.append(info)
	
	#List of information
	fp.close()
	return output


def initialize_blocks():
	'''
	Initialized all blocks into one list
	Returns:  List of all blocks in the game, with no alliegance
	'''
	block_list = []
	block_stats = read_file('block_stats.txt')

	# Read in information about each block
	for line_num, line in enumerate(block_stats):

		#Convert to ints, bools, and tuples
		for index, info in enumerate(line):

			#Ints
			if info.isdigit():
				block_stats[line_num][index] = int(info)

			#Booleans
			elif info == 'T':
				block_stats[line_num][index] = True

			elif info == 'F':
				block_stats[line_num][index] = False
			
			#Tuples
			elif info[0] == '(':    #For Bruce and Comyn
				temp = info
				temp = temp.strip('()').split(',')
				for i, element in enumerate(temp): #Should be tuple of integers
					temp[i] = int(element)
				block_stats[line_num][index] = tuple(temp)


		#store information from line
		name = line[0]
		movement_points = line[1]
		attack_letter = line[2]
		attack_number = line[3]
		attack_strength = line[4]
		block_type = line[5]
		cross = line[6]
		block_id = line[7]

		# Check if it's a noble
		if block_type == 'BRUCE' or block_type == 'COMYN':
			is_noble = True

			# Set up noble homes
			home = line[8]

			# Assign noble loyalty
			loyalty = block_type
			temp_block = blocks.Noble(name, movement_points, attack_letter, attack_number, attack_strength, cross, block_id, home, loyalty)

		else:
			is_noble = False
			temp_block = blocks.Block(name, movement_points, attack_letter, attack_number, attack_strength, cross, block_type, block_id)

		#Finished block - no alliegence yet
		block_list.append(temp_block)

	return block_list

def main():
	initialize_blocks()

if __name__ == '__main__':
	main()	
						



