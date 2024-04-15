"""
Entry point for the game 'Untitled Demise'.
Project began on the 15/04/2024. Initially created as a work sample for
the author's application FutureGames Game Programmer course.
Github: https://github.com/Nebrok/UntitledDemise.git
Author: @Nebrok
"""
from constants import *
from Player import Player
from Environment import Environment


def main():
    pygame.init()

    SIZE = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Untitled Demise")

    done = False
    clock = pygame.time.Clock()
    screen.fill(BLACK)

    dt = 0

    gameSpace = Environment()

    testPlayer = Player(gameSpace)

    while not done:
        #Event Checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                testPlayer.move(pygame.Vector2(0,-1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                testPlayer.move(pygame.Vector2(0,1))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                testPlayer.move(pygame.Vector2(-1,0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                testPlayer.move(pygame.Vector2(1,0))

        #Clears Screen
        screen.fill(BLACK)

        testPlayer.update_position()
        testPlayer.draw()

        #Center of the screen
        pygame.draw.circle(screen, RED, (640,360), 2)

        #End of Loop
        pygame.display.flip()
        #Delta time in seconds since last frame, clock.tick() sets max framerate
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()