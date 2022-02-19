import pygame
from tiles import Tile, Palm, Coin, StaticTile, Crate
from enemy import Enemy
from decoration import Sky, Water, Clouds
from support import import_csv, cut_image
from settings import tile_size

class Level:
    def __init__(self, screen, level_no):
        self.display_screen = screen
        self.world_shift = -1

        terrain_layout = import_csv(f'levels/{level_no}/terrain.csv')
        self.terrain_group = self.get_sprite_group(terrain_layout,'terrain')

        coin_layout = import_csv(f'levels/{level_no}/coins.csv')
        self.coin_group = self.get_sprite_group(coin_layout,'coins')

        crates_layout = import_csv(f'levels/{level_no}/crates.csv')
        self.crates_group = self.get_sprite_group(crates_layout,'crates')

        bg_palms_layout = import_csv(f'levels/{level_no}/bg_palms.csv')
        self.bg_palms = self.get_sprite_group(bg_palms_layout,'bg_palms')

        fg_palms_layout = import_csv(f'levels/{level_no}/fg_palms.csv')
        self.fg_palms = self.get_sprite_group(fg_palms_layout,'fg_palms')

        grass_layout = import_csv(f'levels/{level_no}/grass.csv')
        self.grass_group = self.get_sprite_group(grass_layout,'grass')

        enemy_layout = import_csv(f'levels/{level_no}/enemies.csv')
        self.enemies = self.get_sprite_group(enemy_layout,'enemies')

        constraint_layout = import_csv(f'levels/{level_no}/constraints.csv')
        self.constraints = self.get_sprite_group(constraint_layout,'constraints')

        self.sky = Sky(8)
        self.water = Water(40)
        level_width = len(terrain_layout[0])*tile_size
        self.clouds = Clouds(30,512, level_width)
        
    def get_sprite_group(self, tile_data, type): 
        sprite_group = pygame.sprite.Group()

        for row_idx, row in enumerate(tile_data):
            for col_idx, val in enumerate(row):
                if val != '-1':
                    x = col_idx * tile_size
                    y = row_idx * tile_size
                    if type == 'terrain':
                        img_path = 'graphics/terrain/terrain_tiles.png'
                        surface_list = cut_image(img_path)
                        sprite = StaticTile((x,y), tile_size, surface_list[int(val)])
                    if type == 'coins':
                        if val == '0':
                            sprite = Coin((x,y),tile_size,'graphics/coins/gold')
                        else:
                            sprite = Coin((x,y),tile_size,'graphics/coins/silver')
                    if type == 'crates':
                        sprite = Crate((x,y),tile_size,'graphics/terrain/crate.png')
                    if type == 'bg_palms':
                        sprite = Palm((x,y),tile_size,'graphics/terrain/palm_bg', 64)
                    if type == 'fg_palms':
                        if val == '0': 
                            sprite = Palm((x,y),tile_size,'graphics/terrain/palm_small', 64)
                        if val == '1':
                            sprite = Palm((x,y),tile_size,'graphics/terrain/palm_large', 64)
                    if type == 'grass':
                        img_path = 'graphics/decoration/grass/grass.png'
                        surface_list = cut_image(img_path)
                        sprite = StaticTile((x,y), tile_size, surface_list[int(val)])
                    if type == 'enemies':
                        sprite = Enemy((x,y),tile_size,'graphics/enemy/run')
                    if type == 'constraints':
                        sprite = Tile((x,y), tile_size)
                    sprite_group.add(sprite)
        return sprite_group

    def enemy_collision_constraints(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints,False):
                enemy.reverse()


    def run(self):
        self.sky.draw(self.display_screen)
        self.clouds.draw(self.display_screen,self.world_shift)

        self.bg_palms.update(self.world_shift)
        self.bg_palms.draw(self.display_screen)

        self.terrain_group.update(self.world_shift)
        self.terrain_group.draw(self.display_screen)
        
        self.grass_group.update(self.world_shift)
        self.grass_group.draw(self.display_screen)

        self.crates_group.update(self.world_shift)
        self.crates_group.draw(self.display_screen)
        
        self.coin_group.update(self.world_shift)
        self.coin_group.draw(self.display_screen)

        self.fg_palms.update(self.world_shift)
        self.fg_palms.draw(self.display_screen)      

        self.enemies.update(self.world_shift)
        self.constraints.update(self.world_shift)
        self.enemy_collision_constraints()
        self.enemies.draw(self.display_screen)

        self.water.draw(self.display_screen)
        

        