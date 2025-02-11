import pygame
import random

# Initialisation Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Pokemon:
    def __init__(self, name, level, hp, attack, defense, speed, moves):
        self.name = name
        self.level = level
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves

class Move:
    def __init__(self, name, power, accuracy, type):
        self.name = name
        self.power = power
        self.accuracy = accuracy
        self.type = type

# Création des attaques
tackle = Move("Tackle", 40, 100, "Normal")
ember = Move("Ember", 40, 100, "Fire")

# Création des Pokémon
player_pokemon = Pokemon("Charmander", 5, 39, 52, 43, 65, [tackle, ember])
enemy_pokemon = Pokemon("Squirtle", 5, 44, 48, 65, 43, [tackle])

# État du combat
game_state = "select_move"
selected_move = 0
battle_log = []

def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_hp_bar(pokemon, x, y):
    ratio = pokemon.hp / pokemon.max_hp
    pygame.draw.rect(screen, BLACK, (x-2, y-2, 204, 24), 0)
    pygame.draw.rect(screen, RED, (x, y, 200, 20), 0)
    pygame.draw.rect(screen, GREEN, (x, y, 200 * ratio, 20), 0)

def handle_battle():
    global game_state, selected_move
    
    # Menu de sélection d'attaque
    if game_state == "select_move":
        draw_text("Choisissez une attaque:", 50, 400)
        for i, move in enumerate(player_pokemon.moves):
            draw_text(f"{move.name} ({move.power})", 50, 430 + i * 30, 
                     RED if i == selected_move else BLACK)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and selected_move < len(player_pokemon.moves)-1:
            selected_move += 1
        if keys[pygame.K_UP] and selected_move > 0:
            selected_move -= 1
        if keys[pygame.K_RETURN]:
            game_state = "processing"
            execute_turn(player_pokemon.moves[selected_move])

def calculate_damage(attacker, defender, move):
    # Formule de dégâts simplifiée
    damage = (attacker.attack * move.power) // defender.defense
    return max(1, damage)

def execute_turn(move):
    global game_state
    
    # Déterminer l'ordre d'attaque
    if player_pokemon.speed >= enemy_pokemon.speed:
        attackers = [player_pokemon, enemy_pokemon]
        defenders = [enemy_pokemon, player_pokemon]
    else:
        attackers = [enemy_pokemon, player_pokemon]
        defenders = [player_pokemon, enemy_pokemon]
    
    for i in range(2):
        # Vérifier si le Pokémon peut attaquer
        if attackers[i].hp <= 0:
            continue
        
        # Calcul des dégâts
        damage = calculate_damage(attackers[i], defenders[i], move)
        defenders[i].hp = max(0, defenders[i].hp - damage)
        battle_log.append(f"{attackers[i].name} utilise {move.name}!")
        battle_log.append(f"{defenders[i].name} perd {damage} PV!")
        
        # Vérifier si un Pokémon est K.O.
        if defenders[i].hp <= 0:
            battle_log.append(f"{defenders[i].name} est K.O.!")
            game_state = "battle_over"
            return
    
    game_state = "select_move"

# Boucle principale
running = True
while running:
    screen.fill(WHITE)
    
    # Affichage des Pokémon
    draw_text(player_pokemon.name, 50, 50)
    draw_hp_bar(player_pokemon, 50, 80)
    
    draw_text(enemy_pokemon.name, 450, 50)
    draw_hp_bar(enemy_pokemon, 450, 80)
    
    # Log de combat
    for i, message in enumerate(reversed(battle_log[-3:])):
        draw_text(message, 50, 300 + i * 30)
    
    # Gestion des états
    if game_state != "battle_over":
        handle_battle()
    else:
        draw_text("Le combat est termine!", 300, 300)
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()