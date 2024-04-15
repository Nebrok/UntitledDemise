from constants import *
from Player import Player

class Environment():
    def __init__(self, screen):
        self._screen = screen
        self._worldDimensions = pygame.Vector2(WORLD_WIDTH, WORLD_HEIGHT)
        self._screenOffset = pygame.Vector2(WIDTH/2, HEIGHT/2)
        self._worldCoordsAtScreenCentre = pygame.Vector2()

        self.player = Player(self)

        #pygame system changes
        pygame.key.set_repeat(100)


    
    def get_offset(self):
        return self._screenOffset
    
    def get_coords_at_centre(self):
        return self._worldCoordsAtScreenCentre
    
    def update_events(self):
        """
        Loops through the entire pygame event queue. Returns True if
        the window is closed, otherwise returns False
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.player.move(pygame.Vector2(0,-1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.player.move(pygame.Vector2(0,1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.player.move(pygame.Vector2(-1,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.player.move(pygame.Vector2(1,0))
        
        return False
    
    def draw(self):
        self.player.draw()

    def update_physics(self, dt):
        self.player.update_physics(dt)

    