from constants import *
from Bullet import Bullet

class Player():
    def __init__(self, env):
        self._env = env

        self._sprite = pygame.image.load("Assets/PlayerSprite.png")

        self._position = pygame.Vector2(self._env.get_coords_at_centre())
        self._velocity = pygame.Vector2()
        self._acceleration = pygame.Vector2()
        self._rotation = 90

        self._dimensions = pygame.Vector2(32,32)
    
    def draw(self):
        finalSprite = pygame.transform.rotate(self._sprite, self._rotation - 90)
        rot_rect = finalSprite.get_rect(center = (WIDTH/2, HEIGHT/2))
        pygame.display.get_surface().blit(finalSprite, rot_rect)
            
    def rotateSprite(self, angle):
        self._rotation += angle
    
    def setRotation(self, angle):
        self._rotation = angle

    def update_physics(self, dt):
        self._velocity += self._acceleration * dt
        if self._velocity.magnitude() > PLAYER_MAX_SPEED:
            self._velocity.scale_to_length(PLAYER_MAX_SPEED)
        self._position += self._velocity * dt
        self._acceleration *= 0

    def move(self, acceleration):
        self._acceleration += acceleration

    def get_position(self):
        return self._position
    
    def get_velocity(self):
        return self._velocity
    
    def fire_bullet(self):
        new_bullet = Bullet(self._env, self._position.copy(), self._rotation, self._velocity.copy())
        self._env.get_bullets().append(new_bullet)