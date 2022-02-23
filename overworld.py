import pygame
from game_data import levels
from support import import_folder
from decoration import Sky

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, unlocked, level):
        super().__init__()
        self.frames = import_folder(f'graphics/overworld/{level}')
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.frames[self.frame_index]
        self.unlocked = unlocked
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.unlocked:
            self.animate()
        else:
            overlay_surf = self.image.copy()
            overlay_surf.fill('black',None,pygame.BLEND_RGBA_MULT)
            self.image.blit(overlay_surf, (0,0))

class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('graphics/overworld/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = self.pos)

    def update(self):
        self.rect.center = self.pos

class Overworld:
    def __init__(self, display_surface, start_level, max_level, create_level):

        # setup for overworld
        self.display_surface = display_surface
        self.current_level = start_level
        self.max_level = max_level
        self.moving = False
        self.icon_direction = pygame.math.Vector2(0,0)
        self.icon_speed = 8

        self.create_level = create_level

        # nodes setup
        self.setup_nodes()

        # icon setup
        self.setup_icon()

        self.sky = Sky(8,'overworld')

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for level_idx, level_data in enumerate(levels.values()):
            if level_idx <= self.max_level:
                node_sprite = Node(level_data['node_pos'],True,level_idx)
            else:
                node_sprite = Node(level_data['node_pos'],False, level_idx)
            self.nodes.add(node_sprite)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for idx, node in enumerate(levels.values()) if idx <= self.max_level]
            pygame.draw.lines(self.display_surface,'#a04f45',False,points,6)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.icon_direction = self.get_movement_vector(True)
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.icon_direction = self.get_movement_vector(False)
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)


    def get_movement_vector(self, moving_right):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if moving_right:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level+1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level-1].rect.center)

        return (end - start).normalize()

    def move_icon(self):
        if self.moving and self.icon_direction:
            self.icon.sprite.pos += self.icon_direction * self.icon_speed
            if self.icon.sprite.rect.collidepoint(self.nodes.sprites()[self.current_level].rect.center):
                self.icon.sprite.pos = self.nodes.sprites()[self.current_level].rect.center
                self.moving = False

    def run(self):
        self.get_input()
        self.nodes.update()
        self.move_icon()
        self.icon.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)