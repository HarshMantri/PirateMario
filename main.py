import pygame, sys
from settings import *
from overworld import Overworld
from level import Level

class Game:
    def __init__(self):
        self.max_level = 0
        self.overworld = Overworld(screen, 0, self.max_level, self.create_level)
        self.state = 'overworld'

    def create_level(self, current_level):
        self.level = Level(screen, current_level, self.create_overworld)
        self.state = 'level'

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(screen, current_level, self.max_level, self.create_level)
        self.state = 'overworld'

    def run(self):
        if self.state == 'overworld':
            self.overworld.run()
        else:
            self.level.run()


pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Mario')
clock = pygame.time.Clock()

game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
    screen.fill('grey')
    game.run()

    pygame.display.update()
    clock.tick(60)
