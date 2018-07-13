"""
country class
just to throw error if invalid country
country is a str
idk what's going on
"""
class Country(object):
  def __init__(self, team):
    if team.lower() == 'england':
      self.country = 'england'
    elif team.lower() == 'scotland'
      self.country = 'scotland'
    else:
      raise NotValidCountry("not valid country")
