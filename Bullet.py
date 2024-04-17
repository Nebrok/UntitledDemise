from constants import *

class Bullet():
    def __init__(self, env, position, heading, initialVelocity):
        self._env = env

        #self._sprite = pygame.image.load("Assets/PlayerSprite.png")

        self._position = position
        self._velocity = (pygame.Vector2(1,0).rotate(heading) * BULLET_SPEED)
        self._velocity.y *= -1 
        self._velocity += initialVelocity
        self._acceleration = pygame.Vector2(0,0)
        self._rotation = 0
        self._heading = heading

        self._age = 0

        self._dimensions = pygame.Vector2(32,32)
    
    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(), BLUE, self._position + self._env.get_offset(), 5)

    def update_physics(self, dt):
        #self._velocity += self._acceleration * dt
        self._position += self._velocity * dt
        self._acceleration *= 0

        self._age += 1 * dt

    def get_age(self):
        return self._age

    def get_position(self):
        return self._position
    
    def get_velocity(self):
        return self._velocity