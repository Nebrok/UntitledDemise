from constants import *

class Bullet():
    def __init__(self, env, position, heading, initialVelocity, fired_by):
        self._env = env
        self._position = position
        self._velocity = (pygame.Vector2(1,0).rotate(heading) * BULLET_SPEED)
        self._velocity.y *= -1 
        self._velocity += initialVelocity
        self._acceleration = pygame.Vector2(0,0)
        self._rotation = 0
        self._heading = heading

        self._fired_by = fired_by

        self._age = 0

        self._dimensions = pygame.Vector2(10,10)
    
    def draw(self):
        colour = (40, 200, 40)
        if self._fired_by == "Player":
            colour = BLUE
        elif self._fired_by == "Alien Ship":
            colour = RED
        pygame.draw.circle(pygame.display.get_surface(), colour, self._position + self._env.get_offset(), 5)

    def update_physics(self, dt):
        self._velocity += self._acceleration * dt
        self._position += self._velocity * dt
        self._acceleration *= 0

        self._age += 1 * dt

    def get_age(self):
        return self._age

    def get_position(self):
        return self._position.copy()
    
    def get_velocity(self):
        return self._velocity.copy()
    
    def get_fired_by(self):
        return self._fired_by
    
    def get_dimensions(self):
        return self._dimensions