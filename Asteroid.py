from constants import *
from Enemy import Enemy

class Asteroid(Enemy):
    def __init__(self, env, startX, startY):
        super().__init__(env, startX, startY)

        self._sprite = pygame.Surface.convert_alpha(pygame.image.load("Assets/AsteroidSprite.png"))
        self._rotation = 0
    
    def draw(self):
        finalSprite = pygame.transform.rotate(self._sprite, self._rotation)
        rot_rect = finalSprite.get_rect(center = self._position + self._env.get_offset())
        pygame.display.get_surface().blit(finalSprite, rot_rect)

    def update_physics(self, dt):
        self._velocity += self._acceleration * dt
        if self._velocity.magnitude() > ENEMY_MAX_SPEED:
            self._velocity.scale_to_length(ENEMY_MAX_SPEED)
        self._position += self._velocity * dt
        self._acceleration *= 0
        self._rotation = self._velocity.as_polar()[1]
    
    def move(self, playerPosition):
        """
        positionDifference = (playerPosition + self._playerRelativeTarget - self._position 
                              + pygame.Vector2(randint(-10,10),randint(-10,10)))
        positionDifference.normalize()
        positionDifference *= 1
        self._acceleration += positionDifference
        """
        pass
