import pygame
import sys
import json
from combat import Combat

from pokedex import Pokedex
from pokedex import AddPokemon

pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 900, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Pokémon Game', font, BLACK, screen, 300, 100)
        draw_text('1. Lancer une partie', font, BLACK, screen, 300, 200)
        draw_text('2. Ajouter un Pokémon', font, BLACK, screen, 300, 250)
        draw_text('3. Accéder au Pokédex', font, BLACK, screen, 300, 300)
        draw_text('4. Quitter', font, BLACK, screen, 300, 350)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    combat = Combat(screen)
                    result = combat.start()
                elif event.key == pygame.K_2:
                    pokedex = Pokedex()
                    add_interface = AddPokemon(pokedex, screen, font)
                    add_interface.add()
                elif event.key == pygame.K_3:
                    pokedex = Pokedex()
                    pokedex.show()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()