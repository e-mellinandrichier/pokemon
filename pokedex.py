import pygame
import json
from pokemon import Pokemon

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pokémon")
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

class Pokedex():
    def __init__(self):
        self.is_active = True
        
    def load_pokemons(self):
        with open('pokedex.json', 'r') as f:
            return json.load(f)

    def add_pokemon(self, new_pokemon):
        self.list.append(new_pokemon)
        self.save()

    def save(self):
        data = [pokemon.to_dict() for pokemon in self.list]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def show(self):
        running = True
        pokedex = self.load_pokemons()

        grid_columns = 6
        grid_rows = 3
        image_height = 100
        image_width = 100
        pokemon_image_list = [p['image'] for p in pokedex]
        images = [pygame.image.load(path) for path in pokemon_image_list]

        selected_pokemon = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    col = mouse_x // image_width
                    row = mouse_y // image_height
                    index = (row -1) * grid_columns + col - 1
                    selected_pokemon = pokedex[index]

            screen.fill((255, 255, 255))

            for row_idx in range(grid_rows):
                for col_idx in range(grid_columns):
                    index = row_idx * grid_columns + col_idx
                    if index < len(images):
                        x = col_idx * image_width
                        y = row_idx * image_height
                        screen.blit(images[index], (x, y))

            # Draw Pokémon info if selected
            if selected_pokemon:
                self.show_infos(selected_pokemon)

            pygame.display.flip()
    
    def show_infos(self, pokemon):
        screen.fill((255, 255, 255))
        lines = [
            f"Name: {pokemon['name']}",
            f"HP: {pokemon['hp']}",
            f"Attack: {pokemon['attack']}",
            f"Defense: {pokemon['defense']}",
        ]
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (0, 0, 0))
            screen.blit(text_surface, (100, 100 + i * 30))

        image = pygame.image.load(pokemon['image'])
        screen.blit(image, (300, 0))
        pygame.display.flip()
    
class AddPokemon:
    def __init__(self, pokedex, screen, font):
        self.pokedex = pokedex
        self.screen = screen
        self.font = font
    

    def display_form(self):
        name = pygame_input("Enter Pokémon name:", self.screen, self.font, pos=(300, 200))
        type_ = pygame_input("Enter Pokémon type:", self.screen, self.font, pos=(300, 260))
        hp_str = pygame_input("Enter Pokémon HP:", self.screen, self.font, pos=(300, 320))
        attack_str = pygame_input("Enter Pokémon attack:", self.screen, self.font, pos=(300, 380))
        defense_str = pygame_input("Enter Pokémon defense:", self.screen, self.font, pos=(300, 440))

        try:
            hp = int(hp_str)
            attack = int(attack_str)
            defense = int(defense_str)
        except ValueError:
            self.screen.fill(WHITE)
            draw_text("Input error: numeric values expected.", self.font, BLACK, self.screen, 300, 500)
            pygame.display.flip()
            pygame.time.wait(2000)
            return None

        return Pokemon(name, type_, hp, attack, defense)

    def add(self):
        new_pokemon = self.display_form()
        if new_pokemon:
            self.pokedex.add_pokemon(new_pokemon)
            self.screen.fill(WHITE)
            draw_text(f"{new_pokemon.name} has been added to the Pokedex!", self.font, BLACK, self.screen, 300, 300)
            pygame.display.flip()
            pygame.time.wait(2000)