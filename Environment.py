from constants import *
from Player import Player
from Enemy import Enemy


class Environment():
    def __init__(self, screen):
        self._screen = screen
        self._worldDimensions = pygame.Vector2(WORLD_WIDTH, WORLD_HEIGHT)
        self._screenOffset = pygame.Vector2(WIDTH/2, HEIGHT/2)
        self._worldCoordsAtScreenCentre = pygame.Vector2()

        self.player = Player(self)

        self._enemies = []

        for i in range(10):
            enemy = Enemy(self, randint(-400, 400), randint(-400, 400))
            self._enemies.append(enemy)

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
        movementMag = 10
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.player.move(pygame.Vector2(0,-movementMag))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.player.move(pygame.Vector2(0,movementMag))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.player.move(pygame.Vector2(-movementMag,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.player.move(pygame.Vector2(movementMag,0))
        return False
    
    def draw(self):
        positionRect = pygame.Rect(self._screenOffset, (self._worldDimensions.x,self._worldDimensions.y))
        #centres the Rect object around the Entities Position
        positionRect.move_ip(-self._worldDimensions.x/2, -self._worldDimensions.y/2)
        pygame.draw.rect(self._screen, WHITE, positionRect, 3)

        
        self.player.draw()
        for enemy in self._enemies:
            enemy.draw()
    
    def update_enemy(self):
        playerPos = self.player.get_position()
        for enemy in self._enemies:
            enemy.move(playerPos)


    def update_physics(self, dt):
        self.player.update_physics(dt)
        for enemy in self._enemies:
            enemy.update_physics(dt)

        screenShift = self.player.get_velocity() * dt
        self._screenOffset -= screenShift
        self._worldCoordsAtScreenCentre = self.player.get_position()

    