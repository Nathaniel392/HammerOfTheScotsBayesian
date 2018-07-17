import random
"""dice class
it works"""
class Dice(object):
  @staticmethod
  def roll(num_dice):
    return random.randint(1 * num_dice, 6 * num_dice)
