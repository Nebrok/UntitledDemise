from constants import *
from Player import Player
from Enemy import Enemy
from Asteroid import Asteroid


class Environment():
    def __init__(self, screen):
        self._screen = screen
        self._worldDimensions = pygame.Vector2(WORLD_WIDTH, WORLD_HEIGHT)
        self._screenOffset = pygame.Vector2(WIDTH/2, HEIGHT/2)
        self._worldCoordsAtScreenCentre = pygame.Vector2()

        self._fontHUD = pygame.font.Font(None, 50)
        self._fontTitle = pygame.font.Font(None, 100)
        self._fontInfo = pygame.font.Font(None, 30)

        self.gameStates = ["Start", "Run", "End"]
        self.gameState = 0

        self.player = Player(self)

        self._enemies = []
        self._bullets = []

        self._score = 0
        self._playerLives = 3
        self._lifeLostFlag = False
        self._gameOver = False

        self._backgroundImage = pygame.Surface.convert_alpha(pygame.image.load("Assets/Spacebackground.png"))

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

        srtFlag = False
        runFlag = False
        endFlag = False
        if self.gameState == 0:
            srtFlag = True
            runFlag = False
            endFlag = False
        elif self.gameState == 1:
            srtFlag = False
            runFlag = True
            endFlag = False
        elif self.gameState == 2:
            srtFlag = False
            runFlag = False
            endFlag = True

        movementMag = 500
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.gameState = 2
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and srtFlag:
                self.gameState = 1
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and endFlag:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w and runFlag:
                self.player.move(pygame.Vector2(0,-movementMag))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and runFlag:
                self.player.move(pygame.Vector2(0,movementMag))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and runFlag:
                self.player.move(pygame.Vector2(-movementMag,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d and runFlag:
                self.player.move(pygame.Vector2(movementMag,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and runFlag:
                self.player.rotateSprite(15)
            if event.type == pygame.MOUSEBUTTONDOWN and runFlag:
                self.player.fire_bullet()
        
        if self._lifeLostFlag:
            self._playerLives -= 1
            if self._playerLives == 0:
                self.gameState = 2
            self.player.life_lost()
            self._lifeLostFlag = False
        
        return False
    
    def draw(self):
        positionRect = pygame.Rect(self._screenOffset, (self._worldDimensions.x,self._worldDimensions.y))
        #centres the Rect object around the Entities Position
        positionRect.move_ip(-self._worldDimensions.x/2, -self._worldDimensions.y/2)
        pygame.draw.rect(self._screen, WHITE, positionRect, 3)

        #uncomment to draw space image to background 
        #rot_rect = self._backgroundImage.get_rect(center = self._screenOffset)
        #pygame.display.get_surface().blit(self._backgroundImage, rot_rect)

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
            newEnemy = Asteroid(self, randint(-HALF_WORLD_WIDTH, HALF_WORLD_WIDTH),
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
        scoreSurface = self._fontHUD.render("Score: " + currentScore, True, WHITE)
        scoreSurfaceRect = scoreSurface.get_rect()
        scoreSurfaceRect.y = HEIGHT - scoreSurfaceRect.height
        scoreSurfaceRect.x += 5
        pygame.display.get_surface().blit(scoreSurface, scoreSurfaceRect)

        numLives = str(self._playerLives)
        livesSurface = self._fontHUD.render("Lives: " + numLives, True, WHITE)
        livesSurfaceRect = livesSurface.get_rect()
        livesSurfaceRect.y = HEIGHT - livesSurfaceRect.height
        livesSurfaceRect.x += scoreSurfaceRect.width + 30
        pygame.display.get_surface().blit(livesSurface, livesSurfaceRect)

    def game_logic(self, dt):
        if self.gameState == 0:
            self.start_game()
        elif self.gameState == 1:
            self.run_game(dt)
        elif self.gameState == 2:
            self.end_game()
        else:
            print("Invalid Game State flag")

    def render_start_display(self):
        titleSurface = self._fontTitle.render("UNTITLED DEMISE", True, WHITE)
        titleSurfaceRect = titleSurface.get_rect(center=(int(WIDTH/2), int(HEIGHT/3)))
        pygame.display.get_surface().blit(titleSurface, titleSurfaceRect)

        infoSurface = self._fontInfo.render("Press any button to start the game", True, WHITE)
        infoSurfaceRect = infoSurface.get_rect(center=(int(WIDTH/2), int(HEIGHT/2)))
        pygame.display.get_surface().blit(infoSurface, infoSurfaceRect)

    def start_game(self):
        self.render_start_display()

    def run_game(self, dt):
        self.update_enemy()
        self.update_physics(dt)

        self.draw()
        self.render_HUD()

    def render_end_display(self):
        tauntSurface = self._fontTitle.render("GAME OVER!", True, WHITE)
        tauntSurfaceRect = tauntSurface.get_rect(center=(int(WIDTH/2), int(HEIGHT/3)))
        pygame.display.get_surface().blit(tauntSurface, tauntSurfaceRect)

        currentScore = str(self._score)
        scoreSurface = self._fontInfo.render("Final Score: " + currentScore, True, WHITE)
        scoreSurfaceRect = scoreSurface.get_rect(center=(int(WIDTH/2), int(HEIGHT/2)))
        pygame.display.get_surface().blit(scoreSurface, scoreSurfaceRect)

        infoSurface = self._fontInfo.render("Press any button to end the game", True, WHITE)
        infoSurfaceRect = infoSurface.get_rect(center=(int(WIDTH/2), int(HEIGHT/2) + scoreSurfaceRect.h + 10))
        pygame.display.get_surface().blit(infoSurface, infoSurfaceRect)

    def end_game(self):
        self.render_end_display()