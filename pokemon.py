import pygame
import json
import random

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
            # Read existing Pokedex
            with open('pokedex.json', 'r') as f:
                pokedex = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pokedex = {}

        pokedex[self.name] = {
            'level': self.level,
        }

        # Write back to file
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
            print(chosen_evolution)
            self.evolve(current_pokemon, chosen_evolution)
    
    def evolve(self, current_pokemon, chosen_evolution):
        current_pokemon.name = chosen_evolution["new_name"]
        current_pokemon.image = chosen_evolution["image"]
        current_pokemon.types = chosen_evolution["types"]

    def pokemon_data(self):
        return {"name": self.name, "hp": self.hp, "level": self.level, "attack": self.attack, "defense": self.defense, "types": self.types, "image": self.image, "max_hp": self.max_hp}