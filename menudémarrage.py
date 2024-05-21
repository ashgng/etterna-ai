import pygame
import sys
import tkinter as tk
from tkinter import filedialog

# Initialisation de Pygame
pygame.init()

# Initialisation de Tkinter
root = tk.Tk()
root.withdraw()  # Masquer la fenêtre principale de Tkinter

# Dimensions de la fenêtre
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu de démarrage - Jeu de rythme")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Police d'écriture
font = pygame.font.Font(None, 36)

# Charger l'image de fond
background_image = pygame.image.load("menu démarrage.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Dimensions des éléments
drag_drop_width = 400
drag_drop_height = 100
button_width = 150
button_height = 40
dropdown_width = 400
dropdown_height = 40

# Calcul des positions centrées
drag_drop_x = (screen_width - drag_drop_width) // 2
drag_drop_y = 100
button_x = (screen_width - button_width) // 2
button_y = 220
dropdown_box_x = (screen_width - dropdown_width) // 2
dropdown_box_y = 300

# Zone de drag and drop pour le fichier MP3
drag_drop_box = pygame.Rect(drag_drop_x, drag_drop_y, drag_drop_width, drag_drop_height)
drag_drop_text = "Déposez un fichier mp3 ici"

# Bouton de validation
button_box = pygame.Rect(button_x, button_y, button_width, button_height)
button_text = "Valider"

# Liste des fichiers MP3 précédemment utilisés
mp3_files = []

# Menu déroulant pour les fichiers MP3 précédemment utilisés
dropdown_box = pygame.Rect(dropdown_box_x, dropdown_box_y, dropdown_width, dropdown_height)
dropdown_open = False
selected_file = None

def draw_text(surface, text, position, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def main():
    global drag_drop_text, dropdown_open, selected_file

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if drag_drop_box.collidepoint(event.pos):
                    # Ouvrir la boîte de dialogue pour sélectionner un fichier MP3
                    file_path = filedialog.askopenfilename(filetypes=[("Fichiers MP3", "*.mp3")])
                    if file_path:
                        drag_drop_text = file_path
                        if file_path and file_path not in mp3_files:
                            mp3_files.append(file_path)
                if button_box.collidepoint(event.pos):
                    print("Fichier MP3 sélectionné:", drag_drop_text)
                    if drag_drop_text and drag_drop_text not in mp3_files:
                        mp3_files.append(drag_drop_text)
                
                if dropdown_box.collidepoint(event.pos):
                    dropdown_open = not dropdown_open
                else:
                    dropdown_open = False
                if dropdown_open:
                    for i, file in enumerate(mp3_files):
                        file_rect = pygame.Rect(dropdown_box_x, dropdown_box_y + 40 + 30 * i, 370, 30)
                        delete_rect = pygame.Rect(dropdown_box_x + 370, dropdown_box_y + 40 + 30 * i, 30, 30)
                        if delete_rect.collidepoint(event.pos):
                            mp3_files.pop(i)
                            if selected_file == file:
                                selected_file = None
                            break
                        if file_rect.collidepoint(event.pos):
                            selected_file = file
                            dropdown_open = False  # Fermer le menu déroulant après sélection
            elif event.type == pygame.DROPFILE:
                file_path = event.file
                if file_path.endswith(".mp3"):
                    drag_drop_text = file_path
                    if file_path not in mp3_files:
                        mp3_files.append(file_path)

        screen.blit(background_image, (0, 0))

        # Afficher la zone de drag and drop
        pygame.draw.rect(screen, GRAY, drag_drop_box, 2)
        draw_text(screen, drag_drop_text, (drag_drop_box.x + 5, drag_drop_box.y + 35), font, BLACK)

        # Afficher le bouton de validation
        pygame.draw.rect(screen, BLUE, button_box)
        draw_text(screen, button_text, (button_box.x + 20, button_box.y + 5), font, WHITE)

        # Afficher le menu déroulant
        pygame.draw.rect(screen, GRAY, dropdown_box, 2)
        if dropdown_open:
            for i, file in enumerate(mp3_files):
                file_rect = pygame.Rect(dropdown_box_x, dropdown_box_y + 40 + 30 * i, 370, 30)
                delete_rect = pygame.Rect(dropdown_box_x + 370, dropdown_box_y + 40 + 30 * i, 30, 30)
                pygame.draw.rect(screen, WHITE, file_rect)
                pygame.draw.rect(screen, RED, delete_rect)
                draw_text(screen, file, (file_rect.x + 5, file_rect.y + 5), font, BLACK)
                draw_text(screen, 'X', (delete_rect.x + 5, delete_rect.y + 5), font, BLACK)
        else:
            if selected_file:
                draw_text(screen, selected_file, (dropdown_box.x + 5, dropdown_box.y + 5), font, BLACK)
            else:
                draw_text(screen, "Sélectionner un fichier MP3", (dropdown_box.x + 5, dropdown_box.y + 5), font, BLACK)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()