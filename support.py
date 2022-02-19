import pygame
from csv import reader
from settings import tile_size
from os import walk

def import_folder(path):
    surface_list = []
    for _, _, img_list in walk(path):
        for img_path in img_list: 
            surface = pygame.image.load(path + '/' + img_path).convert_alpha()
            surface_list.append(surface)
    return surface_list

def import_csv(path):
    with open(path) as file:
        data = [row for row in reader(file, delimiter=',')]
    return data

def cut_image(path):
    image = pygame.image.load(path).convert_alpha()
    surface_list = []
    col_range = image.get_width() / tile_size
    row_range = image.get_height() / tile_size
    for col in range(int(col_range)):
        for row in range(int(row_range)):
            surface = pygame.Surface((tile_size,tile_size),flags=pygame.SRCALPHA)
            x = row * tile_size
            y = col * tile_size
            surface.blit(image,(0,0),(x, y, tile_size, tile_size))
            surface_list.append(surface)
    return surface_list
        
            