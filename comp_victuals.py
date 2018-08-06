#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:12:07 2018

@author: amylvaganam
"""

import blocks
                    
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
            
            hits_taken += block.attack_strength - block.current_strength
        #to maximize 3 healing points
        if hits_taken >= 3:
            region_utility += .25
        elif hits_taken == 2:
            region_utility += .1
        
        prob_dict[region] = region_utility
        
    return prob_dict
                
                
                    
def victuals_block_utility(chosen_region, role): #+ prob tables    
    '''
    assigns values to different blocks for victuals card based on importance of
    block and hits taken
    '''
    
    #making list of blocks that have been hit
    below_max_blocks = []
    for block in chosen_region.blocks_present:
            if block.current_strength < block.attack_strength:
                below_max_blocks.append(block)
              
                
    prob_dict = dict()
    
    for block in below_max_blocks:
        block_utility = 0
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
        prob_dict[block] = block_utility
        
    return prob_dict