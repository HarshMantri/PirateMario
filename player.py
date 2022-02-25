import pygame
from support import import_folder
from math import sin

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, create_jump_particles, damage_player):
        super().__init__()
        self.frames = {}
        self.frames['idle'] = import_folder('graphics/character/idle')
        self.frames['run'] = import_folder('graphics/character/run')
        self.frames['jump'] = import_folder('graphics/character/jump')
        self.frames['fall'] = import_folder('graphics/character/fall')

        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.frames['idle'][self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)

        self.state = 'idle'
        self.gravity = 0.8
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (50,self.rect.height))

        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.dust_run_particles = import_folder('graphics/character/dust_particles/run')
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = display_surface
        self.create_jump_particles = create_jump_particles

        self.update_damage = damage_player
        self.invincible =   False
        self.invincibility_duration = 500
        self.hurt_time = 0

        # audio
        self.jump_sound = pygame.mixer.Sound('audio/effects/jump.wav')
        self.jump_sound.set_volume(0.5)
        self.hit_sound = pygame.mixer.Sound('audio/effects/hit.wav')

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames[self.state]):
            self.frame_index = 0
        image = self.frames[self.state][int(self.frame_index)]

        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            image = pygame.transform.flip(image,True,False)
            self.image = image
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        
    def run_dust_animation(self):
        if self.state == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            
            dust_particles = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particles,pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                flipped_dust_particles = pygame.transform.flip(dust_particles,True,False)
                self.display_surface.blit(flipped_dust_particles,pos)

    def apply_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed
        self.jump_sound.play()      

    def get_state(self):
        if self.direction.y < 0:
            self.state = 'jump'
        elif self.direction.y > 1:
            self.state = 'fall'
        else:
            if self.direction.x != 0:
                self.state = 'run'
            else:
                self.state = 'idle'

    def get_damage(self):
        if not self.invincible:
            self.hit_sound.play()
            self.update_damage(-10)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
    
    def invincibility_timer(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.invincible = False

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def update(self):
        self.apply_input()
        self.get_state()
        self.animate()
        self.run_dust_animation()
        self.invincibility_timer()
        
