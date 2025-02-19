import pygame
import json

class Pokedex:
    def __init__(self):
        self.font = pygame.font.Font("assets/pixel_font.ttf", 20)
        self.type_colors = {
            'feu': (255, 68, 34), 'eau': (51, 153, 255), 
            'plante': (119, 204, 85), 'electrik': (255, 204, 51)
        }

    def show(self):
        screen = pygame.display.get_surface()
        bg = pygame.image.load("assets/pokedex_bg.png").convert()
        pokemons = self.load_pokemons()
        
        while True:
            screen.blit(bg, (0,0))
            
            for i, p in enumerate(pokemons):
                x = 50 + (i % 4) * 180
                y = 50 + (i // 4) * 180
                
                # Carte Pokémon
                pygame.draw.rect(screen, self.type_colors[p['types'][0]], (x-5, y-5, 160, 160), 0, 10)
                pygame.draw.rect(screen, (255,255,255), (x, y, 150, 150), 0, 8)
                
                img = pygame.image.load(p['image']).convert_alpha()
                screen.blit(img, (x+25, y+20))
                
                name_surf = self.font.render(p['name'].upper(), True, (0,0,0))
                screen.blit(name_surf, (x+10, y+120))

            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return