import random
"""dice class
it works"""
dice_list = list()
class Dice(object):
    @staticmethod
    def roll(num_dice):
        for i in range(num_dice):
            dice_list.append(random.randint)
        return tuple(dice_list)
 
    
