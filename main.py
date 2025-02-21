import pygame
import sys
from combat import Combat
from pokedex import Pokedex

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
LIGHT_BLUE = (51, 153, 255)
YELLOW = (255, 255, 0)

# Chargement des polices
# - font_title est maintenant en taille 120 pour doubler sa taille
font_title = pygame.font.Font("pokemon.ttf", 120)
font_button = pygame.font.Font("pokemon.ttf", 32)

# Chargement de l'image de fond
background = pygame.image.load("mainbg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

def draw_button(surface, rect, text, font, color_normal, color_hover):
    mouse_pos = pygame.mouse.get_pos()
    color = color_hover if rect.collidepoint(mouse_pos) else color_normal

    pygame.draw.rect(surface, color, rect, border_radius=8)
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

def main_menu():
    button_width = 300
    button_height = 60
    button_x = (WIDTH - button_width) // 2
    button_y_start = 220
    button_spacing = 20

    button_texts = [
        "Lancer une partie",
        "Ajouter un Pokémon",
        "Pokédex",
        "Quitter"
    ]

    buttons = []
    for i, text in enumerate(button_texts):
        rect = pygame.Rect(
            button_x,
            button_y_start + i * (button_height + button_spacing),
            button_width,
            button_height
        )
        buttons.append((rect, text))

    running = True
    while running:
        screen.blit(background, (0, 0))

        # Titre du jeu avec la police doublée
        title_surf = font_title.render("Pokémon Game", True, YELLOW)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        for rect, text in buttons:
            draw_button(screen, rect, text, font_button, BLUE, LIGHT_BLUE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for i, (rect, text) in enumerate(buttons):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            combat = Combat(screen)
                            combat.start()
                        elif i == 1:
                            combat = Combat(screen)
                            combat.list_enemy = []
                            combat.start()
                        elif i == 2:
                            pokedex = Pokedex()
                            pokedex.show()
                        elif i == 3:
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    main_menu()
