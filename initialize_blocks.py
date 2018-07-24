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
    Reads a file and 
	'''

	# Open the file
	#try:
	fp = open(file_name, 'r')
	#except FileNotFoundError:
	#	print('File not found')
	
	output = []
	fp.readline()
	for line in fp:
		info = line.strip()
		output.append(info)
	
	# (2D) list of information from file
	fp.close()
	return output


def initialize_blocks():
    '''

    '''
    block_list = []
    block_stats = read_file('block_stats.txt')

    # Read in information about each block
    for info_line in block_stats:
        name = info_line[0]
        movement_points = info_line[1]
        attack_letter = info_line[2]
        attack_number = info_line[3]
        attack_strength = info_line[4]
        block_type = info_line[5]
        cross = info_line[6]
        block_id = info_line[7]

        # Add the home attribute if it's a noble
        if block_type == 'BRUCE' or block_type == 'COMYN':
            home = info_line[8]





def initialize_blocks_braveheart():
    """
    This function initializes all the block objects into two
    lists, one for all 14 nobles and the other for the rest
    of the infantry and other block
    """
    #Creates a list of every block potentially in the game
    data = []
    data = read_file('block_stats.txt')
    for entry in data:



    nobles = []
    other_blocks = []
    specific_data = []

    #Initialize Infantry, Knights, Archers Objects.
    for i in range(22):
        specific_data = data[i].split()

        for index, item in enumerate(specific_data):
            if type(item) is int:
                specific_data[index] = int(item)
        
        other_blocks.append(blocks.Block(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6], specific_data[7], specific_data[8]))
        #other_blocks.append(blocks.Block(for data in specific_data))
    #Initilize Norse Object
    specific_data = data[22].split()
    other_blocks.append(blocks.Norse(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6], specific_data[7]))
    #Initilize Celtic (Wales and Ulsher)
    for i in range(23, 26):
        specific_data = data[i].split()
        other_blocks.append(blocks.Celtic(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6], specific_data[7], specific_data[8]))
    #Initialize Wallace Object
    specific_data = data[26].split()
    other_blocks.append(blocks.Wallace(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6], specific_data[7]))

    #Initialize Edward Object
    specific_data = data[27].split()
    other_blocks.append(blocks.Edward(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6], specific_data[7]))

    #Initialize Scottish King Object
    specific_data = data[28].split()
    other_blocks.append(blocks.ScottishKing(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6], specific_data[7]))

    #Initialize Noble Objects
    for i in range(14):
        i+=29
        specific_data = data[i].split()
        nobles.append(blocks.Noble(specific_data[0], specific_data[1], specific_data[2], specific_data[3], specific_data[4], specific_data[5], specific_data[6],    \
                            specific_data[7], specific_data[8], specific_data[9]))
        i-=29

    static_nobles = copy.deepcopy(nobles)
    static_other_blocks = copy.deepcopy(other_blocks)
        
    return nobles, other_blocks, static_nobles, static_other_blocks

def initialize_blocks_bruce():
    """
    This function initlializes all the block objects into two
    lists, one for all 13 nobles and the other for the rest
    of the infantry and other blocks
    """
    data = []
    data = read_file('block_info_bruce.txt')

    nobles = []
    other_blocks = []
    specific_data = []

    #Initialize Infantry, Knights, Archers Objects.
    for i in range(22):
        specific_data = data[i].split()
        
        other_blocks.append(blocks.Block(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7], specific_data[8]))
    #Initilize Norse Object
    specific_data = data[22].split()
    other_blocks.append(blocks.Norse(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7]))
    #Initilize Celtic (Wales and Ulsher)
    for i in range(23, 26):
        specific_data = data[i].split()
        other_blocks.append(blocks.Celtic(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7], specific_data[8]))
    #Initialize Wallace Object
    specific_data = data[26].split()
    other_blocks.append(blocks.Wallace(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7]))

    #Initialize Edward Object
    specific_data = data[27].split()
    other_blocks.append(blocks.Edward2(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7]))

    #Initialize Scottish King Object
    specific_data = data[28].split()
    other_blocks.append(blocks.ScottishKing(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7]))

    #Initialize Noble Objects
    for i in range(14):
        i+=29
        specific_data = data[i].split()
        nobles.append(blocks.Noble(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),\
                            specific_data[7], specific_data[8], specific_data[9]))
        i-=29

    static_nobles = copy.deepcopy(nobles)
    static_other_blocks = copy.deepcopy(other_blocks)
        
    return nobles, other_blocks, static_nobles, static_other_blocks

						
						



