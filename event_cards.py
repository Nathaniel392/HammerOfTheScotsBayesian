import cards
"""
event cards inheret freom Card
not finished
"""
class EventCard(Card):
    def __init__(self, text):
        self.text = text
    def __str__(self):
        if not self.hidden:
            return self.text
   
