from constants import *
from Player import Player
from Enemy import Enemy


class Environment():
    def __init__(self, screen):
        self._screen = screen
        self._worldDimensions = pygame.Vector2(WORLD_WIDTH, WORLD_HEIGHT)
        self._screenOffset = pygame.Vector2(WIDTH/2, HEIGHT/2)
        self._worldCoordsAtScreenCentre = pygame.Vector2()

        self._fontObject = pygame.font.Font(None, 50)

        self.player = Player(self)

        self._enemies = []
        self._bullets = []

        self._score = 0
        self._playerLives = 3
        self._lifeLostFlag = False
        self._gameOver = False

        for i in range(1):
            enemy = Enemy(self, randint(-400, 400), randint(-400, 400))
            self._enemies.append(enemy)

        #pygame system changes
        #Changes key press behaviour, where if key is held down registers as
        #new press after given milliseconds
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
        
        if self._lifeLostFlag:
            self._playerLives -= 1
            print("Life Lost")
            if self._playerLives == 0:
                print("GAME OVER!!")
                return True
            self.player.life_lost()
            self._lifeLostFlag = False
        
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
        coinflip = random()
        if coinflip <= 0.02:
            newEnemy = Enemy(self, randint(-HALF_WORLD_WIDTH, HALF_WORLD_WIDTH),
                              randint(-HALF_WORLD_HEIGHT,HALF_WORLD_HEIGHT))
            self._enemies.append(newEnemy)
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
            if self.player.collides(enemy):
                self._lifeLostFlag = True

        if len(self._bullets) > 0:
            for i in range(len(self._bullets)-1, 0-1, -1):
                self._bullets[i].update_physics(dt)
                if self._bullets[i].get_age() > 10:
                    self._bullets.pop(i)
                    continue
                for j in range(len(self._enemies)-1, 0-1, -1):
                    distance = self._bullets[i].get_position().distance_to(self._enemies[j].get_position())
                    if distance <= 21: #5 + 16 radi of bullet and enemy respectively
                        self._score += SCORE_INCREASE_ON_ENEMY_DEATH
                        self._enemies.pop(j)
                        self._bullets.pop(i)
                        break
        

        #Used to calculate the offset between world coordintates and the camera
        # view, required to properly display entities
        screenShift = self.player.get_velocity() * dt
        self._screenOffset = self.player.get_position() * -1 + (WIDTH/2, HEIGHT/2)
        self._worldCoordsAtScreenCentre = self.player.get_position()

    def get_bullets(self):
        return self._bullets

    def render_HUD(self):
        currentScore = str(self._score)
        scoreSurface = self._fontObject.render("Score: " + currentScore, True, WHITE)
        scoreSurfaceRect = scoreSurface.get_rect()
        scoreSurfaceRect.y = HEIGHT - scoreSurfaceRect.height
        scoreSurfaceRect.x += 5
        pygame.display.get_surface().blit(scoreSurface, scoreSurfaceRect)

        numLives = str(self._playerLives)
        livesSurface = self._fontObject.render("Lives: " + numLives, True, WHITE)
        livesSurfaceRect = livesSurface.get_rect()
        livesSurfaceRect.y = HEIGHT - livesSurfaceRect.height
        livesSurfaceRect.x += scoreSurfaceRect.width + 30
        pygame.display.get_surface().blit(livesSurface, livesSurfaceRect)