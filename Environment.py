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
        self._bullets = []

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
        movementMag = 500
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.player.move(pygame.Vector2(0,-movementMag))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.player.move(pygame.Vector2(0,movementMag))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.player.move(pygame.Vector2(-movementMag,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.player.move(pygame.Vector2(movementMag,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.player.rotateSprite(15)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.fire_bullet()
        return False
    
    def draw(self):
        positionRect = pygame.Rect(self._screenOffset, (self._worldDimensions.x,self._worldDimensions.y))
        #centres the Rect object around the Entities Position
        positionRect.move_ip(-self._worldDimensions.x/2, -self._worldDimensions.y/2)
        pygame.draw.rect(self._screen, WHITE, positionRect, 3)


        gridGap = 100
        for i in range(int(WORLD_WIDTH/gridGap)):
            xCoord = -(WORLD_WIDTH/2) + i * gridGap + self._screenOffset.x
            yCoord = (WORLD_HEIGHT/2)
            startPos = (xCoord, -yCoord + self._screenOffset.y)
            endPos = (xCoord, yCoord + self._screenOffset.y)
            pygame.draw.line(self._screen, GREY, startPos, endPos)
        for i in range(int(WORLD_HEIGHT/gridGap)):
            xCoord = (WORLD_WIDTH/2) 
            yCoord = (-WORLD_HEIGHT/2) + i * gridGap + self._screenOffset.y
            startPos = (-xCoord + self._screenOffset.x, yCoord)
            endPos = (xCoord + self._screenOffset.x, yCoord)
            pygame.draw.line(self._screen, GREY, startPos, endPos)

        for enemy in self._enemies:
            enemy.draw()

        self.player.draw()

        for bullet in self._bullets:
            bullet.draw()
    
    def update_enemy(self):
        playerPos = self.player.get_position()
        for enemy in self._enemies:
            enemy.move(playerPos)

    def update_physics(self, dt):
        mousePos = pygame.Vector2(pygame.mouse.get_pos())
        diffX = mousePos.x - WIDTH/2
        diffY = -(mousePos.y - HEIGHT/2)
        angle = math.degrees(math.atan2(diffY, diffX))
        self.player.setRotation(angle)

        self.player.update_physics(dt)
        for enemy in self._enemies:
            enemy.update_physics(dt)

        if len(self._bullets) > 0:
            for i in range(len(self._bullets)-1, 0-1, -1):
                self._bullets[i].update_physics(dt)
                if self._bullets[i].get_age() > 10:
                    self._bullets.pop(i)
        
        screenShift = self.player.get_velocity() * dt
        self._screenOffset -= screenShift
        self._worldCoordsAtScreenCentre = self.player.get_position()

    def get_bullets(self):
        return self._bullets

    