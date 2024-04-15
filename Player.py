from constants import *

class Player():
    def __init__(self, env):
        self._env = env

        self._position = pygame.Vector2(self._env.get_coords_at_centre())
        self._velocity = pygame.Vector2()
        self._acceleration = pygame.Vector2()

        self._dimensions = pygame.Vector2(50,50)
    
    def draw(self):
        positionRect = pygame.Rect(self._position + self._env.get_offset(), (self._dimensions.x,self._dimensions.y))
        #centres the Rect object around Player Position
        positionRect.move_ip(-self._dimensions.x/2, -self._dimensions.y/2)
        pygame.draw.rect(pygame.display.get_surface(), WHITE, positionRect)

    def update_position(self):
        self._velocity += self._acceleration
        self._position += self._velocity
        self._acceleration *= 0

    def move(self, acceleration):
        self._acceleration += acceleration