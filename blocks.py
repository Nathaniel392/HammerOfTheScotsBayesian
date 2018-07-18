"""
blocks class
as well as noble class
"""
class Block(object):
    def __init__(self, name, movement_points, attack_letter, attack_number, attack_strength1, attack_strength2, attack_strength3 \
                attack_strength4):
        """
        name is name of object
        movement_points is movement points
        attack letter is A, B, or C
        attack_number is the number after the A or B or C
        attack_strength1 is weakest attack strength or 0 
        attack_strength4 is strongest attack strength
        current_strength is current strength
        
        """
        self.name = name
        self.movement_points = movement_points
        self.attack_letter = attack_letter
        self.attack_number = attack_number
        self.attack_strength1 = attack_strength1
        self.attack_strength2 = attack_strength2
        self.attack_strength3 = attack_strength3
        self.attack_strength4 = attack_strength4
        self.current_strength = attack_strength4
