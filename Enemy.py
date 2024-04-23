from constants import *

class Enemy():
    def __init__(self, env, startx, starty):
        self._env = env

        self._position = pygame.Vector2(startx, starty)
        self._velocity = pygame.Vector2()
        self._acceleration = pygame.Vector2()

        self._dimensions = pygame.Vector2(32,32)

        self._playerRelativeTarget = pygame.Vector2(0,0)
    
    def draw(self):
        positionRect = pygame.Rect(self._position + self._env.get_offset(), (self._dimensions.x,self._dimensions.y))
        #centres the Rect object around the Entities Position
        positionRect.move_ip(-self._dimensions.x/2, -self._dimensions.y/2)
        pygame.draw.ellipse(pygame.display.get_surface(), RED, positionRect)

    def update_physics(self, dt):
        self._velocity += self._acceleration * dt
        if self._velocity.magnitude() > ENEMY_MAX_SPEED:
            self._velocity.scale_to_length(ENEMY_MAX_SPEED)
        self._position += self._velocity * dt
        self._acceleration *= 0

    def move(self, playerPosition):
        positionDifference = (playerPosition + self._playerRelativeTarget - self._position 
                              + pygame.Vector2(randint(-10,10),randint(-10,10)))
        positionDifference.normalize()
        positionDifference *= 1
        self._acceleration += positionDifference
    
    def get_position(self):
        return self._position.copy()
    
    def get_dimensions(self):
        return self._dimensions.copy()