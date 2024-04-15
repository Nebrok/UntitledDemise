from constants import *

class Environment():
    def __init__(self):
        self._worldDimensions = pygame.Vector2(WORLD_WIDTH, WORLD_HEIGHT)
        self._screenOffset = pygame.Vector2(WIDTH/2, HEIGHT/2)
        self._worldCoordsAtScreenCentre = pygame.Vector2()
    
    def get_offset(self):
        return self._screenOffset
    
    def get_coords_at_centre(self):
        return self._worldCoordsAtScreenCentre