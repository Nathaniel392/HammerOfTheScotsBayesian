import random
"""dice 
Dice.num_dice(num_dice) returns tuple of dice things
"""

def roll(num_dice):
	dice_list = list()
	for i in range(num_dice):
		dice_list.append(random.randint(1,6))
	return dice_list
 
    
