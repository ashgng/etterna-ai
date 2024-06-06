import pygame.gfxdraw

def blur_surface(surface, amount):
    scale = 1.0 / amount
    surf_size = surface.get_size()
    scaled_surf = pygame.transform.smoothscale(surface, (int(surf_size[0] * scale), int(surf_size[1] * scale)))
    return pygame.transform.smoothscale(scaled_surf, surf_size)

def darken_surface(surface, darkness):
    dark_overlay = pygame.Surface(surface.get_size())
    dark_overlay.fill((0, 0, 0))
    dark_overlay.set_alpha(darkness)
    surface.blit(dark_overlay, (0, 0))

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Load the background image
background = pygame.image.load('background.jpg')

# Ensure the background is the same size as the screen
background = pygame.transform.scale(background, (800, 600))

# Blur the background
blurred_background = blur_surface(background, 4)  # Adjust the blur amount

# Darken the background
darken_surface(blurred_background, 150)  # Adjust the darkness amount (0-255)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw the background
    screen.blit(blurred_background, (0, 0))
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()