import pygame
import sys
import tkinter as tk
from tkinter import filedialog, Listbox, Button, Scrollbar, Label
import os


# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu de démarrage - Jeu de rythme")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
PURPLE = (70, 50, 200)

# Police d'écriture
title_font = pygame.font.Font(None, 100)
font = pygame.font.Font(None, 30)

# Charger l'image de fond
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Dimensions des éléments
button_width = 220
button_height = 40
dropdown_button_width = 400
dropdown_button_height = 40
selectsong_button_width = 400
selectsong_button_height = 40

# Calcul des positions centrées
title_y = 20
button_x = (screen_width - button_width) // 2
button_y = 350
selectsong_button_x = (screen_width - dropdown_button_width) // 2
selectsong_button_y = 270
dropdown_button_x = (screen_width - dropdown_button_width) // 2
dropdown_button_y = 430

# Bouton de validation
button_box = pygame.Rect(button_x, button_y, button_width, button_height)
button_text = "Valider et jouer"

# Bouton du menu déroulant d'édition
dropdown_button_box = pygame.Rect(dropdown_button_x, dropdown_button_y, dropdown_button_width, dropdown_button_height)
dropdown_button_text = " Editer la liste des fichiers MP3"

# Bouton du menu déroulant de sélection
selectsong_button_box = pygame.Rect(selectsong_button_x, selectsong_button_y, selectsong_button_width, selectsong_button_height)
selectsong_button_text = " Sélectionner la musique"

# Liste des fichiers MP3 précédemment utilisés
mp3_files = []

# Créer l'interface Tkinter pour le menu déroulant
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale Tkinter

class Editeur:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Editer les fichiers MP3")
        
        self.label = Label(self.window, text="Liste des fichiers MP3")
        self.label.pack()
        
        self.listbox = Listbox(self.window, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        
        self.scrollbar = Scrollbar(self.window, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.add_button = Button(self.window, text="Ajouter un fichier", command=self.add_file)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.remove_button = Button(self.window, text="Supprimer le fichier", command=self.remove_file)
        self.remove_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.select_button = Button(self.window, text="Valider et retourner", command=self.validate_and_return)
        self.select_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.selected_file = None
        self.update_listbox()
        
    def add_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers MP3", "*.mp3")])
        if file_path:
            if file_path not in mp3_files:
                mp3_files.append(file_path)
                self.update_listbox()
    
    def remove_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            mp3_files.pop(selected_index[0])
            self.update_listbox()
    
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in mp3_files:
            self.listbox.insert(tk.END, file)
    
    def validate_and_return(self):
        self.parent.selectsong_button_text = dropdown_button_text
        self.window.destroy()

class Selecteur:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        
        self.label = Label(self.window, text="Liste des fichiers MP3")
        self.label.pack()
        
        self.listbox = Listbox(self.window, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        
        self.scrollbar = Scrollbar(self.window, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.select_button = Button(self.window, text="Sélectionner le fichier", command=self.select_file)
        self.select_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.select_button = Button(self.window, text="Retourner au menu", command=self.return_menu)
        self.select_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Afficher les fichiers dans le menu déroulant
        for file in mp3_files:
            self.listbox.insert(tk.END, file)

    def select_file(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.parent.selectsong_button_text = mp3_files[selected_index[0]]
            # Mettre à jour le bouton "Sélectionner la musique"
            MainGame().draw_selectsong_button()
            self.window.destroy()

    def return_menu(self):
        self.parent.selectsong_button_text = selectsong_button_text
        self.window.destroy()

class MainGame:
    def __init__(self):
        pass
    
    def draw_selectsong_button(self):
        # Effacez l'ancien texte
        pygame.draw.rect(screen, WHITE, selectsong_button_box)
        pygame.draw.rect(screen, GRAY, selectsong_button_box, 2)
        draw_text(screen, selectsong_button_text, selectsong_button_box, font, BLACK)

def draw_text(surface, text, rect, font, color=BLACK):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center

    if text_rect.width > rect.width:
        # Tronquer le texte si nécessaire
        while text_rect.width > rect.width and len(text) > 0:
            text = text[:-1]
            text_surface = font.render(text + "...", True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = rect.center

    surface.blit(text_surface, text_rect.topleft)

def run_loading_screen():
    # Recharger l'image de fond pour la page de chargement
    background_image = pygame.image.load("background.jpg")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    # Police de texte
    font = pygame.font.SysFont(None, 36)

    # Variables de la barre de chargement
    largeur_barre = 600
    hauteur_barre = 50
    x_barre = (screen_width - largeur_barre) // 2
    y_barre = (screen_height - hauteur_barre) // 2
    largeur_remplissage = 0

    # Variables d'état des étapes
    etat_etape1 = False
    etat_etape2 = False
    etat_etape3 = False

    # Textes des étapes
    etape1_texte = "Recherche du tempo..."
    etape2_texte = "Analyse de la structure de la musique..."
    etape3_texte = "Traduction en fichier txt..."

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mise à jour de la barre de chargement
        largeur_remplissage = min(largeur_barre * 0.1, largeur_remplissage + 1)
        etape_courante_texte = etape1_texte
        if etat_etape1:
            largeur_remplissage = min(largeur_barre * 0.4, largeur_remplissage + 1.2)
            etape_courante_texte = etape2_texte
        elif etat_etape2:
            largeur_remplissage = min(largeur_barre * 0.8, largeur_remplissage + 1.4)
            etape_courante_texte = etape3_texte
        elif etat_etape3:
            largeur_remplissage = min(largeur_barre * 1, largeur_remplissage + 3)

        # Affichage
        screen.blit(background_image, (0, 0))
        pygame.draw.rect(screen, WHITE, (x_barre, y_barre, largeur_barre, hauteur_barre))
        pygame.draw.rect(screen, PURPLE, (x_barre, y_barre, largeur_remplissage, hauteur_barre))

        # Affichage du texte de l'étape courante
        texte = font.render(etape_courante_texte, True, WHITE)
        screen.blit(texte, (x_barre, y_barre - 40))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def run_tutorial_screen() :
    buttons_width = 220
    buttons_height = 40

    screen_width = 600
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Page de tutoriel - Jeu de rythme")
    tutorial_image = pygame.image.load("tutorial1.jpg")
    tutorial_image = pygame.transform.scale(tutorial_image, (screen_width-100, screen_height-100))
    
    right_button_x = 3*((screen_width - button_width) // 4)
    left_button_x = (screen_width - button_width) // 4
    buttons_y= 350


    button1_box = pygame.Rect(right_button_x, buttons_y, buttons_width, buttons_height)
    button1_text = "Suivant"
    pygame.draw.rect(screen, WHITE, button1_box)
    pygame.draw.rect(screen, BLACK, button1_box, 2)
    draw_text(screen, button1_text, button1_box, font, WHITE)

    button2_box = pygame.Rect(left_button_x, buttons_y, buttons_width, buttons_height)
    button2_text = "Précédent"
    pygame.draw.rect(screen, WHITE, button2_box)
    pygame.draw.rect(screen, BLACK, button2_box, 2)
    draw_text(screen, button2_text, button2_box, font, WHITE)

    button3_box = pygame.Rect(right_button_x, buttons_y, buttons_width, buttons_height)
    button3_text = "Fermer et jouer"
    pygame.draw.rect(screen, WHITE, button3_box)
    pygame.draw.rect(screen, BLACK, button3_box, 2)
    draw_text(screen, button3_text, button3_box, font, WHITE)

    while True :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_box.collidepoint(event.pos):
                    tutorial_image2 = pygame.image.load("tutorial2.jpg")
                    tutorial_image2= pygame.transform.scale(tutorial_image, (screen_width-100, screen_height-100))
                    button2_box = pygame.Rect(left_button_x, buttons_y, buttons_width, buttons_height)
                    button2_text = "Précédent"
                    pygame.draw.rect(screen, WHITE, button2_box)
                    pygame.draw.rect(screen, BLACK, button2_box, 2)
                    draw_text(screen, button2_text, button2_box, font, WHITE)

                 
                if button2_box.collidepoint(event.pos):

                if button3_box.collidepoint(event.pos) :


def main(clock):
    global dropdown_button_text, selectsong_button_text

    screen.blit(background_image, (0, 0))

    # Afficher le titre du jeu
    title_text = "Solar Sonic"
    title_rect = pygame.Rect(0, title_y, screen_width, 200)
    draw_text(screen, title_text, title_rect, title_font, WHITE)

    # Afficher le bouton de validation
    pygame.draw.rect(screen, PURPLE, button_box)
    pygame.draw.rect(screen, BLACK, button_box, 2)
    draw_text(screen, button_text, button_box, font, WHITE)

    # Afficher le bouton du menu déroulant éditeur
    pygame.draw.rect(screen, WHITE, dropdown_button_box)
    pygame.draw.rect(screen, BLACK, dropdown_button_box, 2)
    draw_text(screen, dropdown_button_text, dropdown_button_box, font, BLACK)

    # Afficher le bouton du menu déroulant sélection
    pygame.draw.rect(screen, WHITE, selectsong_button_box)
    pygame.draw.rect(screen, BLACK, selectsong_button_box, 2)
    draw_text(screen, selectsong_button_text, selectsong_button_box, font, BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if dropdown_button_box.collidepoint(event.pos):
                    # Ouvrir le menu déroulant Tkinter (éditeur)
                    file_editor = Editeur(root)
                    root.wait_window(file_editor.window)
                if selectsong_button_box.collidepoint(event.pos):
                    # Ouvrir le menu déroulant Tkinter (sélection)
                    file_selector = Selecteur(root)
                    root.wait_window(file_selector.window)
                    file_path = file_selector.parent.selectsong_button_text
                    selectsong_button_text = os.path.basename(file_path)
                    pygame.draw.rect(screen, WHITE, selectsong_button_box)
                    pygame.draw.rect(screen, BLACK, selectsong_button_box, 2)
                    draw_text(screen, selectsong_button_text, selectsong_button_box, font, BLACK)
                if button_box.collidepoint(event.pos) and selectsong_button_text != " Sélectionner la musique":
                    print("Fichier MP3 sélectionné:", file_path)
                    run_loading_screen()
                    run_tutorial_screen()
                else:
                    draw_text(screen, "Veuillez sélectionner une musique !", pygame.Rect(0, 100, screen_width, 200), pygame.font.Font(None, 30), WHITE)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    clock = pygame.time.Clock()
    main(clock)