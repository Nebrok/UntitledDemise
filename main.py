"""
Entry point for the game 'Untitled Demise'.
Project began on the 15/04/2024. Initially created as a work sample for
the author's application FutureGames Game Programmer course.
Github: https://github.com/Nebrok/UntitledDemise.git
Author: @Nebrok
"""
from constants import *
from Environment import Environment
from Player import Player


def main():
    pygame.init()
    pygame.font.init()

    SIZE = (WIDTH,HEIGHT)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Untitled Demise")

    done = False
    clock = pygame.time.Clock()
    screen.fill(BLACK)

    dt = 0
    gameEnvironment = Environment(screen)
    

    while not done:
        #Event Checking
        done = gameEnvironment.update_events()

        #Clears Screen
        screen.fill(BLACK)

        gameEnvironment.game_logic(dt)

        #End of Loop
        pygame.display.flip()
        #Delta time in seconds since last frame, clock.tick() also sets max framerate
        dt = clock.tick(60) / 1000
        print("FPS: " + str(clock.get_fps()))
    pygame.quit()

if __name__ == "__main__":
    main()