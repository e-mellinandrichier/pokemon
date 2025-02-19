import pygame
import random
import json
import time
from pokemon import Pokemon
from pokedex import Pokedex

class Combat:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.font = pygame.font.Font("assets/pokemon.ttf", 24)
        self.clock = pygame.time.Clock()
        
        with open('pokemon.json', 'r') as f:
            self.pokemon_list = json.load(f)
            
        # Chargement du fond et adaptation si nécessaire
        self.background = pygame.image.load("assets/battlebg.png").convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        self.type_colors = {
            'feu': (255, 68, 34), 'eau': (51, 153, 255), 'plante': (119, 204, 85),
            'electrik': (255, 204, 51), 'glace': (153, 255, 255), 'combat': (204, 68, 34),
            'poison': (170, 85, 170), 'sol': (221, 187, 102), 'vol': (170, 170, 255),
            'psy': (255, 102, 170), 'insecte': (170, 187, 34), 'roche': (187, 170, 102),
            'spectre': (102, 102, 170), 'dragon': (102, 102, 255), 'tenebres': (119, 85, 68),
            'acier': (170, 170, 187), 'fee': (238, 153, 238), 'normal': (170, 170, 153)
        }
        
        self.player_pokemon = None
        self.enemy_pokemon = None
        self.combat_active = False
        self.message = ""
        self.message_timer = 0
        
        # Les boutons affichés en bas de l'écran
        self.buttons = [
            {"rect": pygame.Rect(50, 450, 150, 40), "text": "ATTAQUE", "color": (234, 85, 72)},
            {"rect": pygame.Rect(220, 450, 150, 40), "text": "CHANGER", "color": (72, 172, 234)},
            {"rect": pygame.Rect(390, 450, 150, 40), "text": "FUITE",    "color": (159, 234, 72)}
        ]

    def draw_button(self, rect, text, color):
        # Bordure noire
        pygame.draw.rect(self.screen, (0,0,0), rect.inflate(4,4), 0, border_radius=3)
        # Fond bouton
        pygame.draw.rect(self.screen, color, rect, 0, border_radius=3)
        # Texte avec un léger ombrage
        text_surf_shadow = self.font.render(text, True, (30,30,30))
        self.screen.blit(text_surf_shadow, (rect.x+8, rect.y+8))
        text_surf = self.font.render(text, True, (255,255,255))
        self.screen.blit(text_surf, (rect.x+5, rect.y+5))

    def draw_health_bar(self, pokemon, x, y):
        # Barre de fond + bordure
        pygame.draw.rect(self.screen, (0,0,0), (x-2, y-2, 204, 24), 0, 5)
        pygame.draw.rect(self.screen, (80,80,80), (x, y, 200, 20), 0, 5)
        fill_width = int(196 * (pokemon.hp / pokemon.max_hp))
        pygame.draw.rect(self.screen, (92,187,96), (x+2, y+2, fill_width, 16), 0, 5)

    def show_message(self, text, duration=500):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration

    def handle_input(self):
        """
        Gère les événements pygame et renvoie soit 'attaque', 'changer', 'fuite'
        ou None. Peut aussi retourner 'quit' si on ferme la fenêtre.
        """
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in self.buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        # On renvoie le texte du bouton en minuscule
                        return btn["text"].lower()
        return None

    def player_turn(self):
        """
        Affiche l'écran de combat et attend l'action du joueur.
        Renvoie 'attaque', 'changer', 'fuite', ou 'quit'.
        """
        action = None
        while not action:
            self.screen.blit(self.background, (0,0))
            
            # Chargement/redimensionnement des images
            player_img = pygame.image.load(self.player_pokemon.image).convert_alpha()
            enemy_img = pygame.image.load(self.enemy_pokemon.image).convert_alpha()

            # Pour éviter que ce soit trop grand, on redimensionne (à ajuster selon vos sprites)
            player_img = pygame.transform.scale(player_img, (150, 150))
            enemy_img = pygame.transform.scale(enemy_img, (150, 150))
            
            # On les blit aux positions choisies
            self.screen.blit(player_img, (100, 300))
            self.screen.blit(enemy_img, (500, 100))
            
            # Barres de vie
            self.draw_health_bar(self.player_pokemon, 50, 80)
            self.draw_health_bar(self.enemy_pokemon, 500, 80)
            
            # Boutons
            for btn in self.buttons:
                self.draw_button(btn["rect"], btn["text"], btn["color"])

            # Affichage d'un éventuel message (attaques, KO, etc.)
            if self.message:
                text_bg = pygame.Surface((self.width-100, 40), pygame.SRCALPHA)
                text_bg.fill((0, 0, 0, 128))
                self.screen.blit(text_bg, (50, 350))
                
                text_surf = self.font.render(self.message, True, (255,255,255))
                self.screen.blit(text_surf, (self.width//2 - text_surf.get_width()//2, 360))

            pygame.display.flip()
            action = self.handle_input()
            self.clock.tick(30)
            
            if pygame.time.get_ticks() > self.message_timer:
                self.message = ""
                
        return action

    def calculate_damage(self, attacker, defender):
        """
        Calcule les dégâts infligés en fonction des types,
        de l’attaque, de la défense, etc.
        """
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
        }

        multiplier = 1
        for attack_type in attacker.types:
            for defense_type in defender.types:
                multiplier *= type_chart.get(attack_type.lower(), {}).get(defense_type.lower(), 1)

        damage = attacker.attack * multiplier - defender.defense
        return max(10, int(damage))

    def load_pokemons(self):
        with open('pokemon.json', 'r') as f:
            return json.load(f)

    def display_pokemons(self, pokedex_data):
        """
        Affiche les Pokémon en grille pour la sélection,
        renvoie une liste de Pokemon (objets) dont on peut vérifier la zone cliquable.
        """
        pokemon_list = []
        space_x = 120
        space_y = 120
        origin_x = 10
        origin_y = 50
        pokemons_per_line = 6

        self.screen.fill((255, 255, 255))
        self.show_message("Sélectionner un Pokémon :")

        for i, p in enumerate(pokedex_data):
            # Création de l'objet Pokemon
            pokemon = Pokemon(
                p["name"], p["hp"], p["level"], 
                p["attack"], p["defense"], p["types"], p["image"], p["max_hp"]
            )

            # On redimensionne l'image pour la grille de sélection
            scaled_img = pygame.transform.scale(pokemon.assets, (80, 80))
            
            column = i % pokemons_per_line
            row = i // pokemons_per_line
            x = origin_x + column * space_x
            y = origin_y + row * space_y
            
            # On positionne la rect
            pokemon.rect = scaled_img.get_rect(topleft=(x, y))
            
            # On blit l'image redimensionnée
            self.screen.blit(scaled_img, (x, y))
            pokemon_list.append(pokemon)

        pygame.display.flip()
        return pokemon_list

    def run_selection_screen(self):
        """Gère l'écran de sélection d'un Pokémon et renvoie le Pokémon sélectionné."""
        selection_active = True
        pokedex_data = self.load_pokemons()
        displayed_pokemons = self.display_pokemons(pokedex_data)
        
        while selection_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for pokemon in displayed_pokemons:
                        # On vérifie directement si le clic est dans la rect du Pokémon
                        if pokemon.rect.collidepoint(mouse_pos):
                            return pokemon
            
            # On peut éventuellement réafficher ou pas. 
            # Ici, on se contente de limiter la boucle
            self.clock.tick(30)
        return None

    def add_pokemon(self, new_pokemon):
        """
        Ajoute un Pokémon dans le fichier pokedex.json s’il n’y est pas déjà.
        """
        try:
            with open("pokedex.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []

        # On vérifie s’il est déjà présent
        if any(pokemon.get('name') == new_pokemon.get('name') for pokemon in data):
            pass
        else: 
            # On remet les PV à fond
            new_pokemon['hp'] = new_pokemon['max_hp']
            data.append(new_pokemon)

        with open("pokedex.json", "w") as file:
            json.dump(data, file, indent=4)

    def start(self):
        """
        Lance un combat : 
        1. Sélection du Pokémon du joueur
        2. Pokémon ennemi choisi aléatoirement
        3. Boucle d'actions (attaque, changer, fuir)
        """
        self.combat_active = True
        self.player_pokemon = None
        self.enemy_pokemon = None

        # Sélection du Pokémon du joueur
        self.player_pokemon = self.run_selection_screen()
        # On ajoute le Pokémon choisi dans le pokedex du joueur
        new_pokemon = self.player_pokemon.pokemon_data()
        self.add_pokemon(new_pokemon)

        # Choix aléatoire d’un Pokémon ennemi
        self.enemy_pokemon = Pokemon(**random.choice(self.load_pokemons()))
    
        self.show_message(f"Un {self.enemy_pokemon.name} sauvage apparaît!", 2000)

        while self.combat_active:
            action = self.player_turn()

            if action == "quit":
                return

            if action == "attaque":
                # Dégâts du joueur vers ennemi
                damage = self.calculate_damage(self.player_pokemon, self.enemy_pokemon)
                self.enemy_pokemon.take_damage(damage)
                self.show_message(f"{self.player_pokemon.name} attaque pour {damage} dégâts!", 1500)
                pygame.display.flip()
                pygame.time.delay(1500)
                
                if self.enemy_pokemon.is_fainted():
                    new_pokemon = self.enemy_pokemon.pokemon_data()
                    self.add_pokemon(new_pokemon)
                    self.show_message(f"{self.enemy_pokemon.name} est K.O.!", 2000)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    self.combat_active = False
                    return True
                
                # L'ennemi contre-attaque
                damage = self.calculate_damage(self.enemy_pokemon, self.player_pokemon)
                self.player_pokemon.take_damage(damage)
                self.show_message(f"{self.enemy_pokemon.name} contre-attaque pour {damage} dégâts!", 1500)
                pygame.display.flip()
                pygame.time.delay(1500)
                
                if self.player_pokemon.is_fainted():
                    self.show_message(f"{self.player_pokemon.name} est K.O.!", 2000)
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    self.combat_active = False
                    return False

            elif action == "changer":
                new_poke = self.run_selection_screen()
                if new_poke:
                    self.player_pokemon = new_poke
                    self.show_message(f"{self.player_pokemon.name} est prêt(e) à combattre!", 1500)
                continue

            elif action == "fuite":
                self.show_message("Vous avez fui le combat!", 1500)
                pygame.display.flip()
                pygame.time.delay(1500)
                self.combat_active = False
                return False

            self.clock.tick(30)
