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
        data = [list(row) for row in reader(file, delimiter=',')]
    return data

def cut_image(path):
    image = pygame.image.load(path).convert_alpha()
    surface_list = []
    tile_num_x = int(image.get_size()[0] / tile_size)
    tile_num_y = int(image.get_size()[1] / tile_size)
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            surface = pygame.Surface((tile_size,tile_size),flags=pygame.SRCALPHA)
            x = col * tile_size
            y = row * tile_size
            surface.blit(image,(0,0),pygame.Rect(x, y, tile_size, tile_size))
            surface_list.append(surface)
    return surface_list
        
            