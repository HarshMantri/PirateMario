import pygame
from tiles import Tile, Palm, Coin, StaticTile, Crate
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from support import import_csv, cut_image
from settings import tile_size, screen_width

class Level:
    def __init__(self, screen, level_no):
        self.display_screen = screen
        self.world_shift = 0

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
        level_width = len(terrain_layout[0])*tile_size
        self.water = Water(30, level_width)
        self.clouds = Clouds(30,400, level_width)

        player_layout = import_csv(f'levels/{level_no}/player.csv')

        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout) 

        self.current_x = None

        self.dust_group = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
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
                            sprite = Palm((x,y),tile_size,'graphics/terrain/palm_small', 38)
                        if val == '1':
                            sprite = Palm((x,y),tile_size,'graphics/terrain/palm_large', 64)
                    if type == 'grass':
                        img_path = 'graphics/decoration/grass/grass.png'
                        surface_list = cut_image(img_path)
                        sprite = StaticTile((x,y), tile_size, surface_list[int(val)])
                    if type == 'enemies':
                        sprite = Enemy((x,y),tile_size)
                    if type == 'constraints':
                        sprite = Tile((x,y), tile_size)
                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self, tile_data):
        for r_idx, row in enumerate(tile_data):
            for c_idx, val in enumerate(row):
                x = c_idx * tile_size
                y = r_idx * tile_size
                if val == '0':
                    player_sprite = Player((x,y),self.display_screen, self.create_jump_particles)
                    self.player.add(player_sprite)
                elif val == '1':
                    goal_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    goal_sprite = StaticTile((x,y),tile_size,goal_surface)
                    self.goal.add(goal_sprite)
        
    def enemy_collision_constraints(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints,False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,5)
        else:
            pos += pygame.math.Vector2(10,-5)

        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_group.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player_sprite = self.player.sprite
        player_direction_x = player_sprite.direction.x
        player_sprite.rect.x += player_direction_x* player_sprite.speed
        collidable_sprite = self.terrain_group.sprites()+self.fg_palms.sprites()+self.crates_group.sprites()
        for sprite in collidable_sprite:
            if player_sprite.rect.colliderect(sprite.rect):
                if player_direction_x > 0:
                    player_sprite.rect.right = sprite.rect.left
                    player_sprite.on_right = True
                    self.current_x = player_sprite.rect.right
                elif player_direction_x < 0:
                    player_sprite.rect.left = sprite.rect.right
                    player_sprite.on_right = False
                    self.current_x = player_sprite.rect.left

        if player_sprite.on_left and (player_direction_x >= 0 or player_sprite.rect.left < self.current_x):
            player_sprite.on_left = False
        if player_sprite.on_right and (player_direction_x <= 0 or player_sprite.rect.right < self.current_x):
            player_sprite.on_right = False
        
    def vertical_mevement_collision(self):
        player_sprite = self.player.sprite
        player_sprite.apply_gravity()
        collidable_sprite = self.terrain_group.sprites()+self.fg_palms.sprites()+self.crates_group.sprites()
        for sprite in collidable_sprite:
            if player_sprite.rect.colliderect(sprite.rect):
                if player_sprite.direction.y > 0:
                    player_sprite.rect.bottom = sprite.rect.top
                    player_sprite.direction.y = 0
                    player_sprite.on_ground = True
                elif player_sprite.direction.y < 0:
                    player_sprite.rect.top = sprite.rect.bottom
                    player_sprite.direction.y = 0
                    player_sprite.on_ceiling = True

        if player_sprite.on_ground and (player_sprite.direction.y < 0 or player_sprite.direction.y > 1):
            player_sprite.on_ground = False
        if player_sprite.on_ceiling and (player_sprite.direction.y > 0):
            player_sprite.on_ceiling = False

    def scroll_x(self):
        player_sprite = self.player.sprite
        player_x = player_sprite.rect.x
        player_direction_x = player_sprite.direction.x

        if player_x < screen_width/4 and player_direction_x < 0:
            self.world_shift = 8
            player_sprite.speed = 0
        elif player_x > screen_width*3/4 and player_direction_x > 0:
            self.world_shift = -8
            player_sprite.speed = 0
        else:
            self.world_shift = 0
            player_sprite.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_group.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10,15)
            else:
                offset = pygame.math.Vector2(-10,15)
            landing_dust = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_group.add(landing_dust)

    def run(self):
        self.sky.draw(self.display_screen)
        self.clouds.draw(self.display_screen,self.world_shift)

        self.bg_palms.update(self.world_shift)
        self.bg_palms.draw(self.display_screen)

        self.terrain_group.update(self.world_shift)
        self.terrain_group.draw(self.display_screen)

        self.enemies.update(self.world_shift)
        self.constraints.update(self.world_shift)
        self.enemy_collision_constraints()
        self.enemies.draw(self.display_screen)
        
        self.crates_group.update(self.world_shift)
        self.crates_group.draw(self.display_screen)

        self.grass_group.update(self.world_shift)
        self.grass_group.draw(self.display_screen)     
        
        self.coin_group.update(self.world_shift)
        self.coin_group.draw(self.display_screen)

        self.fg_palms.update(self.world_shift)
        self.fg_palms.draw(self.display_screen)   

        self.dust_group.update(self.world_shift)
        self.dust_group.draw(self.display_screen)   
        
        self.player.update()
        self.horizontal_movement_collision()

        self.get_player_on_ground()
        self.vertical_mevement_collision()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_screen)

        self.goal.update(self.world_shift)
        self.goal.draw(self.display_screen)
        

        self.water.draw(self.display_screen)

        
        

        