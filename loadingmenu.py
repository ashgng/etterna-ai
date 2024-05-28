import pygame
import time

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Page de chargement")

# Charger l'image de fond
image_fond = pygame.image.load("background.jpg")
image_fond = pygame.transform.scale(image_fond, (largeur, hauteur))

# Couleurs
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
PURPLE = (70, 50, 200)

# Police de texte
font = pygame.font.SysFont(None, 36)

# Variables de la barre de chargement
largeur_barre = 600
hauteur_barre = 50
x_barre = (largeur - largeur_barre) // 2
y_barre = (hauteur - hauteur_barre) // 2
largeur_remplissage = 0

# Variables d'état des étapes
etat_etape1 = False
etat_etape2 = False
etat_etape3 = False

# Textes des étapes
etape1_texte = "Recherche du tempo..."
etape2_texte = "Analyse de la structure de la musique..."
etape3_texte = "Traduction en fichier txt..."

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mise à jour de la barre de chargement
    largeur_remplissage = min(largeur_barre * 0.1, largeur_remplissage + 1)
    etape_courante_texte = etape1_texte
    if etat_etape1 :
        largeur_remplissage = min(largeur_barre * 0.4, largeur_remplissage + 1.2)
        etape_courante_texte = etape2_texte
    elif etat_etape2 :
        largeur_remplissage = min(largeur_barre * 0.8, largeur_remplissage + 1.4)
        etape_courante_texte = etape3_texte
    elif etat_etape3 :
        largeur_remplissage = min(largeur_barre * 1, largeur_remplissage + 3)

    # Affichage
    fenetre.blit(image_fond, (0,0))
    pygame.draw.rect(fenetre, BLANC, (x_barre, y_barre, largeur_barre, hauteur_barre))
    pygame.draw.rect(fenetre, PURPLE, (x_barre, y_barre, largeur_remplissage, hauteur_barre))
    

    # Affichage du texte de l'étape courante
    texte = font.render(etape_courante_texte, True, BLANC)
    fenetre.blit(texte, (x_barre, y_barre - 40))
    
    
    pygame.display.flip()
    
    # Limiter la vitesse de la boucle
    pygame.time.Clock().tick(30)

pygame.quit()