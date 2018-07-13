import random
"""dice class
it works"""
class Dice(object):
  @staticmethod
  def roll():
    return random.randint(1, 6)
