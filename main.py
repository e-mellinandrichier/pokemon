import pygame
import sys

# On importe les classes dont on a besoin
from combat import Combat
from pokedex import Pokedex

pygame.init()

# Dimensions de l'écran
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pokémon Game")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (10, 80, 200)
YELLOW = (255, 215, 0)
BUTTON_COLOR = (20, 50, 120)
BUTTON_HOVER = (40, 90, 200)

# Chargement des assets
background = pygame.image.load("assets/menubg.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

try:
    FONT = pygame.font.Font("assets/Pokemon.ttf", 36)
    TITLE_FONT = pygame.font.Font("assets/Pokemon.ttf", 48)
except FileNotFoundError:
    print("Police non trouvée. Assurez-vous que 'Pokemon.ttf' est dans le dossier 'assets'.")
    sys.exit()

# Options du menu
options = ["Lancer une partie", "Ajouter un Pokémon", "Pokédex", "Quitter"]
selected_index = 0

# Positions des boutons
button_rects = []
for i in range(len(options)):
    rect = pygame.Rect(WIDTH // 2 - 150, 250 + i * 60, 300, 50)
    button_rects.append(rect)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_menu():
    """Affiche l'écran de fond et les boutons du menu principal."""
    screen.blit(background, (0, 0))
    draw_text("POKÉMON GAME", TITLE_FONT, YELLOW, screen, WIDTH // 2, 150)
    
    mouse_pos = pygame.mouse.get_pos()
    for i, option in enumerate(options):
        rect = button_rects[i]
        color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, BLACK, rect.inflate(4, 4), 0, border_radius=5)
        pygame.draw.rect(screen, color, rect, 0, border_radius=5)
        draw_text(option, FONT, WHITE, screen, rect.centerx, rect.centery)

def lancer_partie():
    """
    Lance une partie complète : par exemple, un combat.
    On crée un objet Combat et on appelle sa méthode start().
    """
    combat = Combat(screen)
    combat.start()
    # Quand combat.start() se termine, on retourne dans main_menu().

def ajouter_pokemon():
    """
    Permet d'ajouter un Pokémon en utilisant l'écran de sélection
    de la classe Combat, puis en l'ajoutant dans pokedex.json, etc.
    """
    c = Combat(screen)
    pokemon_selectionne = c.run_selection_screen()
    
    if pokemon_selectionne is not None:
        new_pokemon_data = pokemon_selectionne.pokemon_data()
        c.add_pokemon(new_pokemon_data)
    # Après l'ajout, on revient au menu.

def afficher_pokedex():
    """
    Affiche le Pokédex complet à l'écran via la classe Pokedex.
    """
    p = Pokedex()
    p.show()
    # On revient ensuite au menu quand l'utilisateur ferme la fenêtre du Pokédex.

def main_menu():
    global selected_index
    clock = pygame.time.Clock()
    
    while True:
        draw_menu()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        lancer_partie()
                    elif selected_index == 1:
                        ajouter_pokemon()
                    elif selected_index == 2:
                        afficher_pokedex()
                    elif selected_index == 3:
                        pygame.quit()
                        sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        if i == 0:
                            lancer_partie()
                        elif i == 1:
                            ajouter_pokemon()
                        elif i == 2:
                            afficher_pokedex()
                        elif i == 3:
                            pygame.quit()
                            sys.exit()
        
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
