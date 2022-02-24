import pygame

class UI:
    def __init__(self, display_surface):
        self.display_surface = display_surface

        self.health_bar = pygame.image.load('graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54,39)
        self.bar_max_width = 152
        self.bar_height = 4

        self.coin = pygame.image.load('graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft = (50,61))

        self.font = pygame.font.Font('graphics/ui/ARCADEPI.TTF',30)
        

    def draw_health_bar(self, curr_health, max_health):
        self.display_surface.blit(self.health_bar, (20,10))
        curr_health_ratio = curr_health/max_health
        curr_bar_width = self.bar_max_width*curr_health_ratio
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (curr_bar_width,self.bar_height))
        pygame.draw.rect(self.display_surface,'#dc4949',health_bar_rect)

    def draw_coins(self, coins):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_text = self.font.render(str(coins),False,'#33323d')
        coin_text_rect = coin_text.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
        self.display_surface.blit(coin_text, coin_text_rect)