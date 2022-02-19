import pygame
from support import import_folder
from settings import tile_size
from random import randint

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self,shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos,size)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, pos, size, path):
        super().__init__(pos,size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self, shift):
        super().update(shift)
        self.animate()

class Coin(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos,size, path)
        center_x = self.rect.x + tile_size / 2
        center_y = self.rect.y + tile_size / 2

        self.rect = self.image.get_rect(center = (center_x, center_y))

class Crate(StaticTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, None)
        x = pos[0]
        y = pos[1]
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(bottomleft = (x,y+tile_size))

class Palm(AnimatedTile):
    def __init__(self, pos, size, path, offset_y):
        super().__init__(pos, size, path)
        self.rect.y -= offset_y
