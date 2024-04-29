from constants import *
from Enemy import Enemy
from Bullet import Bullet

class AlienShip(Enemy):
    def __init__(self, env, startX, startY):
        super().__init__(env, startX, startY)

        self._sprite = pygame.Surface.convert_alpha(pygame.image.load("Assets/AlienShipSprite.png"))
        self._rotation = 0
    
    def draw(self):
        finalSprite = pygame.transform.rotate(self._sprite, self._rotation - 90)
        rot_rect = finalSprite.get_rect(center = self._position + self._env.get_offset())
        pygame.display.get_surface().blit(finalSprite, rot_rect)

    def move(self, playerPosition):
        positionDifference = (playerPosition + self._playerRelativeTarget - self._position 
                              + pygame.Vector2(randint(-10,10),randint(-10,10)))
        positionDifference.normalize()
        positionDifference *= 1
        self._acceleration += positionDifference

        distance_to_player = self._position.distance_to(playerPosition)
        if distance_to_player < 250 and self._event_timer >= 2:
            self.fire_bullet()
            self._event_timer = 0
    
    def fire_bullet(self):
        bullet_offset = pygame.Vector2(0,0)
        bullet_offset.x = math.cos(math.radians(self._rotation)) * 40
        bullet_offset.y = math.sin(math.radians(self._rotation)) * 40 * -1
        new_bullet = Bullet(self._env, self._position.copy() + bullet_offset, self._rotation, self._velocity.copy(), "Alien Ship")
        self._env.get_bullets().append(new_bullet)

