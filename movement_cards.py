import cards
"""
inherets card
movement card
not finshed
"""

class MovementCard(Card):
    def __init__(self, movement_points):
        self.movement_points = movement_points
    def __str__(self):
        if not self.hidden:
            return 'Movement card with ' , movement_points , ' movement points'
