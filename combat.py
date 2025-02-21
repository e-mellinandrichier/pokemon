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
        self.clock = pygame.time.Clock()

        # Chargement des polices personnalisées (assurez-vous que "pokemon.ttf" est accessible)
        self.font = pygame.font.Font("pokemon.ttf", 24)
        self.button_font = pygame.font.Font("pokemon.ttf", 32)

        # Définition des couleurs utilisées
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 102, 204)
        self.LIGHT_BLUE = (51, 153, 255)
        self.YELLOW = (255, 255, 0)

        # Chargement et redimensionnement de l'image de fond de combat
        try:
            self.background = pygame.image.load("battlebg.png")
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except Exception as e:
            print("Erreur lors du chargement de battlebg.png :", e)
            self.background = pygame.Surface((self.width, self.height))
            self.background.fill(self.WHITE)

        # Chargement de la liste des Pokémon depuis le fichier JSON
        try:
            with open('pokemon.json', 'r') as f:
                self.pokemon_list = json.load(f)
        except Exception as e:
            print("Erreur lors du chargement de pokemon.json :", e)
            self.pokemon_list = []

        self.player_pokemon = None
        self.enemy_pokemon = None
        self.combat_active = False
        self.message = ""
        self.message_timer = 0

        # Repositionnement des boutons pour éviter qu'ils soient coupés
        self.buttons = [
            {"rect": pygame.Rect(500, 430, 250, 50), "text": "Attaquer", "action": "attack"},
            {"rect": pygame.Rect(500, 490, 250, 50), "text": "Changer", "action": "switch"},
            {"rect": pygame.Rect(500, 550, 250, 50), "text": "Fuir", "action": "flee"}
        ]

    def draw_button(self, rect, text):
        mouse_pos = pygame.mouse.get_pos()
        color = self.LIGHT_BLUE if rect.collidepoint(mouse_pos) else self.BLUE
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        text_surf = self.button_font.render(text, True, self.BLACK)
        text_rect = text_surf.get_rect(center=rect.center)
        self.screen.blit(text_surf, text_rect)

    def draw_health_bar(self, pokemon, x, y):
        bar_width = 200
        bar_height = 20
        fill = int((pokemon.hp / pokemon.max_hp) * bar_width)
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(self.screen, self.BLACK, outline_rect, 2)
        pygame.draw.rect(self.screen, (0, 255, 0), fill_rect)

    def draw_dialogue_box(self):
        # Boîte de dialogue réduite et repositionnée en bas à gauche
        box_rect = pygame.Rect(50, 500, 400, 80)
        s = pygame.Surface((box_rect.width, box_rect.height))
        s.set_alpha(180)
        s.fill(self.WHITE)
        self.screen.blit(s, box_rect.topleft)
        if self.message:
            lines = self.message.split('\n')
            for i, line in enumerate(lines):
                text_surf = self.font.render(line, True, self.BLACK)
                self.screen.blit(text_surf, (box_rect.x + 10, box_rect.y + 10 + i * 30))

    def render_battle_screen(self):
        self.screen.blit(self.background, (0, 0))
        enemy_img = pygame.image.load(self.enemy_pokemon.image)
        enemy_img = pygame.transform.scale(enemy_img, (200, 200))
        # Position ajustée pour l'ennemi
        self.screen.blit(enemy_img, (550, 30))
        enemy_text = self.font.render(f"{self.enemy_pokemon.name}", True, self.BLACK)
        self.screen.blit(enemy_text, (550, 220))
        # La barre de vie de l'ennemi est placée juste en dessous du sprite
        self.draw_health_bar(self.enemy_pokemon, 550, 240)

        # Affichage du Pokémon du joueur en bas à gauche avec sprite agrandi (200×200)
        player_img = pygame.image.load(self.player_pokemon.image)
        player_img = pygame.transform.scale(player_img, (200, 200))
        self.screen.blit(player_img, (50, 350))
        # Affichage du nom du Pokémon du joueur au-dessus de la barre de vie
        player_text = self.font.render(f"{self.player_pokemon.name}", True, self.BLACK)
        self.screen.blit(player_text, (50, 310 - 30))  # affiché à 280
        self.draw_health_bar(self.player_pokemon, 50, 310)

        # Affichage des boutons d'action
        for btn in self.buttons:
            self.draw_button(btn["rect"], btn["text"])
        self.draw_dialogue_box()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn in self.buttons:
                    if btn["rect"].collidepoint(mouse_pos):
                        return btn["action"]
        return None

    def player_turn(self):
        action = None
        while not action:
            self.render_battle_screen()
            pygame.display.flip()
            action = self.handle_input()
            self.clock.tick(30)
            if pygame.time.get_ticks() > self.message_timer:
                self.message = ""
        return action

    def calculate_damage(self, attacker, defender):
        # Calcul de dégâts inspiré de la formule des combats Pokémon
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
        move_type = attacker.types[0] if isinstance(attacker.types, list) else attacker.types
        if random.randint(1, 15) == 1:
            return 0
        multiplier = 1
        for defense_type in defender.types:
            if isinstance(defense_type, str):
                effectiveness = type_chart.get(move_type.lower(), {}).get(defense_type.lower(), 1)
                multiplier *= effectiveness
        base_power = 50
        damage = ((2 * attacker.level / 5 + 2) * base_power * attacker.attack / defender.defense) // 50
        damage = (damage + 2) * multiplier
        return max(1, int(damage))

    def load_pokemons(self, file):
        try:
            with open(file, 'r') as f:
                pokedex = json.load(f)
                return pokedex
        except (FileNotFoundError, json.JSONDecodeError):
            starter = [{
                "name": "Wattwatt",
                "hp": 35,
                "level": 5,
                "attack": 52,
                "defense": 40,
                "types": ["electrik"],
                "image": "assets/wattwatt.png",
                "max_hp": 35
            }]
            with open('pokedex.json', 'w') as f:
                json.dump(starter, f, indent=2)
            return starter

    def display_pokemons(self, pokedex):
        pokemon_list = []
        space_x = 100
        space_y = 100
        origin_x = 10
        origin_y = 10
        pokemons_per_line = 6
        self.screen.fill(self.WHITE)
        self.message = "Sélectionner un Pokémon :"
        self.draw_dialogue_box()
        for i, p in enumerate(pokedex):
            pokemon = Pokemon(p["name"], p["hp"], p["level"], p["attack"], p["defense"], p["types"], p["image"], p["max_hp"])
            column = i % pokemons_per_line
            row = i // pokemons_per_line
            x = origin_x + column * space_x
            y = origin_y + row * space_y
            pokemon.rect.topleft = (x, y)
            self.screen.blit(pokemon.assets, (x, y))
            pokemon_list.append(pokemon)
        pygame.display.flip()
        return pokemon_list

    def run_selection_screen(self):
        selection_active = True
        pokedex = self.load_pokemons('pokedex.json')
        displayed_pokemons = self.display_pokemons(pokedex)
        while selection_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for pokemon in displayed_pokemons:
                        if pokemon.rect.collidepoint(mouse_pos):
                            return pokemon
            pygame.display.flip()
            self.clock.tick(30)
        return None

    def add_pokemon(self, new_pokemon):
        try:
            with open("pokedex.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []
        if any(pokemon.get('name') == new_pokemon.get('name') for pokemon in data):
            pass
        else:
            new_pokemon['hp'] = new_pokemon['max_hp']
            data.append(new_pokemon)
        with open("pokedex.json", "w") as file:
            json.dump(data, file, indent=4)

    def enemy(self):
        p = Pokedex()
        list_enemy = p.select_pokemons()
        return list_enemy

    def start(self):
        self.combat_active = True
        if not hasattr(self, 'list_enemy') or not self.list_enemy:
            self.list_enemy = self.enemy()
        index = random.randint(0, len(self.list_enemy) - 1)
        enemy_data = self.list_enemy[index]
        self.enemy_pokemon = Pokemon(
            enemy_data['name'],
            enemy_data['hp'],
            enemy_data['level'],
            enemy_data['attack'],
            enemy_data['defense'],
            enemy_data['types'],
            enemy_data['image'],
            enemy_data['max_hp']
        )
        if self.player_pokemon is None:
            self.player_pokemon = self.run_selection_screen()
        new_pokemon = self.player_pokemon.pokemon_data()
        self.add_pokemon(new_pokemon)
        self.message = f"Un {self.enemy_pokemon.name} sauvage apparaît!"
        self.message_timer = pygame.time.get_ticks() + 2000
        self.render_battle_screen()
        pygame.display.flip()
        pygame.time.delay(2000)

        while self.combat_active:
            action = self.player_turn()
            if action == "quit":
                return False
            if action == "attack":
                damage = self.calculate_damage(self.player_pokemon, self.enemy_pokemon)
                self.enemy_pokemon.take_damage(damage)
                self.message = f"{self.player_pokemon.name} attaque pour {damage} dégâts!"
                self.message_timer = pygame.time.get_ticks() + 1500
                self.render_battle_screen()
                pygame.display.flip()
                pygame.time.delay(1500)
                if self.enemy_pokemon.is_fainted():
                    new_pokemon = self.enemy_pokemon.pokemon_data()
                    self.add_pokemon(new_pokemon)
                    self.player_pokemon.level_up(self.player_pokemon)
                    self.player_pokemon.check_evolution(self.player_pokemon)
                    self.message = f"{self.enemy_pokemon.name} est K.O.!"
                    self.message_timer = pygame.time.get_ticks() + 3000
                    self.render_battle_screen()
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    self.start()
                    return
                damage = self.calculate_damage(self.enemy_pokemon, self.player_pokemon)
                self.player_pokemon.take_damage(damage)
                self.message = f"{self.enemy_pokemon.name} contre-attaque pour {damage} dégâts!"
                self.message_timer = pygame.time.get_ticks() + 1500
                self.render_battle_screen()
                pygame.display.flip()
                pygame.time.delay(1500)
                if self.player_pokemon.is_fainted():
                    self.message = f"{self.player_pokemon.name} est K.O.!"
                    self.message_timer = pygame.time.get_ticks() + 3000
                    self.render_battle_screen()
                    pygame.display.flip()
                    pygame.time.delay(3000)
                    new_pokemon = self.run_selection_screen()
                    if new_pokemon:
                        self.player_pokemon = new_pokemon
                        self.message = f"{self.player_pokemon.name} est prêt à combattre!"
                        self.message_timer = pygame.time.get_ticks() + 1500
                    continue
            elif action == "switch":
                new_pokemon = self.run_selection_screen()
                if new_pokemon:
                    self.player_pokemon = new_pokemon
                    self.message = f"{self.player_pokemon.name} est prêt à combattre!"
                    self.message_timer = pygame.time.get_ticks() + 1500
                continue
            elif action == "flee":
                self.message = "Vous avez fui le combat!"
                self.message_timer = pygame.time.get_ticks() + 1500
                self.render_battle_screen()
                pygame.display.flip()
                pygame.time.delay(1500)
                self.combat_active = False
                return False
            self.clock.tick(30)
