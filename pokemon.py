import pygame

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
    
    def pokemon_data(self):
        return {"name": self.name, "hp": self.hp, "level": self.level, "attack": self.attack, "defense": self.defense, "types": self.types, "image": self.image, "max_hp": self.max_hp}
    