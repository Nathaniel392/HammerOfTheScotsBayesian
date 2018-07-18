"""
blocks class
as well as noble class
"""
class Block(object):
    def __init__(self, name, movement_points, attack_letter, attack_number, attack_strength1, attack_strength2, attack_strength3 \
                attack_strength4, location):
        """
        name is name of object
        movement_points is movement points
        attack_letter is A, B, or C
        attack_number is the number after the A or B or C
        attack_strength1 is weakest attack strength or 0 
        attack_strength4 is strongest attack strength
        current_strength is current strength
        location is a Region object
        """
        self.name = name
        self.movement_points = movement_points
        self.attack_letter = attack_letter
        self.attack_number = attack_number
        self.attack_strength = list(attack_strength1, attack_strength2, attack_strength3, attack_strength4)
        self.current_strength = attack_strength4
        self.location = location
    def get_hurt(self, damage):
        """
        returns False if block is dead
        otherwise returns True and damages block
        """
        if self.current_strength == self.attack_strength[0] or self.current_strength == 1:
            return False
        else:
            for i, strength in enumerate(self.attack_strength):
                if self.current_strength = strength:
                    self.current_strength = attack_strength[i - 1]
                    return True
    def heal(self, health_points):
        """
        returns False if cannot heal by that many points
        otherwise returns True and heals block
        """
        for i, strength in enumerate(self.attack_strength):
            if self.current_strength = strength:
                if i + health_points - 1 > len(self.attack_strength):
                    return False
                else:
                    self.current_strength = self.attack_strength[i + health_points]
                    return True
