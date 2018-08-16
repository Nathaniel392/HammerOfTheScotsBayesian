#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 16:12:07 2018

@author: amylvaganam
"""


'''
(both) infantry unit A > B > C
(both) downvote a noble that's going to be lost, prioritize infantry, before wintering ( big - )
(England) "near winter": infantry > archers + knights
(England) noble > non-noble when not going to lose
(both) jeopardy and hopeless ( - )
(both) homeland jeopardy ( + )
(England) Hobelars (++) - blocks that you can't get back, have 3 movement pts
(Scotland) noble > non-noble
(Scotland) if moray,norse,french knights < full, gets an up vote because he doesn't switch sides
(Scotland) cathedral locale
(Scotland) raid in jeopardy (+)
(England) scot pillage and adjacent pieces (+)
'''





import blocks
import weighted_prob
       




def victuals_utility(board, role):
    #decide whether you want to play victuals based on chosen region and block list
    region_dict = victuals_region_utility(board, role)
    chosen_region = weighted_prob.weighted_prob(region_dict)
    
    #choosing blocks to victual and adding them to victual_block_list
    victual_block_list = []
    
    blocks_dict = victuals_block_utility(chosen_region, role)
    victual_block_list.append(weighted_prob.weighted_prob(blocks_dict))
    
    blocks_dict = victuals_block_utility(chosen_region, role)
    victual_block_list.append(weighted_prob.weighted_prob(blocks_dict))
    
    blocks_dict = victuals_block_utility(chosen_region, role)
    victual_block_list.append(weighted_prob.weighted_prob(blocks_dict))
    
    utility_value = 0
    hits_taken = 0
    for block in victual_block_list:
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
        prob_dict[block] = block_utility
        
    return prob_dict