import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()
        if type == 'jump':
            self.frames = import_folder('graphics/character/dust_particles/jump')
        elif type == 'land':
            self.frames = import_folder('graphics/character/dust_particles/land')
        elif type == 'explosion':
            self.frames = import_folder('graphics/enemy/explosion')
        self.frame_index = 0
        self.animation_speed = 0.5
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]


    def update(self, shift):
        self.animate()
        self.rect.x += shift