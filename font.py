import pygame
import sys

# Initialisation
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pokémon Game")

# Charger la police
try:
    title_font = pygame.font.Font('pokemon_font.ttf', 40)
    menu_font = pygame.font.Font('pokemon_font.ttf', 24)
except FileNotFoundError:
    title_font = pygame.font.SysFont('Arial', 40, bold=True)
    menu_font = pygame.font.SysFont('Arial', 24)

# Texte du menu
title_text = title_font.render("Pokémon", True, (255, 0, 0))
menu_text = menu_font.render("Appuyez sur ESPACE pour commencer", True, (255, 255, 255))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Lancement du jeu...")

    # Affichage
    screen.fill((0, 0, 0))
    screen.blit(title_text, (250, 200))
    screen.blit(menu_text, (200, 300))
    pygame.display.flip()

pygame.quit()
sys.exit()