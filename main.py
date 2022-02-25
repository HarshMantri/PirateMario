import pygame, sys
from settings import *
from overworld import Overworld
from level import Level
from ui import UI

class Game:
    def __init__(self):
        self.max_level = 0

        # audio
        self.level_bgmusic = pygame.mixer.Sound('audio/level_music.wav')
        self.overworld_bgmusic = pygame.mixer.Sound('audio/overworld_music.wav')

        self.overworld = Overworld(screen, 0, self.max_level, self.create_level)
        self.state = 'overworld'
        self.overworld_bgmusic.play(loops=-1)

        self.max_health = 100
        self.curr_health = 100
        self.coins = 0
        self.ui = UI(screen)

    def create_level(self, current_level):
        self.level = Level(screen, current_level, self.create_overworld, self.update_coins, self.damage_player)
        self.state = 'level'
        self.overworld_bgmusic.stop()
        self.level_bgmusic.play(loops=-1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(screen, current_level, self.max_level, self.create_level)
        self.state = 'overworld'
        self.level_bgmusic.stop()
        self.overworld_bgmusic.play(loops=-1)

    def update_coins(self, amount):
        self.coins += amount

    def damage_player(self, amount):
        self.curr_health += amount

    def check_game_over(self):
        if self.curr_health <= 0:
            self.curr_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(screen, 0, self.max_level, self.create_level)
            self.state = 'overworld'
            self.level_bgmusic.stop()
            self.overworld_bgmusic.play(loops=-1)

    def run(self):
        if self.state == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.draw_health_bar(self.curr_health, self.max_health)
            self.ui.draw_coins(self.coins)
            self.check_game_over()


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
