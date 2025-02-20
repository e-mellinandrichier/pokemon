import pygame
import json

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pokémon")
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

class Pokedex():
    def __init__(self):
        self.is_active = True
        
    def load_pokemons(self, file):
        try:
            with open(file, 'r') as f:
                pokedex = json.load(f)
                # print(pokedex)
                return pokedex
        except (FileNotFoundError, json.JSONDecodeError):
            starter = [{        "name": "Wattwatt",
            "hp": 35,
            "level": 5,
            "attack": 52,
            "defense": 40,
            "types": [
                "electrik"
            ],
            "image": "assets/wattwatt.png",
            "max_hp": 35}]

            with open('pokedex.json', 'w') as f:
                json.dump(starter, f, indent=2)
            return starter

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

# au lancement du jeu, on sélectionne un des pokemon pour combattre avec
# afficher tous les pokemon du pokedex qui sont déselectionnés 
# selctionne les pokemon
# retourne une deuxième liste contenant uniquement les pokemon séléctionnés
# sur cette liste -> qu'on fait le random sur le opponent pokemon
