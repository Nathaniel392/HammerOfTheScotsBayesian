#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 10:50:03 2018

@author: elliotmoore
"""

"""
initlizes blocks
"""

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
		info = line.strip()

		if file_name == 'block_info.txt':
			output.append(info)
	
	#List of information
	fp.close()
	return output

def reset_block(block, blockID):
    """
    resets a block
    returns nothing
    """
    fp = open('block_info.txt', 'r')
    for i, line in enumerate(fp):

        if i == blockID:
            specific_data = line.strip().split()
            if type(block) is Noble:
                block = blocks.Noble(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),\
                            specific_data[7], specific_data[8], specific_data[9])
            elif type(block) is Wallace:
                block = blocks.Wallace(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7])
            elif type(block) is Edward:
                block = blocks.Edward(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7])
            elif type(block) is ScottishKing:
                block = blocks.ScottishKing(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7])
            else:
                block = blocks.Block(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7])

def initialize_blocks():
    """
    This function initlializes all the block objects into two
    lists, one for all 14 nobles and the other for the rest
    of the infantry and other blocks
    """
    data = []
    data = read_file('block_info.txt')

    nobles = []
    other_blocks = []
    specific_data = []

    #Initialize Infantry, Knights, Archers Objects.
    for i in range(22):
        specific_data = data[i].split()
        
        other_blocks.append(blocks.Block(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7]))
    #Initilize Norse Object
    specific_data = data[22].split()
    other_blocks.append(blocks.Norse(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7]))
    #Initilize Celtic (Wales and Ulsher)
    for i in range(23, 26):
        specific_data = data[i].split()
        other_blocks.append(blocks.Celtic(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]), specific_data[7]))
    #Initialize Wallace Object
    specific_data = data[26].split()
    other_blocks.append(blocks.Wallace(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7]))

    #Initialize Edward Object
    specific_data = data[27].split()
    other_blocks.append(blocks.Edward(specific_data[0], int(specific_data[1]), specific_data[2], int(specific_data[3]), int(specific_data[4]), specific_data[5], int(specific_data[6]),specific_data[7]))

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
    return nobles, other_blocks

