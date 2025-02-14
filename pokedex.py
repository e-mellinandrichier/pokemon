import pygame
import json

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon")

class Pokedex():
    def __init__(self):
        self.is_active = True
        
    def load_pokemons(self):
        with open('pokedex.json', 'r') as f:
            return json.load(f)
    
    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    running = False
            screen.fill((255, 255, 255))
            pokemon_image_list = []
            x = 100
            y = 100
            grid_columns = 6
            grid_rows = 2
            image_width = 100  
            image_height = 100
            pokedex = self.load_pokemons()
            for p in pokedex:
                pokemon_image_list.append(p['image'])
            images = [pygame.image.load(path) for path in pokemon_image_list]
            for row in range(grid_rows):
                for col in range(grid_columns):
                    x = col * image_width
                    y = row * image_height
                    index = row * grid_columns + col
                    if index < len(images):
                        screen.blit(images[index], (x, y))
            pygame.display.flip()