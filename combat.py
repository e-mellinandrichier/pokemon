import pygame
import random
import json
import time
from pokemon import Pokemon

class Combat:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()
        
        # Charger les Pokémon
        with open('pokedex.json', 'r') as f:
            self.pokemon_list = json.load(f)
            
        # Initialisation des Pokémon
        self.player_pokemon = None
        self.player_pokemon_img = None
        self.enemy_pokemon = None
        self.enemy_pokemon_img = None
        self.combat_active = False
        self.message = ""
        self.message_timer = 0
        self.buttons = [
            {"rect": pygame.Rect(50, 450, 200, 50), "text": "Attaquer", "action": "attack"},
            {"rect": pygame.Rect(300, 450, 200, 50), "text": "Changer", "action": "switch"},
            {"rect": pygame.Rect(550, 450, 200, 50), "text": "Fuir", "action": "flee"}
        ]

    def draw_button(self, rect, text, color=(200, 200, 200)):
        pygame.draw.rect(self.screen, color, rect)
        text_surf = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def draw_health_bar(self, pokemon, x, y):
        bar_width = 200
        bar_height = 20
        fill = (pokemon.hp / pokemon.max_hp) * bar_width  # Calcul de la proportion de vie
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        
        # Dessiner la barre de vie
        pygame.draw.rect(self.screen, (255, 0, 0), outline_rect)  # Fond rouge
        pygame.draw.rect(self.screen, (0, 255, 0), fill_rect)     # Barre verte
        pygame.draw.rect(self.screen, (0, 0, 0), outline_rect, 2) # Contour noir

    def show_message(self, text, duration=500):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration 

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["action"]
        return None

    def player_turn(self):
        action = None
        while not action:
            self.screen.fill((255, 255, 255))  # Fond blanc
            
            # Dessiner les Pokémon
            player_pokemon_img = pygame.image.load(self.player_pokemon.image)
            self.screen.blit(self.font.render(f"Player: {self.player_pokemon.name}", True, (0, 0, 0)), (50, 50))
            self.screen.blit(player_pokemon_img, (50, 250))
            self.draw_health_bar(self.player_pokemon, 50, 80)  # Barre de vie du joueur
            
            enemy_pokemon_img = pygame.image.load(self.enemy_pokemon.image)
            self.screen.blit(enemy_pokemon_img, (500, 50))
            self.screen.blit(self.font.render(f"Enemy: {self.enemy_pokemon.name}", True, (0, 0, 0)), (500, 50))
            self.draw_health_bar(self.enemy_pokemon, 500, 80)  # Barre de vie de l'ennemi
            
            # Dessiner les boutons
            for btn in self.buttons:
                self.draw_button(btn["rect"], btn["text"])
            
            # Afficher les messages
            if self.message:
                text_surf = self.font.render(self.message, True, (0, 0, 0))
                self.screen.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 300))

            pygame.display.flip()
            action = self.handle_input()
            self.clock.tick(30)
            
            if pygame.time.get_ticks() > self.message_timer:
                self.message = ""
                
        return action

    def calculate_damage(self, attacker, defender):
        
        type_chart = {
            'normal': {'normal': 1, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 0.5, 'spectre': 0, 'dragon': 1, 'tenebres': 1, 'acier': 0.5, 'fee': 1},
            'plante': {'normal': 1, 'plante': 0.5, 'feu': 0.5, 'eau': 2, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 0.5, 'sol': 2, 'vol': 0.5, 'psy': 1, 'insecte': 0.5, 'roche': 2, 'spectre': 1, 'dragon': 0.5, 'tenebres': 1, 'acier': 0.5, 'fee': 1},
            'feu': {'normal': 1, 'plante': 2, 'feu': 0.5, 'eau': 0.5, 'electrik': 1, 'glace': 2, 'combat': 1, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 1, 'insecte': 2, 'roche': 0.5, 'spectre': 1, 'dragon': 0.5, 'tenebres': 1, 'acier': 2, 'fee': 1},
            'eau': {'normal': 1, 'plante': 0.5, 'feu': 2, 'eau': 0.5, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 1, 'sol': 2, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 2, 'spectre': 1, 'dragon': 0.5, 'tenebres': 1, 'acier': 1, 'fee': 1},
            'electrik': {'normal': 1, 'plante': 0.5, 'feu': 1, 'eau': 2, 'electrik': 0.5, 'glace': 1, 'combat': 1, 'poison': 1, 'sol': 0, 'vol': 2, 'psy': 1, 'insecte': 1, 'roche': 1, 'spectre': 1, 'dragon': 0.5, 'tenebres': 1, 'acier': 1, 'fee': 1},
            'glace': {'normal': 1, 'plante': 2, 'feu': 0.5, 'eau': 0.5, 'electrik': 1, 'glace': 0.5, 'combat': 1, 'poison': 1, 'sol': 2, 'vol': 2, 'psy': 1, 'insecte': 1, 'roche': 1, 'spectre': 1, 'dragon': 2, 'tenebres': 1, 'acier': 0.5, 'fee': 1},
            'combat': {'normal': 2, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 2, 'combat': 1, 'poison': 0.5, 'sol': 1, 'vol': 0.5, 'psy': 0.5, 'insecte': 0.5, 'roche': 2, 'spectre': 0, 'dragon': 1, 'tenebres': 2, 'acier': 2, 'fee': 0.5},
            'poison': {'normal': 1, 'plante': 2, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 0.5, 'sol': 0.5, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 0.5, 'spectre': 0.5, 'dragon': 1, 'tenebres': 1, 'acier': 0, 'fee': 2},
            'sol': {'normal': 1, 'plante': 0.5, 'feu': 2, 'eau': 1, 'electrik': 2, 'glace': 1, 'combat': 1, 'poison': 2, 'sol': 1, 'vol': 0, 'psy': 1, 'insecte': 0.5, 'roche': 2, 'spectre': 1, 'dragon': 1, 'tenebres': 1, 'acier': 2, 'fee': 1},
            'vol': {'normal': 1, 'plante': 2, 'feu': 1, 'eau': 1, 'electrik': 0.5, 'glace': 1, 'combat': 2, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 1, 'insecte': 2, 'roche': 0.5, 'spectre': 1, 'dragon': 1, 'tenebres': 1, 'acier': 0.5, 'fee': 1},
            'psy': {'normal': 1, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 2, 'poison': 2, 'sol': 1, 'vol': 1, 'psy': 0.5, 'insecte': 1, 'roche': 1, 'spectre': 1, 'dragon': 1, 'tenebres': 0, 'acier': 0.5, 'fee': 1},
            'insecte': {'normal': 1, 'plante': 2, 'feu': 0.5, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 0.5, 'poison': 0.5, 'sol': 1, 'vol': 0.5, 'psy': 2, 'insecte': 1, 'roche': 1, 'spectre': 0.5, 'dragon': 1, 'tenebres': 2, 'acier': 0.5, 'fee': 0.5},
            'roche': {'normal': 1, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 2, 'combat': 0.5, 'poison': 1, 'sol': 0.5, 'vol': 2, 'psy': 1, 'insecte': 2, 'roche': 1, 'spectre': 1, 'dragon': 1, 'tenebres': 1, 'acier': 0.5, 'fee': 1},
            'spectre': {'normal': 0, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 2, 'insecte': 1, 'roche': 1, 'spectre': 2, 'dragon': 1, 'tenebres': 0.5, 'acier': 1, 'fee': 1},
            'dragon': {'normal': 1, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 1, 'spectre': 1, 'dragon': 2, 'tenebres': 1, 'acier': 0.5, 'fee': 0},
            'tenebres': {'normal': 1, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 0.5, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 2, 'insecte': 1, 'roche': 1, 'spectre': 2, 'dragon': 1, 'tenebres': 0.5, 'acier': 1, 'fee': 0.5},
            'acier': {'normal': 1, 'plante': 0.5, 'feu': 0.5, 'eau': 1, 'electrik': 0.5, 'glace': 2, 'combat': 1, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 2, 'spectre': 1, 'dragon': 1, 'tenebres': 1, 'acier': 0.5, 'fee': 2},
            'fee': {'normal': 1, 'plante': 0.5, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 2, 'sol': 0.5, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 1, 'spectre': 1, 'dragon': 2, 'tenebres': 2, 'acier': 0.5, 'fee': 1}

            # 'feu': {'normal': 1, 'plante': 1, 'feu': 1, 'eau': 1, 'electrik': 1, 'glace': 1, 'combat': 1, 'poison': 1, 'sol': 1, 'vol': 1, 'psy': 1, 'insecte': 1, 'roche': 1, 'spectre': 1, 'dragon': 1, 'tenebres': 1, 'acier': 1, 'fee': 1}
        }

        multiplier = 1
        for attack_type in attacker.types:
            for defense_type in defender.types:
                multiplier *= type_chart.get(attack_type.lower(), {}).get(defense_type.lower(), 1)

        damage = attacker.attack * multiplier - defender.defense
        return max(10, int(damage))

    def start(self):
        self.combat_active = True
        
        # Sélection du Pokémon
        self.player_pokemon = Pokemon(**random.choice(self.pokemon_list))
        # self.player_pokemon_img = self.player_pokemon.image
        self.enemy_pokemon = Pokemon(**random.choice(self.pokemon_list))
        # self.enemy_pokemon_img = self.enemy_pokemon.image

        
        self.show_message(f"Un {self.enemy_pokemon.name} sauvage apparaît!", 2000)

        while self.combat_active:
            # Tour du joueur
            action = self.player_turn()
            
            if action == "quit":
                return

            if action == "attack":
                # Attaque du joueur
                damage = self.calculate_damage(self.player_pokemon, self.enemy_pokemon)
                self.enemy_pokemon.take_damage(damage)
                self.show_message(f"{self.player_pokemon.name} attaque pour {damage} dégâts!", 1500)  # Afficher le message pendant 1,5 seconde
                
                # Mettre à jour l'affichage avant de passer à la contre-attaque
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.font.render(f"Player: {self.player_pokemon.name}", True, (0, 0, 0)), (50, 50))
                player_pokemon_img = pygame.image.load(self.player_pokemon.image)
                self.screen.blit(player_pokemon_img, (50, 250))
                
                self.draw_health_bar(self.player_pokemon, 50, 80)
                self.screen.blit(self.font.render(f"Enemy: {self.enemy_pokemon.name}", True, (0, 0, 0)), (500, 50))
                enemy_pokemon_img = pygame.image.load(self.enemy_pokemon.image)
                self.screen.blit(enemy_pokemon_img, (500, 50))

                self.draw_health_bar(self.enemy_pokemon, 500, 80)
                for btn in self.buttons:
                    self.draw_button(btn["rect"], btn["text"])
                text_surf = self.font.render(f"{self.player_pokemon.name} attaque pour {damage} dégâts!", True, (0, 0, 0))
                self.screen.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 300))
                pygame.display.flip()
                
                # Pause pour afficher le message
                pygame.time.delay(1500)  # Pause de 1,5 seconde
                
                # Vérifier si l'ennemi est K.O.
                if self.enemy_pokemon.is_fainted():
                    self.show_message(f"{self.enemy_pokemon.name} est K.O.!", 3000)
                    self.combat_active = False
                    return True
                
                # Contre-attaque de l'ennemi
                damage = self.calculate_damage(self.enemy_pokemon, self.player_pokemon)
                self.player_pokemon.take_damage(damage)
                self.show_message(f"{self.enemy_pokemon.name} contre-attaque pour {damage} dégâts!", 1500)
                
                # Mettre à jour l'affichage après la contre-attaque
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.font.render(f"Player: {self.player_pokemon.name}", True, (0, 0, 0)), (50, 50))
                self.draw_health_bar(self.player_pokemon, 50, 80)
                player_pokemon_img = pygame.image.load(self.player_pokemon.image)
                self.screen.blit(player_pokemon_img, (50, 250))

                self.screen.blit(self.font.render(f"Enemy: {self.enemy_pokemon.name}", True, (0, 0, 0)), (500, 50))
                self.draw_health_bar(self.enemy_pokemon, 500, 80)
                enemy_pokemon_img = pygame.image.load(self.enemy_pokemon.image)
                self.screen.blit(enemy_pokemon_img, (500, 50))
                
                for btn in self.buttons:
                    self.draw_button(btn["rect"], btn["text"])
                text_surf = self.font.render(f"{self.enemy_pokemon.name} contre-attaque pour {damage} dégâts!", True, (0, 0, 0))
                self.screen.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 300))
                pygame.display.flip()
                
                # Pause pour afficher le message
                    
                pygame.time.delay(1500)  # Pause de 1,5 seconde
                
                # Vérifier si le joueur est K.O.
                if self.player_pokemon.is_fainted():
                    self.show_message(f"{self.player_pokemon.name} est K.O.!", 3000)
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    self.combat_active = False
                    return False

            elif action == "switch":
                self.show_message("Changement non implémenté!", 1500)

            elif action == "flee":
                self.show_message("Vous avez fui le combat!", 1500)
                self.combat_active = False
                return False

            self.clock.tick(30)