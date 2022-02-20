import pygame
from tiles import AnimatedTile
from random import randint
from settings import tile_size


class Enemy(AnimatedTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, 'graphics/enemy/run')
        self.rect = self.image.get_rect(bottomleft = (self.rect.left, self.rect.top+tile_size))
        self.speed = randint(3,5)
    
    def update_direction(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image,True,False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        super().update(shift)
        self.rect.x += self.speed
        self.update_direction()
        