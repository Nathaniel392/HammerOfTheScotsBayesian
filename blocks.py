import country
"""
blocks class
idk what this game is about
not finished
"""
class Block(class):
  def __init__(self, movement_points, strength, country_str):
    self.movement_points = movement_points
    self.strength = strength
    self.country = country.Country(country_str)
