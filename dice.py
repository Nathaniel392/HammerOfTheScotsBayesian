import random
"""dice class"""
class Dice(object):
  @staticmethod
  def roll:
    return random.randint(6) + 1
