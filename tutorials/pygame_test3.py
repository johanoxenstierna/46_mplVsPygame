import pygame
import numpy as np
import sys
from scipy.stats import norm


WRITE = 0  # Set to True to write to file
FPS = 60

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)

backgr_b = pygame.image.load('./pictures/backgr_b.png').convert()
backgr_55 = pygame.image.load('./pictures/backgr_55.jpg').convert_alpha()
backgr_55.set_alpha(25)  # ~10% opacity

# Load O1
O1_names = ['1_OgunL.png', '2_VenusL.png', '3_MolliL.png', '3_NauvisL.png', '6_JupiterL.png']
O1 = []
O1_rects = []

for name in O1_names:
    try:
        img = pygame.image.load(f'./pictures/Calidus1/planets/{name}')
        O1.append(img)
        O1_rects.append(img.get_rect())
    except pygame.error as e:
        print(f"Error loading image {name}: {e}")

# Pre-computed transformations
num_images = len(O1)
orbit_radius = 150

# Set initial positions for O1
for i, rect in enumerate(O1_rects):
    rect.center = (width // 2, height // 2)  # Start at the center

# Create small objects
num_R = 10
R = [pygame.Surface((np.random.randint(1, 6), np.random.randint(1, 6))) for _ in range(num_R)]
for obj in R:
    obj.fill((255, 255, 255))  # White small objects

# Set initial positions for small objects
R_rects = [obj.get_rect(center=(np.random.randint(0, width), np.random.randint(0, height))) for obj in R]

clock = pygame.time.Clock()

# Main loop =================================================================
NUM_FRAMES = 381
num_images = len(O1)

# --- Alpha (Gaussian shape per O1) ---
x = np.linspace(0, 1, NUM_FRAMES)  # normalized time
alphas = np.zeros((NUM_FRAMES, num_images))

# Each object peaks at a slightly different time
peaks = np.linspace(0.3, 0.7, num_images)
for i in range(num_images):
    pdf = norm.pdf(x, loc=peaks[i], scale=0.1)
    pdf = (pdf - pdf.min()) / (pdf.max() - pdf.min())  # normalize to 0–1
    alphas[:, i] = (pdf * 255).astype(np.uint8)

# --- Zorder (shifted identity pattern) ---
zorders = np.zeros((NUM_FRAMES, num_images), dtype=int)
base_order = np.arange(num_images)

for f in range(NUM_FRAMES):
    # Rotate the base order slightly every frame
    shift = f // (NUM_FRAMES // num_images)
    zorders[f] = np.roll(base_order, shift)


base_radius = 150
orbit_radii = np.linspace(base_radius, base_radius - 130, num_images)  # smaller radii to cluster


frame_count = 0
while frame_count < NUM_FRAMES:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Clear the screen
    # screen.blit(background, (0, 0))

    screen.blit(backgr_b, (0, 0))
    screen.blit(backgr_55, (0, 0))

    # Use zorder sorting
    draw_order = np.argsort(zorders[frame_count])  # from back to front

    for i in draw_order:
        angle = frame_count * 0.02 + (i * (2 * np.pi / num_images))
        radius = orbit_radii[i]
        x = (width // 2) + radius * np.cos(angle)
        y = (height // 2) + radius * np.sin(angle)

        scaled_img = pygame.transform.scale(O1[i], (int(O1[i].get_width() * 0.5), int(O1[i].get_height() * 0.5)))
        scaled_img.set_alpha(alphas[frame_count, i])

        rect = O1_rects[i]
        rect.center = (x, y)

        screen.blit(scaled_img, rect)


    # Draw small objects
    for rocket_rect in R_rects:
        screen.blit(R[0], rocket_rect)  # Draw small objects

    # Update the display
    pygame.display.flip()

    # Save frame to video if WRITE is True
    if WRITE:
        pygame.display.iconify()  # Minimize window during render
        pygame.image.save(screen, f"./pygame_frames/frame_{frame_count}.png")  # Save each frame as an image
        frame_count += 1

    frame_count += 1  # Increment frame count for the next iteration
    clock.tick(FPS)  # Control the frame rate


# ffmpeg -framerate 20 -i frame_%d.png -c:v libx264 -pix_fmt yuv420p output.mp4