import copy
import pygame
import math
import random


"""
obligé::::
fenetre --
background --

loulou --
déplacement loulou --
anim loulou (déplacement et saut) -- aaaAAAAAAAAAAAAAAHHHHHHHHHHHHhhhhhhaaaaa


apparaitre tim --
déplacemnt tim --
anim tim (déplacement et saut) --
collision tim loulou -- Il faut revoir la collision droite-gauche et faire comme la collision up ou la collision avec les blocs



création de la mécanique des plusieurs niveaux --
menu et reload --

bloc --
placement des blocs --

collision perso blocs --



création de plusieurs niveaux -



Finito!
"""
"""
quasi sur::::
inversion des touches qui déplacent tim et loulou --

ce serait cool::::
plateforme où si un perso est dessus une porte s'ouvre pendant qu'il est dessus --


            effet sonore

musique --


            en plus::::
            création et pose de buissons

"""

pygame.init()

clock = pygame.time.Clock()  # définir une clock
FPS = 60

pygame.display.set_caption("Loulou & Tim !")  # fenetre
screen = pygame.display.set_mode((2000, 1080))  # 2000, 1080      100 54

background_ciel = pygame.image.load("ciel_nuage_background.png")
background_ciel = pygame.transform.scale(background_ciel, (2000, 1080))  # (1406, 974)

background_sol = pygame.image.load("background_sol.png")
background_sol = pygame.transform.scale(background_sol, (2000, 167))  # 167
background_sol_rect = background_sol.get_rect()

drapeau = pygame.image.load("Drapeau.png")
drapeau = pygame.transform.scale(drapeau, (150, 300))

reload = pygame.image.load("reload.png")
reload = pygame.transform.scale(reload, (80, 80))
reload_rect = reload.get_rect()
reload_rect.x = 30 + 100
reload_rect.y = 30

menu = pygame.image.load("menu.png")
menu = pygame.transform.scale(menu, (239, 81))
menu_rect = menu.get_rect()
menu_rect.x = 30 + reload_rect.width + 30 + 100
menu_rect.y = 30

play_button = pygame.image.load("play_button_nuage.png")
play_button = pygame.transform.scale(play_button, (660, 300))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3)
play_button_rect.y = math.ceil(screen.get_height() / 2.7)

son_marche = pygame.image.load("Son-1.png")
son_marche = pygame.transform.scale(son_marche, (90, 90))
son_marche_rect = son_marche.get_rect()
son_marche_rect.x = 25
son_marche_rect.y = 25

son_eteint = pygame.image.load("Son-2.png")
son_eteint = pygame.transform.scale(son_eteint, (90, 90))
son_eteint_rect = son_eteint.get_rect()
son_eteint_rect.x = 25
son_eteint_rect.y = 25

niveau = 8

myfont = pygame.font.Font('Lysande_Mac.ttf', 60)  # écriture pour les niveaux

pygame.mixer.init()

channel1 = pygame.mixer.Channel(1)  # ouvrir 2 canals (il y a 2 musiques par niveau)
channel2 = pygame.mixer.Channel(2)  # Quand un niveau est fini, les musiques du niveau fini sont écrasé par les musiques du nouveau niveau

death = pygame.mixer.Sound("pet.mp3")

# quelques variables utiles à la suite du code

cpt_saut_loulou = 0  # pour les saut des personnages
cpts_saut_tim = 0  # Il y a deux variables, une pour tim, une pour loulou

dernier_appuye = 0  # pour quand les personnages s'arettent, savoir si c'est à gauche ou à droite
dernier_appuyes = 0

compteur_chgmt_touche = 0  # pour les touches
touche_gauche_tim = pygame.K_q
touche_gauche_loulou = pygame.K_k
touche_droite_loulou = pygame.K_m
touche_droite_tim = pygame.K_d

passe_ici = False  # pour les musiques
passe_la = False
demarrer_musique_menu = False
demarrer_musique_play = False

cpt1_teleporteur_tim = 0  # pour les compteurs de teleporteurs
cpt2_teleporteur_tim = 0
cpt1_teleporteur_loulou = 0
cpt2_teleporteur_loulou = 0

is_tim_passe_par_teleporteur1_1 = False  # pour quand les perso prennent un teleporteur et arrivent sur un teleporteur
is_tim_passe_par_teleporteur1_2 = False  # cela évite qu'ils soient retéléporté dans la foulé
is_loulou_passe_par_teleporteur1_1 = False
is_loulou_passe_par_teleporteur1_2 = False

appliquer_blocs_generateur2 = False

is_bouton_marche = True

cpt_cinematique = 0

# Certaines variables peuvent etre dans des __init__


class Player(pygame.sprite.Sprite):

    def __init__(self, jeu, name, rect_x, saut_hauteur, vitesse):
        super().__init__()
        self.game = jeu
        self.size = (128, 128)
        self.name = name
        self.etat_saut = False
        self.etat_descente_saut = False
        self.image = pygame.image.load(f"{self.name}.png")
        self.image = pygame.transform.scale(self.image, self.size)
        self.current_image = 0  # commencer l'anim à l'image 0
        self.images = animation.get(self.name)
        self.vitesse = vitesse
        self.saut_hauteur = saut_hauteur
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = screen.get_height() - 295
        self.animation = False
        self.gravite_bas = self.vitesse + self.saut_hauteur

    def update_images(self):
        self.images = animation.get(self.name)

    def update_animation_repeat(self):
        self.animate(loop=True)

    def update_animation_no_repeat(self):
        self.animate(loop=False)

    # définir une méthode pour animer le sprite
    def animate(self, loop=False):
        # vérifier si l'animation est active
        if self.animation is True:
            # passer à l'image suivante
            self.current_image += 1
            # verifier si on a atteint la fin de l'animation
            if self.current_image >= len(self.images):
                # remettre l'anim au départ
                self.current_image = 0
                # vérifier si l'animation n'est pas en mode boucle
                if loop is False:
                    # desactivation de l'animation
                    self.animation = False

            # modifier l'image précédente par l'image suivante
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)

    # définir une méthode pour démarer l'animation
    def start_animation(self):
        self.animation = True

    def saut(self):
        self.rect.y = self.rect.y - (self.gravite_bas + self.gravite_bas)  # 2 fois gravite bas pour contrer la gravite qui s'applique en permanence

    def gravite(self):
        self.rect.y = self.rect.y + self.gravite_bas

    def verifie_pique(self):
        global niveau
        if niveau == 1:
            if self.game.check_collision(self, self.game.bloc_pique1):
                self.game.game_over()
        elif niveau == 2:
            if self.game.check_collision(self, self.game.bloc_pique2):
                self.game.game_over()
        elif niveau == 3:
            if self.game.check_collision(self, self.game.bloc_pique3):
                self.game.game_over()
        elif niveau == 4:
            if self.game.check_collision(self, self.game.bloc_pique4):
                self.game.game_over()
        elif niveau == 5:
            if self.game.check_collision(self, self.game.bloc_pique5):
                self.game.game_over()
        elif niveau == 6:
            if self.game.check_collision(self, self.game.bloc_pique6):
                self.game.game_over()
        elif niveau == 7:
            if self.game.check_collision(self, self.game.bloc_pique7):
                self.game.game_over()
        elif niveau == 8:
            if self.game.check_collision(self, self.game.bloc_pique8):
                self.game.game_over()
        elif niveau == 9:
            if self.game.check_collision(self, self.game.bloc_pique9):
                self.game.game_over()


class Loulou(Player):
    def __init__(self, jeu):
        super().__init__(jeu, "loulou_cour_droite", 200, -5, 17)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = screen.get_height() - 295

    def move_right(self):
        if self.rect.x + 20 + 70 < self.game.tim.rect.x or self.rect.x > self.game.tim.rect.x + 70 or self.rect.y > self.game.tim.rect.y + 100:  # faire collision entre tim et loulou
            self.rect.x += self.vitesse

    def move_left(self):
        if self.rect.x + 70 < self.game.tim.rect.x or self.rect.x - 20 > self.game.tim.rect.x + 70 or self.rect.y > self.game.tim.rect.y + 100:  # faire collision entre tim et loulou
            self.rect.x -= self.vitesse

    def rectangle_loulou_up(self):  # pour la collision avec tim
        self.rect_mini_up = copy.deepcopy(self.rect)
        self.rect_mini_up.x = self.rect.x + 55
        self.rect_mini_up.y = self.rect.y + 26
        self.rect_mini_up.w = 127 - 55 * 2
        self.rect_mini_up.h = 20
        return self.rect_mini_up


class Tim(Player):
    def __init__(self, jeu):
        super().__init__(jeu, "tim_cour_droite", 50, 19, 8)  # saut_hauteur = 14

    def move_right(self):
        if self.rect.x + 20 + 70 < self.game.loulou.rect.x or self.rect.x > self.game.loulou.rect.x + 70 or self.rect.y + 100 < self.game.loulou.rect.y:  # faire collision entre tim et loulou
            self.rect.x += self.vitesse

    def move_left(self):
        if self.rect.x + 70 < self.game.loulou.rect.x or self.rect.x - 20 > self.game.loulou.rect.x + 70 or self.rect.y + 100 < self.game.loulou.rect.y:  # faire collision entre tim et loulou
            self.rect.x -= self.vitesse


class Papa(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = (91, 119)  # 17*7 = 119   91
        self.image = pygame.image.load("Papa.png")
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = 800
        self.rect.y = 0 - self.rect.h


class ImageCinematique(pygame.sprite.Sprite):
    def __init__(self, width, height, nom, forma, rectx=800, recty=400):
        super().__init__()
        self.size = (width, height)  # 17*7 = 119   91
        self.image = pygame.image.load(f"{nom}.{forma}")
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = rectx
        self.rect.y = recty


def load_animation_images(sprite_name, nb_image):
    # charger les 24 images dans le le dossier correspondant
    images = []
    # récuperer le chemin du dossier pour ce sprite
    path = f"{sprite_name}/{sprite_name}_"  # ATTENTION ICI J4AI MIS UN "_"
    # boucler chaques images dans ce dossier
    for num in range(0, nb_image):  # ATTENTION ICI J4AI MIS UN 12
        image_path = path + str(num) + ".png"
        images.append(pygame.image.load(image_path))
    # renvoyer le contenu de la liste d'image
    return images


animation = {
    "loulou_cour_droite": load_animation_images("loulou_cour_droite", 12),
    "loulou_cour_gauche": load_animation_images("loulou_cour_gauche", 12),
    "loulou_saute_droite": load_animation_images("loulou_saute_droite", 10),
    "loulou_saute_gauche": load_animation_images("loulou_saute_gauche", 10),
    "tim_cour_droite": load_animation_images("tim_cour_droite", 12),
    "tim_cour_gauche": load_animation_images("tim_cour_gauche", 12),
    "tim_saute_droite": load_animation_images("tim_saute_droite", 10),
    "tim_saute_gauche": load_animation_images("tim_saute_gauche", 10),
    "generateur": load_animation_images("generateur", 16)
}


class Bloc(pygame.sprite.Sprite):

    def __init__(self, type_bloc, rect_x, rect_y, forme):
        super().__init__()
        self.type_bloc = type_bloc
        if forme == "carre":
            self.size = (83, 83)
        elif forme == "rectangle":
            self.size = (166, 83)
        self.image = pygame.image.load(f"{self.type_bloc}.png")
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.y = rect_y
        self.rect.x = rect_x
        self.rect_mini_up = copy.deepcopy(self.rect)
        self.rect_mini_up.x = self.rect.x + 55
        self.rect_mini_up.y = self.rect.y + 17
        self.rect_mini_up.w = 55
        self.rect_mini_up.h = 20
        self.rect_mini_down = copy.deepcopy(self.rect)
        self.rect_mini_down.x = self.rect.x + 55
        self.rect_mini_down.y = self.rect.y + 56
        self.rect_mini_down.w = 55
        self.rect_mini_down.h = 20
        self.rect_mini_left = copy.deepcopy(self.rect)
        self.rect_mini_left.x = self.rect.x + 45
        self.rect_mini_left.y = self.rect.y + 36
        self.rect_mini_left.w = 55
        self.rect_mini_left.h = 20
        self.rect_mini_right = copy.deepcopy(self.rect)
        self.rect_mini_right.x = self.rect.x + (self.image.get_width() - (45 + (127 - 55 * 2)))
        self.rect_mini_right.y = self.rect.y + 36
        self.rect_mini_right.w = 127 - 55 * 2
        self.rect_mini_right.h = 20

    def rectangle_bloc_up(self):
        return self.rect_mini_up

    def rectangle_bloc_right(self):
        return self.rect_mini_right

    def rectangle_bloc_left(self):
        return self.rect_mini_left

    def rectangle_bloc_down(self):
        return self.rect_mini_down


def teleportation():  # ne sert que au 1er teleporteur

    # POUR LE 1ER GENERATEUR DU NIVEAU 7

    global cpt1_teleporteur_tim
    global cpt1_teleporteur_loulou
    global cpt2_teleporteur_tim
    global cpt2_teleporteur_loulou
    global is_tim_passe_par_teleporteur1_1
    global is_tim_passe_par_teleporteur1_2
    global is_loulou_passe_par_teleporteur1_1
    global is_loulou_passe_par_teleporteur1_2

    if game.tim.rect.colliderect(game.teleporteur1_1.rectangle_for_collision()) and not is_tim_passe_par_teleporteur1_2:
        cpt1_teleporteur_tim += 1
        if cpt1_teleporteur_tim > 20:
            game.tim.rect.x += 980
            cpt1_teleporteur_tim = 0
            is_tim_passe_par_teleporteur1_1 = True
    else:
        cpt1_teleporteur_tim = 0
    if game.loulou.rect.colliderect(game.teleporteur1_1.rectangle_for_collision()) and not is_loulou_passe_par_teleporteur1_2:
        cpt1_teleporteur_loulou += 1
        if cpt1_teleporteur_loulou > 20:
            game.loulou.rect.x += 980
            cpt1_teleporteur_loulou = 0
            is_loulou_passe_par_teleporteur1_1 = True
    else:
        cpt1_teleporteur_loulou = 0

    if game.tim.rect.colliderect(game.teleporteur1_2.rectangle_for_collision()) and not is_tim_passe_par_teleporteur1_1:
        cpt2_teleporteur_tim += 1
        if cpt2_teleporteur_tim > 20:
            game.tim.rect.x -= 980
            cpt2_teleporteur_tim = 0
            is_tim_passe_par_teleporteur1_2 = True
    else:
        cpt2_teleporteur_tim = 0
    if game.loulou.rect.colliderect(game.teleporteur1_2.rectangle_for_collision()) and not is_loulou_passe_par_teleporteur1_1:
        cpt2_teleporteur_loulou += 1
        if cpt2_teleporteur_loulou > 20:
            game.loulou.rect.x -= 980
            cpt2_teleporteur_loulou = 0
            is_loulou_passe_par_teleporteur1_2 = True
    else:
        cpt2_teleporteur_loulou = 0

    if not game.tim.rect.colliderect(game.teleporteur1_2.rectangle_for_collision()):
        is_tim_passe_par_teleporteur1_1 = False
    if not game.loulou.rect.colliderect(game.teleporteur1_2.rectangle_for_collision()):
        is_loulou_passe_par_teleporteur1_1 = False
    if not game.tim.rect.colliderect(game.teleporteur1_1.rectangle_for_collision()):
        is_tim_passe_par_teleporteur1_2 = False
    if not game.loulou.rect.colliderect(game.teleporteur1_1.rectangle_for_collision()):
        is_loulou_passe_par_teleporteur1_2 = False


def generation():  # EN fait ça c'est juste pour le premier generateur
    #              # les autres il sont fait en bas de update
    if game.tim.rect.colliderect(game.generateur1.rectangle_for_collision()) or game.loulou.rect.colliderect(
            game.generateur1.rectangle_for_collision()):
        game.generateur1.update_images()
        game.generateur1.start_animation()
        game.generateur1.animate()  # mais ce serait cool de faire une généralisation de tout ça
        screen.blit(game.bloc15.image, game.bloc15.rect)
        if game.tim.rect.colliderect(game.bloc15.rectangle_bloc_right()):
            game.tim.rect.x += game.tim.vitesse
        elif game.tim.rect.colliderect(game.bloc15.rectangle_bloc_left()):
            game.tim.rect.x -= game.tim.vitesse
        elif game.tim.rect.colliderect(game.bloc15.rectangle_bloc_up()):
            game.tim.etat_descente_saut = False
            game.tim.rect.y -= game.tim.gravite_bas
        elif game.tim.rect.colliderect(game.bloc15.rectangle_bloc_down()):
            game.tim.rect.y += game.tim.gravite_bas
    else:
        game.generateur1.image = pygame.image.load("generateur.png")
        game.generateur1.image = pygame.transform.scale(game.generateur1.image, game.generateur1.size)


class Teleporteur(pygame.sprite.Sprite):

    def __init__(self, rect_x, rect_y):
        super().__init__()
        self.size = (176, 216)
        self.image = pygame.image.load("teleporteur.png")
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.rect_mini = copy.deepcopy(self.rect)
        self.rect_mini.x = self.rect.x + 85
        self.rect_mini.y = self.rect.y + 40
        self.rect_mini.w = self.rect.w - 85 * 2
        self.rect_mini.h = 100

    def rectangle_for_collision(self):  # POUR LES RECTANGLES
        return self.rect_mini


class Generateur(pygame.sprite.Sprite):

    def __init__(self, rect_x, rect_y):
        super().__init__()
        self.size = (152, 152)
        self.name = "generateur"
        self.image = pygame.image.load(f"{self.name}.png")
        self.image = pygame.transform.scale(self.image, self.size)
        self.current_image = 0  # commencer l'anim à l'image 0
        self.images = animation.get(self.name)
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect.y = rect_y
        self.rect_mini = copy.deepcopy(self.rect)
        self.rect_mini.x = self.rect.x + 75
        self.rect_mini.y = self.rect.y + 35
        self.rect_mini.w = self.rect.w - 75 - 75
        self.rect_mini.h = self.rect.h - 35 - 35
        self.animation = False

    def rectangle_for_collision(self):  # POUR LES RECTANGLES
        return self.rect_mini

    def update_images(self):
        self.images = animation.get(self.name)

    # définir une méthode pour animer le sprite
    def animate(self, loop=True):
        # vérifier si l'animation est active
        if self.animation is True:
            # passer à l'image suivante
            self.current_image += 1
            # verifier si on a atteint la fin de l'animation
            if self.current_image >= len(self.images):
                # remettre l'anim au départ
                self.current_image = 0
                # vérifier si l'animation n'est pas en mode boucle
                if loop is False:
                    # desactivation de l'animation
                    self.animation = False

            # modifier l'image précédente par l'image suivante
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)

    # définir une méthode pour démarer l'animation
    def start_animation(self):
        self.animation = True


class Game:
    def __init__(self):
        # definir si le jeu a commencé ou non
        self.is_playing = False
        # generer notre joueur
        self.loulou = Loulou(self)
        self.tim = Tim(self)
        self.papa = Papa()
        self.boticeli = ImageCinematique(131, 83, "venus", "jpg")
        self.hunger = ImageCinematique(120, 160, "hunger", "webp")
        self.medecine = ImageCinematique(120, 118, "medecine", "png")
        self.prepa = ImageCinematique(140, 180, "prepa", "jpg")
        self.uber_eat = ImageCinematique(120, 120, "uber_eat", "png")
        self.maman = ImageCinematique(84, 130, "maman", "png", screen.get_width(), 400)
        self.avenir = ImageCinematique(248, 60, "avenir", "png", screen.get_width() - 300, 300)

        # la diff entre les diff bloc est le type de bloc, position en x, position en y, forme du bloc (carre ou rectangle)
        # Création de tout les blocs dont j'ai besoin dans tout les niveaux

        self.bloc1 = Bloc("bloc_herbe_long", 166 * 3, screen.get_height() - background_sol.get_height() - 83, "rectangle")
        self.bloc2 = Bloc("bloc_herbe_long", 166 * 4, screen.get_height() - background_sol.get_height() - 83, "rectangle")
        self.bloc3 = Bloc("bloc_herbe_long", 166 * 5, screen.get_height() - background_sol.get_height() - 83, "rectangle")
        self.bloc4 = Bloc("bloc_terre_pique_ciel", 166 * 4 + 153, screen.get_height() - background_sol.get_height() - 1, "rectangle")  # PIQUE
        self.bloc5 = Bloc("bloc_terre_pique_ciel", 166 * 6 + 153, screen.get_height() - background_sol.get_height() - 1, "rectangle")  # PIQUE
        self.bloc6 = Bloc("bloc_herbe_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83 - 83, "rectangle")
        self.bloc7 = Bloc("bloc_terre_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83, "rectangle")
        self.bloc8 = Bloc("bloc_herbe_long", 166 * 5, screen.get_height() - background_sol.get_height() - 83 - 83 - 83 - 50, "rectangle")
        self.bloc9 = Bloc("bloc_terre_pique_ciel", 166 * 4 + 153, screen.get_height() - background_sol.get_height() - 1, "rectangle")  # PIQUE
        self.bloc10 = Bloc("bloc_terre_pique_ciel", 166 * 5 + 153, screen.get_height() - background_sol.get_height() - 1, "rectangle")  # PIQUE
        self.bloc11 = Bloc("bloc_herbe_long", 166 * 3, screen.get_height() - background_sol.get_height() - 83 - 83 - 50, "rectangle")
        self.bloc12 = Bloc("bloc_herbe_long", 166 * 4 + 50, screen.get_height() - background_sol.get_height() - 83 - 83 - 83 - 83 - 50, "rectangle")
        self.bloc13 = Bloc("bloc_herbe_long", 166 * 3, screen.get_height() - background_sol.get_height() - 83 - 83 - 83 - 83 - 50, "rectangle")
        self.bloc14 = Bloc("bloc_herbe_long", 166 * 4 + 70, screen.get_height() - background_sol.get_height() - 83 - 83 - 83 - 83 - 83 - 50, "rectangle")
        self.bloc15 = Bloc("bloc_herbe_long", 166 * 5 + 70, screen.get_height() - background_sol.get_height() - 83 - 83 - 83 - 83 - 83 - 50, "rectangle")
        self.bloc16 = Bloc("bloc_terre_pique_ciel", 166 * 6 + 153, screen.get_height() - background_sol.get_height() - 1, "rectangle")  # PIQUE
        self.bloc17 = Bloc("bloc_terre_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83 * 3, "rectangle")
        self.bloc18 = Bloc("bloc_terre_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83 * 4, "rectangle")
        self.bloc19 = Bloc("bloc_terre_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83 * 5, "rectangle")
        self.bloc20 = Bloc("bloc_terre_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83 * 2, "rectangle")
        self.bloc21 = Bloc("bloc_herbe_long", 166 * 6, screen.get_height() - background_sol.get_height() - 83 * 6, "rectangle")
        self.bloc22 = Bloc("bloc_herbe_long", 166 * 2, screen.get_height() - background_sol.get_height() - 83 * 4, "rectangle")
        self.bloc23 = Bloc("bloc_herbe_long", 166 * 3 + 100, screen.get_height() - background_sol.get_height() - 83 * 6, "rectangle")
        self.bloc24 = Bloc("bloc_herbe_long", 166 * 1 - 100, screen.get_height() - background_sol.get_height() - 83 * 8 - 37, "rectangle")
        self.bloc25 = Bloc("bloc_herbe_long", 166 * 2, screen.get_height() - background_sol.get_height() - 83 * 8, "rectangle")
        self.bloc26 = Bloc("bloc_herbe_long", screen.get_width() - 166, screen.get_height() - background_sol.get_height() - 83 * 5, "rectangle")
        self.bloc27 = Bloc("bloc_herbe_long", screen.get_width() - 166 * 2 - 100, screen.get_height() - background_sol.get_height() - 83 * 6, "rectangle")

        self.generateur1 = Generateur(500, 775)
        self.generateur2 = Generateur(700, 775)
        self.teleporteur1_1 = Teleporteur(500, 700)
        self.teleporteur1_2 = Teleporteur(1500 - self.teleporteur1_1.rect.w / 5, 700)
        self.generateur3 = Generateur(600, 775)
        self.teleporteur2 = Teleporteur(166 * 1 - 100 - 5, screen.get_height() - background_sol.get_height() - 83 * 8 - 34 - self.teleporteur1_2.rect.h)
        self.generateur4 = Generateur(screen.get_width() - 166 * 2 - 100, screen.get_height() - background_sol.get_height() - 83 * 6 - self.generateur3.rect.h + 14)

        self.bloc_niveau1 = pygame.sprite.Group()
        self.bloc_niveau2 = pygame.sprite.Group(self.bloc3)
        self.bloc_niveau3 = pygame.sprite.Group(self.bloc2, self.bloc8)
        self.bloc_niveau4 = pygame.sprite.Group(self.bloc2, self.bloc9)
        self.bloc_niveau5 = pygame.sprite.Group(self.bloc11, self.bloc12, self.bloc9, self.bloc10)
        self.bloc_niveau6 = pygame.sprite.Group(self.bloc13, self.bloc14, self.bloc16, self.bloc10)  # A partir d'ici il faut mettre en bas
        self.bloc_niveau7 = pygame.sprite.Group(self.bloc9, self.bloc10, self.bloc16)
        self.bloc_niveau8 = pygame.sprite.Group()  # regarde en dessous self.bloc_generateur_2
        self.bloc_niveau9 = pygame.sprite.Group(self.bloc23, self.bloc25, self.bloc22, self.bloc9, self.bloc10, self.bloc27, self.bloc26)  # le bloc 16 24 généré

        self.bloc_pique1 = pygame.sprite.Group()
        self.bloc_pique2 = pygame.sprite.Group()
        self.bloc_pique3 = pygame.sprite.Group()
        self.bloc_pique4 = pygame.sprite.Group(self.bloc9)
        self.bloc_pique5 = pygame.sprite.Group(self.bloc9, self.bloc10)
        self.bloc_pique6 = pygame.sprite.Group(self.bloc16, self.bloc10)
        self.bloc_pique7 = pygame.sprite.Group(self.bloc9, self.bloc10, self.bloc16)
        self.bloc_pique8 = pygame.sprite.Group()
        self.bloc_pique9 = pygame.sprite.Group(self.bloc9, self.bloc10)
        self.bloc_pique9_generateur = pygame.sprite.Group(self.bloc16)

        self.bloc_generateur_2 = pygame.sprite.Group(self.bloc20, self.bloc7, self.bloc17, self.bloc18, self.bloc19, self.bloc21)

        self.pressed = {}

    @staticmethod
    def check_collision(sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)

    def start(self):
        self.is_playing = True

    def game_over(self):
        # remettre le jeu à neuf car perdu niveau
        pygame.mixer.Sound.play(death)
        self.tim.etat_saut = False
        self.loulou.etat_saut = False
        self.tim.rect.x = 50
        self.tim.rect.y = screen.get_height() - 295
        self.loulou.rect.y = screen.get_height() - 295
        self.loulou.rect.x = 200
        global dernier_appuye
        global dernier_appuyes
        dernier_appuye = 0
        dernier_appuyes = 0
        global cpts_saut_tim, cpt_saut_loulou
        cpts_saut_tim = 0
        cpt_saut_loulou = 0
        self.is_playing = False  # il faudrait mixer game_win et game_over

    def game_win(self):
        # remettre le jeu à neuf car gagné niveau
        self.tim.etat_saut = False
        self.loulou.etat_saut = False
        self.tim.rect.x = 50
        self.tim.rect.y = screen.get_height() - 295
        self.loulou.rect.y = screen.get_height() - 295
        self.loulou.rect.x = 200
        global dernier_appuye
        global dernier_appuyes
        dernier_appuye = 0
        dernier_appuyes = 0
        global niveau, cpts_saut_tim, cpt_saut_loulou
        cpts_saut_tim = 0
        cpt_saut_loulou = 0
        # effacer les blocs du niveau précédents
        if niveau == 1:
            self.bloc_niveau1 = pygame.sprite.Group()
        elif niveau == 2:
            self.bloc_niveau2 = pygame.sprite.Group()
        elif niveau == 3:
            self.bloc_niveau3 = pygame.sprite.Group()
        elif niveau == 4:
            self.bloc_niveau4 = pygame.sprite.Group()
        elif niveau == 5:
            self.bloc_niveau5 = pygame.sprite.Group()
        elif niveau == 6:
            self.bloc_niveau6 = pygame.sprite.Group()
        elif niveau == 7:
            self.bloc_niveau7 = pygame.sprite.Group()
        elif niveau == 8:
            self.bloc_niveau8 = pygame.sprite.Group()
        elif niveau == 9:
            self.bloc_niveau9 = pygame.sprite.Group()
            # Là il faut rajouter des choses car c'est fini
            # genre met une cinématique tropp stylé
        niveau += 1
        if niveau == 10:
            channel1.stop()  # arrete les 2 musiques
            channel2.stop()

        global passe_la
        global passe_ici
        global demarrer_musique_menu
        global demarrer_musique_play
        passe_la = False
        passe_ici = False
        demarrer_musique_menu = False
        demarrer_musique_play = False

        self.is_playing = False

    """def cinematique(self):
        pass
        self.tim.rect.x = 50
        self.loulou.rect.x = 200
        self.tim.rect.y = screen.get_height() - 295
        self.loulou.rect.y = screen.get_height() - 295
        self.personnages = pygame.sprite.Group(self.loulou, self.tim)
        self.personnages.draw(screen)
        time.sleep(10)
        self.loulou.rect.x = 700
        self.personnages.draw(screen)
        time.sleep(10)"""

    def appliquer_bloc(self, bloc):
        if self.tim.rect.colliderect(bloc.rectangle_bloc_right()):
            self.tim.rect.x += self.tim.vitesse
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_left()):
            self.tim.rect.x -= self.tim.vitesse
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_up()):
            self.tim.rect.y -= self.tim.gravite_bas
            game.tim.etat_descente_saut = False
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_down()):
            self.tim.rect.y += self.tim.gravite_bas

    def appliquer_bloc_bas(self, bloc):  # comme appliquer bloc mais avec le down en premier pour les cas où tim arrive en dessous
        if self.tim.rect.colliderect(bloc.rectangle_bloc_down()):
            self.tim.rect.y += self.tim.gravite_bas
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_left()):
            self.tim.rect.x -= self.tim.vitesse
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_up()):
            self.tim.rect.y -= self.tim.gravite_bas
            game.tim.etat_descente_saut = False
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_right()):
            self.tim.rect.x += self.tim.vitesse

    def appliquer_bloc_haut(self, bloc):  # comme appliquer bloc mais avec le up en premier pour les cas où tim arrive au dessus
        if self.tim.rect.colliderect(bloc.rectangle_bloc_up()):
            self.tim.rect.y -= self.tim.gravite_bas
            game.tim.etat_descente_saut = False
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_down()):
            self.tim.rect.y += self.tim.gravite_bas
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_left()):
            self.tim.rect.x -= self.tim.vitesse
        elif self.tim.rect.colliderect(bloc.rectangle_bloc_right()):
            self.tim.rect.x += self.tim.vitesse

    def update(self, surface):

        global is_bouton_marche
        global cpt_cinematique

        if niveau == 10:
            is_bouton_marche = False
            cpt_cinematique += 1
            surface.blit(self.papa.image, self.papa.rect)
            surface.blit(self.maman.image, self.maman.rect)
            if cpt_cinematique < 180:
                self.papa.rect.y += 2
            if 180 < cpt_cinematique < 200:
                self.papa.rect.y += 1
            if 200 < cpt_cinematique < 250:
                self.loulou.rect.x += 8
                self.tim.rect.x += random.randint(3, 4)
            if 250 < cpt_cinematique < 300:
                texte_cinematique = myfont.render("Bonjour mon père que j'honore", False, (0, 0, 0))
                screen.blit(texte_cinematique, (700, 800))
            if 300 < cpt_cinematique < 330:
                texte_cinematique = myfont.render("Salut papa", False, (0, 0, 0))
                screen.blit(texte_cinematique, (200, 700))
            if 330 < cpt_cinematique < 380:
                texte_cinematique = myfont.render("Ca farte?", False, (0, 0, 0))
                screen.blit(texte_cinematique, (200, 700))
            if 380 < cpt_cinematique < 410:
                texte_cinematique = myfont.render("Trql, trql, tkt", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 410 < cpt_cinematique < 480:
                texte_cinematique = myfont.render("Je viens vous souhaiter un bon anniversaire mes enfants", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 480 < cpt_cinematique < 560:
                texte_cinematique = myfont.render("Et je vais vous donner quelques cadeaux choisis avec minutie", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 560 < cpt_cinematique < 750:
                texte_cinematique = myfont.render("Tient, voilà pour toi Loulou", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 600 < cpt_cinematique:
                surface.blit(self.boticeli.image, self.boticeli.rect)
            if 600 < cpt_cinematique < 650:
                self.boticeli.rect.x -= 1
                self.boticeli.rect.y += 9
            if 650 < cpt_cinematique:
                surface.blit(self.hunger.image, self.hunger.rect)
            if 650 < cpt_cinematique < 700:
                self.hunger.rect.x -= 3
                self.hunger.rect.y += 7
            if 700 < cpt_cinematique:
                surface.blit(self.medecine.image, self.medecine.rect)
            if 700 < cpt_cinematique < 750:
                self.medecine.rect.x -= 5
                self.medecine.rect.y += 8
            if 750 < cpt_cinematique < 850:
                texte_cinematique = myfont.render("Et voilà pour toi Tim", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 800 < cpt_cinematique:
                surface.blit(self.prepa.image, self.prepa.rect)
            if 800 < cpt_cinematique < 850:
                self.prepa.rect.x -= 12
                self.prepa.rect.y += 8
            if 850 < cpt_cinematique < 950:
                texte_cinematique = myfont.render("Et il me semble aussi que tu aimes bien cela", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 900 < cpt_cinematique:
                surface.blit(self.uber_eat.image, self.uber_eat.rect)
            if 900 < cpt_cinematique < 950:
                self.uber_eat.rect.x -= 14
                self.uber_eat.rect.y += 8
            if 950 < cpt_cinematique < 1010:
                texte_cinematique = myfont.render("J'aurais besoin d'un grand doudou pour mettre le couvert!", False, (0, 0, 0))
                screen.blit(texte_cinematique, (700, 450))
            if 960 < cpt_cinematique < 1000:
                self.maman.rect.x -= 5
            if 1020 < cpt_cinematique < 1070:
                self.maman.rect.x += 5
            if 1070 < cpt_cinematique < 1130:
                texte_cinematique = myfont.render("Le devoir m'appelle!", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 1130 < cpt_cinematique < 1180:
                texte_cinematique = myfont.render("D'ailleurs Tim j'adors ta playlist sur deezer", False, (0, 0, 0))
                screen.blit(texte_cinematique, (900, 300))
            if 1180 < cpt_cinematique < 1330:
                self.papa.rect.x += 5
            if 1230 < cpt_cinematique < 1270:
                texte_cinematique = myfont.render("Angelaaa appelle moi ce soiiir...", False, (0, 0, 0))
                screen.blit(texte_cinematique, (1100, 200))
            if 1270 < cpt_cinematique < 1330:
                self.papa.rect.x += 5
            if 1330 < cpt_cinematique < 1370:
                self.papa.rect.x -= 5
            if 1330 < cpt_cinematique < 1390:
                texte_cinematique = myfont.render("Ah oui j'avais oublié de vous dire", False, (0, 0, 0))
                screen.blit(texte_cinematique, (1100, 200))
            if 1400 < cpt_cinematique < 1450:
                texte_cinematique = myfont.render("Je garde cela pour Max", False, (0, 0, 0))
                screen.blit(texte_cinematique, (1200, 200))
            if 1420 < cpt_cinematique:
                surface.blit(self.avenir.image, self.avenir.rect)
            if 1440 < cpt_cinematique:
                self.papa.rect.x += 10
                self.avenir.rect.x += 10

        # Normalement dans cette méthode il n'y a que des méthodes qui sont appellés et pas de code

        # Je peux faire une méthode pour toutes les appliques

        # appliquer les blocs par niveau
        if niveau == 1:
            pass  # Il n'y a pas de blocs a appliquer pour le niveau 1
        elif niveau == 2:
            self.bloc_niveau2.draw(surface)
        elif niveau == 3:
            self.bloc_niveau3.draw(surface)
        elif niveau == 4:
            self.bloc_niveau4.draw(surface)
        elif niveau == 5:
            self.bloc_niveau5.draw(surface)
        elif niveau == 6:
            self.bloc_niveau6.draw(surface)
            surface.blit(self.generateur1.image, self.generateur1.rect)  # En plus d'appliquer les blocs on applique a certains niveaux des generateurs ou des teleporteur
        elif niveau == 7:
            self.bloc_niveau7.draw(surface)
            surface.blit(self.teleporteur1_1.image, self.teleporteur1_1.rect)
            surface.blit(self.teleporteur1_2.image, self.teleporteur1_2.rect)
        elif niveau == 8:
            self.bloc_niveau8.draw(surface)
            surface.blit(self.generateur2.image, self.generateur2.rect)
            global appliquer_blocs_generateur2
            if appliquer_blocs_generateur2:  # Ça sert juste a appliquer les blocs avant loulou pour que loulou soit devant les blocs
                self.bloc_generateur_2.draw(surface)
        elif niveau == 9:
            self.bloc_niveau9.draw(surface)
            surface.blit(self.generateur3.image, self.generateur3.rect)
            surface.blit(self.generateur4.image, self.generateur4.rect)

        # appliquer les joueur
        surface.blit(self.loulou.image, self.loulou.rect)
        self.loulou.update_animation_repeat()
        # en faire un 2eme pour tim
        surface.blit(self.tim.image, self.tim.rect)
        self.tim.update_animation_repeat()

        # appliquer le reload, le menu et le niveau
        surface.blit(reload, (reload_rect.x, reload_rect.y))
        surface.blit(menu, (menu_rect.x, menu_rect.y))
        text = "niveau " + str(niveau)
        textsurface = myfont.render(text, False, (0, 0, 0))
        surface.blit(textsurface, (surface.get_width() - 160, 30))

        # appliquer la gravité à chaques frames
        self.loulou.gravite()
        self.tim.gravite()

        # vérifier que le perso n'est pas allé trop bas à cause de la gravité
        if self.tim.rect.y > 785:
            self.tim.rect.y = 785
            self.tim.etat_descente_saut = False
        if self.loulou.rect.y > 785:
            self.loulou.rect.y = 785

        # vérifier que tim n'est pas sur loulou
        if self.tim.rect.colliderect(self.loulou.rectangle_loulou_up()):
            self.tim.rect.y -= self.tim.gravite_bas
            game.tim.etat_descente_saut = False

        # A mettre dans une méthode de classe
        global touche_gauche_loulou
        global touche_gauche_tim
        global touche_droite_loulou
        global touche_droite_tim
        global cpt_saut_loulou
        if self.loulou.etat_saut:
            cpt_saut_loulou += 1
            self.loulou.saut()
            if self.pressed.get(touche_droite_loulou):
                self.loulou.name = "loulou_saute_droite"
            else:
                self.loulou.name = "loulou_saute_gauche"
            self.loulou.update_images()
            self.loulou.start_animation()
            self.loulou.update_animation_no_repeat()
            if cpt_saut_loulou >= 11:
                cpt_saut_loulou = 0
                self.loulou.etat_saut = False
                self.loulou.etat_descente_saut = True
        elif self.loulou.etat_descente_saut:
            cpt_saut_loulou += 1
            if cpt_saut_loulou > 11:
                cpt_saut_loulou = 0
                self.loulou.etat_descente_saut = False

        global cpts_saut_tim
        if self.tim.etat_saut:
            cpts_saut_tim += 1
            self.tim.saut()
            if self.pressed.get(touche_droite_tim):
                self.tim.name = "tim_saute_droite"
            else:
                self.tim.name = "tim_saute_gauche"
            self.tim.update_images()
            self.tim.start_animation()
            self.tim.update_animation_no_repeat()
            if cpts_saut_tim >= 11:
                cpts_saut_tim = 0
                self.tim.etat_saut = False
                self.tim.etat_descente_saut = True

        global dernier_appuye
        global dernier_appuyes
        global compteur_chgmt_touche

        compteur_chgmt_touche += 1

        if compteur_chgmt_touche >= 300:
            compteur_chgmt_touche = 0

            echangeur_touche_gauche = touche_gauche_tim
            touche_gauche_tim = touche_gauche_loulou
            touche_gauche_loulou = echangeur_touche_gauche

            echangeur_touche_droite = touche_droite_loulou
            touche_droite_loulou = touche_droite_tim
            touche_droite_tim = echangeur_touche_droite

        # déplacement du joueur
        if self.pressed.get(touche_droite_loulou) and self.loulou.rect.x < surface.get_width() - 120:  # la taille du png
            self.loulou.move_right()
            self.loulou.name = "loulou_cour_droite"
            if self.loulou.etat_saut:
                self.loulou.name = "loulou_saute_droite"
            self.loulou.update_images()
            self.loulou.start_animation()
            dernier_appuye = 0
        elif self.pressed.get(touche_gauche_loulou) and self.loulou.rect.x > 0:
            self.loulou.move_left()
            self.loulou.name = "loulou_cour_gauche"
            if self.loulou.etat_saut:
                self.loulou.name = "loulou_saute_gauche"
            self.loulou.start_animation()
            self.loulou.update_images()
            dernier_appuye = 1
        else:  # quand les perso ne sont pas en mouvement ils sont arreter à droite ou a gauche
            if dernier_appuye == 0:  # dernier_appuye détermine si le personnage allait à gauche ou a droite avant de s'arreter
                self.loulou.image = pygame.image.load("loulou_cour_droite.png")
                self.loulou.image = pygame.transform.scale(self.loulou.image, self.loulou.size)
            else:
                self.loulou.image = pygame.image.load("loulou_cour_gauche.png")
                self.loulou.image = pygame.transform.scale(self.loulou.image, self.loulou.size)

        if self.pressed.get(touche_droite_tim) and self.tim.rect.x < surface.get_width() - 120:
            self.tim.move_right()
            self.tim.name = "tim_cour_droite"
            if self.tim.etat_saut:
                self.tim.name = "tim_saute_droite"
            self.tim.start_animation()
            self.tim.update_images()
            dernier_appuyes = 0
        elif self.pressed.get(touche_gauche_tim) and self.tim.rect.x > 0:
            self.tim.move_left()
            self.tim.name = "tim_cour_gauche"
            if self.tim.etat_saut:
                self.tim.name = "tim_saute_gauche"
            self.tim.start_animation()
            self.tim.update_images()
            dernier_appuyes = 1
        else:
            if dernier_appuyes == 0:
                self.tim.image = pygame.image.load("tim_cour_droite.png")
                self.tim.image = pygame.transform.scale(self.tim.image, self.tim.size)
            else:
                self.tim.image = pygame.image.load("tim_cour_gauche.png")
                self.tim.image = pygame.transform.scale(self.tim.image, self.tim.size)

        # vérifier la collision de Tim avec les blocs
        # A mettre après le déplacement mais avant l'application des personnages
        if niveau == 1:
            pass  # Il n'y a pas de blocs au niveau 1
        elif niveau == 2:
            self.appliquer_bloc(self.bloc3)
        elif niveau == 3:
            self.appliquer_bloc(self.bloc2)
            self.appliquer_bloc(self.bloc8)
        elif niveau == 4:
            self.appliquer_bloc(self.bloc2)
        elif niveau == 5:
            self.appliquer_bloc(self.bloc12)
            self.appliquer_bloc(self.bloc11)
        elif niveau == 6:
            self.appliquer_bloc(self.bloc13)
            self.appliquer_bloc(self.bloc14)
            generation()
        elif niveau == 7:
            teleportation()
        elif niveau == 8:
            if self.tim.rect.colliderect(self.generateur2.rectangle_for_collision()) or self.loulou.rect.colliderect(self.generateur2.rectangle_for_collision()):
                self.generateur2.update_images()
                self.generateur2.start_animation()
                self.generateur2.animate()
                appliquer_blocs_generateur2 = False
            else:
                self.generateur2.image = pygame.image.load("generateur.png")
                self.generateur2.image = pygame.transform.scale(self.generateur2.image, self.generateur2.size)
                appliquer_blocs_generateur2 = True
                self.appliquer_bloc(self.bloc20)
                self.appliquer_bloc(self.bloc7)
                self.appliquer_bloc(self.bloc17)
                self.appliquer_bloc(self.bloc18)
                self.appliquer_bloc(self.bloc19)
                self.appliquer_bloc(self.bloc21)
        elif niveau == 9:
            # 22 23 25
            self.appliquer_bloc_bas(self.bloc22)
            self.appliquer_bloc_haut(self.bloc25)
            self.appliquer_bloc_haut(self.bloc23)
            self.appliquer_bloc_haut(self.bloc26)
            self.appliquer_bloc_haut(self.bloc27)

            if self.tim.rect.colliderect(self.generateur3.rectangle_for_collision()) or self.loulou.rect.colliderect(
                    self.generateur3.rectangle_for_collision()):
                self.generateur3.update_images()
                self.generateur3.start_animation()
                self.generateur3.animate()
                self.appliquer_bloc_haut(self.bloc24)
                surface.blit(self.bloc24.image, self.bloc24.rect)
                surface.blit(self.teleporteur2.image, self.teleporteur2.rect)

                global cpt1_teleporteur_tim
                if self.tim.rect.colliderect(self.teleporteur2.rectangle_for_collision()):
                    cpt1_teleporteur_tim += 1
                    if cpt1_teleporteur_tim > 20:  # screen.get_width() - 166, screen.get_height() - background_sol.get_height() - 83 * 5
                        self.tim.rect.x = screen.get_width() - 166
                        self.tim.rect.y = screen.get_height() - background_sol.get_height() - 83 * 5 - self.teleporteur2.rect.h + 60
                        cpt1_teleporteur_tim = 0
                else:
                    cpt1_teleporteur_tim = 0
            else:
                self.generateur3.image = pygame.image.load("generateur.png")
                self.generateur3.image = pygame.transform.scale(self.generateur3.image, self.generateur3.size)

            if self.tim.rect.colliderect(self.generateur4.rectangle_for_collision()) or self.loulou.rect.colliderect(self.generateur4.rectangle_for_collision()):
                self.generateur4.update_images()
                self.generateur4.start_animation()
                self.generateur4.animate()
                self.appliquer_bloc_haut(self.bloc24)

            else:
                self.generateur4.image = pygame.image.load("generateur.png")
                self.generateur4.image = pygame.transform.scale(self.generateur4.image, self.generateur4.size)
                surface.blit(self.bloc16.image, self.bloc16.rect)
                if self.check_collision(self.loulou, self.bloc_pique9_generateur):
                    self.game_over()

        self.tim.verifie_pique()
        self.loulou.verifie_pique()

        if self.loulou.rect.x > screen.get_width() - 300 and self.tim.rect.x > screen.get_width() - 300:
            self.game_win()


game = Game()


def musique_play_jeu(nom):
    global demarrer_musique_play
    global passe_la
    global passe_ici
    nom_musique_sound = pygame.mixer.Sound(f'musique/{nom}.mp3')
    pygame.mixer.Sound.set_volume(nom_musique_sound, 0.1)
    channel2.pause()
    if not demarrer_musique_play:
        channel1.play(nom_musique_sound)
        channel1.pause()
        demarrer_musique_play = True
    channel1.unpause()
    passe_la = True
    passe_ici = False


def musique_play_menu(nom):
    global demarrer_musique_menu
    global passe_la
    global passe_ici
    nom_musique_sound = pygame.mixer.Sound(f'musique/{nom}.mp3')
    pygame.mixer.Sound.set_volume(nom_musique_sound, 0.1)
    channel1.pause()
    if not demarrer_musique_menu:
        channel2.play(nom_musique_sound)
        channel2.pause()
        demarrer_musique_menu = True
    channel2.unpause()
    passe_ici = True
    passe_la = False


def lancer_musique_jeu():
    if niveau == 1 and not passe_la:  # Créer une liste avec le nom de toutes les musiques puis faire une boucle
        musique_play_jeu("Drug")
    if niveau == 2 and not passe_la:
        musique_play_jeu("Birds")
    if niveau == 3 and not passe_la:
        musique_play_jeu("follow_you")
    if niveau == 4 and not passe_la:
        musique_play_jeu("I'm Still Standing")
    if niveau == 5 and not passe_la:
        musique_play_jeu("quicker")
    if niveau == 6 and not passe_la:
        musique_play_jeu("let_me_down")
    if niveau == 7 and not passe_la:
        musique_play_jeu("WHAT YOU KNOW")
    if niveau == 8 and not passe_la:
        musique_play_jeu("No Time To Die")
    if niveau == 9 and not passe_la:
        musique_play_jeu("UR SO FKING COOL")


def lancer_musique_menu():
    # demarrer les diff musiques de menu et stoper les musiques de jeu

    if niveau == 1 and not passe_ici:
        musique_play_menu("cant_sleep")
    if niveau == 2 and not passe_ici:
        musique_play_menu("Gloria")
    if niveau == 3 and not passe_ici:
        musique_play_menu("Everybody Talks")
    if niveau == 4 and not passe_ici:
        musique_play_menu("Je te promets")
    if niveau == 5 and not passe_ici:
        musique_play_menu("Legendary")
    if niveau == 6 and not passe_ici:
        musique_play_menu("Lollipop")
    if niveau == 7 and not passe_ici:
        musique_play_menu("Weight Of Living, Pt. I")
    if niveau == 8 and not passe_ici:
        musique_play_menu("unstoppable")
    if niveau == 9 and not passe_ici:
        musique_play_menu("Wish I Knew You")


is_son_marche = True

running = True
while running:

    screen.blit(background_ciel, (0, 0))  # Décor
    screen.blit(background_sol, (0, screen.get_height() - background_sol.get_height()))
    screen.blit(drapeau, (screen.get_width() - 300, screen.get_height() - background_sol.get_height() - drapeau.get_height()))

    if is_son_marche:
        screen.blit(son_marche, (son_marche_rect.x, son_marche_rect.y))
    else:
        screen.blit(son_eteint, (son_eteint_rect.x, son_eteint_rect.y))
        channel1.stop()  # arrete les 2 musiques
        channel2.stop()  # les musiques reprendront ensuite depuis le début

    if game.is_playing:

        lancer_musique_jeu()

        # lancer les instructions de la partie
        game.update(screen)

    else:
        # ajouter mon écran de bienvenue
        screen.blit(play_button, play_button_rect)
        tgt = "a"
        tdt = "a"
        tgl = "a"
        tdl = "a"
        if touche_gauche_tim == 113:
            tgt = "Q"
            tdt = "D"
            tgl = "K"
            tdl = "M"
        elif touche_gauche_tim == 107:
            tgt = "K"
            tdt = "M"
            tgl = "Q"
            tdl = "D"

        touche_explication = myfont.render(f"Tim gauche {tgt}   --   Tim droite {tdt}   --   Loulou gauche {tgl}   --   Loulou droite {tdl}   --   Saut espace", False, (235, 235, 235))
        screen.blit(touche_explication, (100, screen.get_height() - 100))

        lancer_musique_menu()

    pygame.display.flip()  # mettre à jour l'écran

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if is_bouton_marche:
                game.pressed[event.key] = True
                if event.key == pygame.K_SPACE:
                    if game.is_playing:
                        if not game.loulou.etat_saut and not game.tim.etat_saut and not game.loulou.etat_descente_saut and not game.tim.etat_descente_saut:
                            game.loulou.etat_saut = True
                            game.tim.etat_saut = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # verification pour savoir si la souris a appuyé
            if play_button_rect.collidepoint(event.pos):
                # mettre le jeu en mode lancé
                if not game.is_playing:
                    game.start()
            if reload_rect.collidepoint(event.pos):
                game.game_over()
                game.is_playing = True
            if menu_rect.collidepoint(event.pos):
                game.game_over()
            if son_marche_rect.collidepoint(event.pos) or son_eteint_rect.collidepoint(event.pos):
                passe_la = False
                passe_ici = False
                demarrer_musique_menu = False
                demarrer_musique_play = False
                if is_son_marche:
                    is_son_marche = False
                else:
                    is_son_marche = True
                    if game.is_playing:
                        lancer_musique_jeu()
                    else:
                        lancer_musique_menu()
    # fixer le nb de fps
    clock.tick(FPS)

# + de 1200 lignes de code!
