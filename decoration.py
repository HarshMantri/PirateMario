import pygame
from settings import screen_width, tile_size, num_vertical_tiles, screen_height
from support import import_folder
from  tiles import AnimatedTile, StaticTile
from random import choice, randint

class Sky:
    def __init__(self, horizon, style = 'level'):
        self.horizon = horizon

        self.sky_top = pygame.image.load('graphics/decoration/sky/sky_top.png').convert()
        self.sky_middle = pygame.image.load('graphics/decoration/sky/sky_middle.png').convert()
        self.sky_bottom = pygame.image.load('graphics/decoration/sky/sky_bottom.png').convert()

        self.sky_top = pygame.transform.scale(self.sky_top,(screen_width, tile_size))
        self.sky_middle = pygame.transform.scale(self.sky_middle,(screen_width, tile_size))
        self.sky_bottom = pygame.transform.scale(self.sky_bottom,(screen_width, tile_size))

        self.style = style
        if self.style == 'overworld':
            palm_surfaces = import_folder('graphics/overworld/palms')
            cloud_surfaces = import_folder('graphics/overworld/clouds')
            self.palms = []

            for surface in [choice(palm_surfaces) for i in range(10)]:
                x = randint(0, screen_width)
                y = self.horizon * tile_size+ randint(50,100)
                rect = surface.get_rect(midbottom = (x,y))

                self.palms.append((surface,rect))

            self.clouds = []
            for surface in [choice(cloud_surfaces) for i in range(10)]:
                x = randint(0, screen_width)
                y = randint(0,(self.horizon * tile_size) - 100)
                rect = surface.get_rect(midbottom = (x,y))

                self.clouds.append((surface,rect))



        
    def draw(self, screen):
        for i in range(num_vertical_tiles):
            y = i * tile_size
            if i < self.horizon:
                screen.blit(self.sky_top,(0,y))
            elif i == self.horizon:
                screen.blit(self.sky_middle,(0,y))
            else:
                screen.blit(self.sky_bottom,(0,y))

        if self.style == 'overworld':
            for palm in self.palms:
                screen.blit(palm[0],palm[1])
            for cloud in self.clouds:
                screen.blit(cloud[0],cloud[1])

        

class Water:
    def __init__(self, height, level_width):
        image_width = 192
        max_x = level_width+screen_width
        min_x = -level_width
        total_x_size = (max_x - min_x)
        num_tiles = int(total_x_size / image_width)+1
        self.water_tiles_group = pygame.sprite.Group()

        for i in range(num_tiles):
            x = i*image_width + min_x
            y = screen_height - height
            sprite = AnimatedTile((x,y),image_width,'graphics/decoration/water')
            self.water_tiles_group.add(sprite)

    def draw(self, screen):
        self.water_tiles_group.update(0)
        self.water_tiles_group.draw(screen)

class Clouds:
    def __init__(self, cloud_count, horizon, level_width):
        self.cloud_sprite = pygame.image.load('graphics/decoration/clouds/1.png')
        self.cloud_group = pygame.sprite.Group()
        y_min = 10
        y_max = horizon - 90

        x_min = -screen_width
        x_max = level_width + screen_width
        for i in range(cloud_count):
            sprite = StaticTile((randint(x_min, x_max),randint(y_min,y_max)),0
            ,self.cloud_sprite)
            self.cloud_group.add(sprite)

    def draw(self, screen, shift):
        self.cloud_group.update(shift)
        self.cloud_group.draw(screen)
