import random
"""dice class
Dice.num_dice(num_dice) returns tuple of dice things
"""
dice_list = list()

def roll(num_dice):
    for i in range(num_dice):
        dice_list.append(random.randint(1,6))
    return tuple(dice_list)
 
    
