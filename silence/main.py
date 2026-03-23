import pygame
import json
import random
import os

# Initializing Headless Mode (No window will pop up)
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

# Setup constants
FPS = 60
TOTAL_SECONDS = 10
TOTAL_FRAMES = FPS * TOTAL_SECONDS
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED = 7
SCORE = 0

# Create frames directory
if not os.path.exists("frames"):
    os.makedirs("frames")

# Setup Surface
DISPLAYSURF = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
font_small = pygame.font.SysFont("Verdana", 20)

# Load Assets (Ensure these files exist in your folder)
# background = pygame.image.load("AnimatedStreet.png")
# player_img = pygame.image.load("Player.png")
# enemy_img = pygame.image.load("Enemy.png")


def write_log(log_data, filename="collisions_log.json"):
    json_data = json.dumps(log_data, indent=4)
    with open(filename, "w") as f:
        f.write(json_data)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 80)  # Placeholder rect
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = -50
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 80)  # Placeholder rect
        self.rect.center = (160, 520)

    def auto_move(self, enemy_rect):
        # BASIC AI: Move away from the enemy's X position
        if self.rect.centerx < enemy_rect.centerx:
            self.rect.move_ip(-5, 0)
        elif self.rect.centerx > enemy_rect.centerx:
            self.rect.move_ip(5, 0)

        # Keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


# Initialize Sprites
P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)

# LOGGING FOR SOUND
collision_log = []

print(f"DeepFlow: Starting generation of {TOTAL_FRAMES} frames...")

for frame in range(TOTAL_FRAMES):
    # Update logic
    E1.move()
    P1.auto_move(E1.rect)

    # Increase speed slightly every second
    if frame % 60 == 0:
        SPEED += 0.5

    # Check for collision
    if pygame.sprite.collide_rect(P1, E1):
        collision_log.append({"frame": frame, "time": frame / FPS, "type": "crash"})
        # NEW: Create a "Freeze Frame" effect
        # Repeat the current frame 10 times in the folder to "stall" the video
        for i in range(10):
            # This effectively pauses the video for 1/6th of a second
            pygame.image.save(DISPLAYSURF, f"frames/frame_{frame:04d}_pause_{i}.png")
        # Reset positions for the "Fail/Win" loop logic if desired
        E1.rect.top = -100
        E1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    # DRAWING
    DISPLAYSURF.fill((255, 255, 255))  # White BG
    # DISPLAYSURF.blit(background, (0, 0))

    # Draw Player (Blue) and Enemy (Red)
    pygame.draw.rect(DISPLAYSURF, (0, 0, 255), P1.rect)
    pygame.draw.rect(DISPLAYSURF, (255, 0, 0), E1.rect)

    # Draw Score
    scores = font_small.render(f"Score: {SCORE}", True, (0, 0, 0))
    DISPLAYSURF.blit(scores, (10, 10))

    # SAVE FRAME
    file_name = f"frames/frame_{frame:04d}.png"
    pygame.image.save(DISPLAYSURF, file_name)

    if frame % 60 == 0:
        print(f"Progress: {int(frame / TOTAL_FRAMES * 100)}%")

print("Generation Complete!")
print(f"Collisions logged at: {collision_log}")
write_log(collision_log)
