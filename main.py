import pygame
import json
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokémon")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY = (200, 200, 200)

def charger_pokedex():
    with open("pokedex.json", "r") as file :
        return json.load(file)

class Pokemon :
    def __init__(self, data, x, y):
        self.nom = data["nom"]
        # self.type = data["type"]
        # self.vie = data["vie"]
        # self.attaque = data["attaque"]
        # self.defense = data["defense"]
        self.sprite = pygame.image.load(data["sprite"])
        self.sprite = pygame.transform.scale(self.sprite, (180, 180))
        self.rect = self.sprite.get_rect(topleft=(x, y))

def afficher_menu():
    screen.fill(WHITE)
    bouton_jouer = pygame.Rect(400, 300, 200, 80)
    pygame.draw.rect(screen, GRAY, bouton_jouer)
    afficher_texte("Jouer", 450, 325, 40)
    pygame.display.flip()

    return bouton_jouer

#Fonction qui prend en argument pokédex, les éléments charger depis LE FICHIER JSON
#Liste vide pour stocker les objets Pokemon
#espacement c la distance entre chaque pokemon le x horizontal et y verticale
#on bocle sr i qui représente l'index du pokémon 
#data c les infos du pokémon image et nom
# calcule les coordonées de x et y en fonction de sa colonne et ligne 

def afficher_pokemons(pokedex):
    pokemon_objets = []
    espacement_x = 150
    espacement_y = 150
    orgine_x = 50
    origine_y = 100
    pokemons_par_ligne = 6

    screen.fill(WHITE)
    afficher_texte("Sélectionner un pokemon : ", 280, 30, 35)


    for i, data in enumerate(pokedex):
        colonne = i % pokemons_par_ligne
        ligne = i // pokemons_par_ligne
        x = orgine_x + colonne * espacement_x
        y = origine_y + ligne * espacement_y
        pokemon = Pokemon(data,x , y)
        pokemon_objets.append(Pokemon(data, x,y))
        screen.blit(pokemon.sprite, (x,y))

    pygame.display.flip()

    return pokemon_objets

def afficher_texte(texte,x,y, taille):
    font = pygame.font.Font(None, taille)
    text_surface = font.render(texte, True, BLACK)
    screen.blit(text_surface, (x, y))

def main():
    pokedex = charger_pokedex()
    bouton_jouer= afficher_menu()

    menu = True
    while menu :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(event.pos):
                    menu = False
    pokemons_affiches = afficher_pokemons(pokedex)

    selection = True
    while selection :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for pokemon in pokemons_affiches :
                    if pokemon.rect.collidepoint(event.pos):
                        print(f"Vous avez selectionnée {pokemon.nom} !")
                        pygame.quit()
                        exit()

if __name__ == "__main__":
    main()
