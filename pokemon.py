import time

class Pokemon():
    def __init__(self, typ, name, PV, attaque, defense, niveau):
        self.type = typ
        self.name = name
        self.PV = PV
        self.attaque = attaque
        self.defense = defense
        self.niveau = niveau

class Combat():
    def __init__(self, joueur1, joueur2):
        self.poke1 = poke1
        self.poke2 = poke2

    def infos(self):
        poke1type = poke1.type
        poke2type = poke2.type

    def attaque(self):
        poke1.PV -= poke2.PV 

    def pokegagnant(self, p):
        return p.name

    def 


class Pokedex():
    def __init__(self):
        self.name

p1 = Pokemon("feu", "ponyta", 40, 10, 10, 4)
p2 = Pokemon("eau", "grenousse", 60, 20, 10, 8)

c1 = Combat()
c1.infos(p1, p2)