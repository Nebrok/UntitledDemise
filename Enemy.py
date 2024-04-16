from constants import *

class Enemy():
    def __init__(self, env, startx, starty):
        self._env = env

        self._position = pygame.Vector2(startx, starty)
        self._velocity = pygame.Vector2()
        self._acceleration = pygame.Vector2()

        self._dimensions = pygame.Vector2(32,32)
    
    def draw(self):
        positionRect = pygame.Rect(self._position + self._env.get_offset(), (self._dimensions.x,self._dimensions.y))
        #centres the Rect object around the Entities Position
        positionRect.move_ip(-self._dimensions.x/2, -self._dimensions.y/2)
        pygame.draw.ellipse(pygame.display.get_surface(), RED, positionRect)

    def update_physics(self, dt):
        self._velocity += self._acceleration
        self._position += self._velocity * dt
        self._acceleration *= 0

    def move(self, acceleration):
        self._acceleration += acceleration