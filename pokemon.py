import pygame
import json
import random
import time

pygame.init()

class Pokemon:
    def __init__(self, name, hp, level, attack, defense, types, image, max_hp):
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.level = level
        self.attack = attack
        self.defense = defense
        self.types = types
        self.image = image
        self.assets = pygame.image.load(image)
        self.rect = self.assets.get_rect()

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def is_fainted(self):
        return self.hp <= 0

    def level_up(self, current_pokemon):
        current_pokemon.level +=1
        current_pokemon.attack += 10
        current_pokemon.defense += 10
        current_pokemon.hp += 10
        current_pokemon.max_hp += 10
        try:
            with open('pokedex.json', 'r') as f:
                pokedex = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pokedex = {}

        for entry in pokedex:
            if entry["name"] == current_pokemon.name:
                entry["level"] >= current_pokemon.level

        with open('pokedex.json', 'w') as f:
            json.dump(pokedex, f, indent=2)
        
    def update_pokedex(self):
        try:
            with open('pokedex.json', 'r') as f:
                pokedex = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pokedex = {}

        pokedex[self.name] = {
            'level': self.level,
        }
        with open('pokedex.json', 'w') as f:
            json.dump(pokedex, f, indent=2)

    def check_evolution(self, current_pokemon):
        try:
            with open("evolutions.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return 

        possible_evolutions = []
        for entry in data:
            if entry["name"] == current_pokemon.name and entry["level"] == current_pokemon.level:
                possible_evolutions.append(entry)
                print(possible_evolutions)

        if possible_evolutions:
            chosen_evolution = random.choice(possible_evolutions)
            self.evolve(current_pokemon, chosen_evolution)
    
    def evolve(self, current_pokemon, chosen_evolution):
        self.animate(current_pokemon, chosen_evolution)
        current_pokemon.image = chosen_evolution["image"]
        current_pokemon.types = chosen_evolution["types"]
        current_pokemon.name = chosen_evolution["new_name"]

    def pokemon_data(self):
        return {"name": self.name, "hp": self.hp, "level": self.level, "attack": self.attack, "defense": self.defense, "types": self.types, "image": self.image, "max_hp": self.max_hp}

    def display_text(self, text):
        font = pygame.font.Font(None, 36)
        screen = pygame.display.set_mode((800, 600))
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (300, 100))

    def animate(self, current_pokemon, chosen_evolution):
        screen = pygame.display.set_mode((800, 600))
        screen.fill((0, 0, 0))
        poke_image = pygame.image.load(current_pokemon.image)
        self.display_text("Evolution!")
        screen.blit(poke_image, (200, 150))
        pygame.display.flip()
        
        time.sleep(1)

        for i in range(5):
            screen.fill((255, 255, 255))
            pygame.display.flip()
            time.sleep(0.2)
            screen.fill((0, 0, 0))
            pygame.display.flip()
            time.sleep(0.2)


        screen.fill((0, 0, 0))
        poke_image2 = pygame.image.load(chosen_evolution["image"])
        screen.blit(poke_image2, (200, 150))
        pygame.display.flip()


        time.sleep(2)