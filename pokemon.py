import pygame
import json

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
        self.battles_won = 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)

    def is_fainted(self):
        return self.hp <= 0
    
    def evolve(self, current_pokemon):
        try:
            with open("evolutions.json", "r") as file:
                 data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = []

        for entry in data:
            if entry["name"] == current_pokemon.name:
                current_pokemon.name = entry["new_name"]
                current_pokemon.image = entry["image"]
                break
        else: 
            pass

    def pokemon_data(self):
        return {"name": self.name, "hp": self.hp, "level": self.level, "attack": self.attack, "defense": self.defense, "types": self.types, "image": self.image, "max_hp": self.max_hp}