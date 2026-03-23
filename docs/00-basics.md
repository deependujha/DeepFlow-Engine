# PyGame Basics

## 🧠 What a Pygame program really is

- A Pygame game is just:

```text
setup → infinite loop → exit
```

- Inside the loop:

```text
handle events → update game states → render → display → control FPS
```

______________________________________________________________________

## 🔹 Initialization

```python
pygame.init()
```

- Initializes all modules (display, sound, input, etc.)
- Must be called before anything else

______________________________________________________________________

## 🔹 Creating a Window

```python
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")
```

- Creates the main window (your canvas)
- Caption = window title

______________________________________________________________________

## 🔹 Colors

```python
WHITE = (255, 255, 255)
```

- RGB tuples (0–255)
- Used for fills, text, shapes

______________________________________________________________________

## 🔹 Images (Background & Sprites)

```python
background = pygame.image.load("bg.png")
screen.blit(background, (0, 0))
```

- `load()` → loads image as a **Surface**
- `blit()` → draws it onto another surface

👉 Everything in pygame is basically:

```text
Surface → drawn onto another Surface
```

______________________________________________________________________

## 🔹 Game Loop (core structure)

```python
while True:
    for event in pygame.event.get():
        ...

    # update game state
    ...

    # render
    screen.blit(...)

    pygame.display.update()
    clock.tick(FPS)
```

- Runs forever until you quit
- Order matters (don’t mix update/render randomly)

______________________________________________________________________

## 🔹 Sprites (very important concept)

- A **Sprite** = object with:

  - image (visual)
  - rect (position + collision box)
  - behavior (methods like `move()`)

```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ...
        self.rect = ...
```

👉 Think:

```text
Sprite = image + position + logic
```

______________________________________________________________________

## 🔹 `rect` (this is everything)

```python
self.rect = self.image.get_rect()
self.rect.center = (x, y)
```

- Handles:

  - position
  - collision
  - movement

______________________________________________________________________

## 🔹 Movement

```python
self.rect.move_ip(dx, dy)
```

- `move_ip` = move **in place**
- Changes position directly

______________________________________________________________________

## 🔹 Input Handling

```python
pressed_keys = pygame.key.get_pressed()
if pressed_keys[K_LEFT]:
    ...
```

- Continuous input (held keys)

______________________________________________________________________

## 🔹 Sprite Groups

- rather than trying to manage individual sprites, we can use groups:

```python
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
```

- Collections of sprites

- Useful for:

  - updates
  - rendering
  - collision

______________________________________________________________________

## 🔹 Collision Detection

```python
pygame.sprite.spritecollideany(player, enemies)
```

- Checks overlap using `rect`
- Returns collided sprite or `None`

______________________________________________________________________

## 🔹 Killing Sprites

```python
entity.kill()
```

- Removes sprite from **all groups**
- Effectively deletes it from game logic

👉 Important:

```text
kill() ≠ delete object
kill() = remove from game systems
```

______________________________________________________________________

## 🔹 Fonts / Text

```python
my_text = font.render("Text", True, color)
DISPLAYSURF.blit(my_text, (10, 10))
```

- Returns a surface
- Needs `blit()` to display at specific position

______________________________________________________________________

## 🔹 FPS Control

```python
clock.tick(FPS)
```

- Limits loop speed
- Returns delta time (ms)

______________________________________________________________________

# ✅ Cleaned “Oops-Proof” Version (what you should aim for)

This is your same game — but structured correctly 👇

```python
import pygame
import sys
import random

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
FPS = 60

# Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Assets
background = pygame.image.load("AnimatedStreet.png").convert()
player_img = pygame.image.load("Player.png").convert_alpha()
enemy_img = pygame.image.load("Enemy.png").convert_alpha()

font_small = pygame.font.SysFont("Verdana", 20)

SPEED = 200  # pixels/sec
SCORE = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(160, 520))

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 300 * dt
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 300 * dt


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(
            center=(random.randint(40, SCREEN_WIDTH - 40), 0)
        )

    def update(self, dt):
        global SCORE
        self.rect.y += SPEED * dt

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.centerx = random.randint(40, SCREEN_WIDTH - 40)


# Sprites
player = Player()
enemy = Enemy()

all_sprites = pygame.sprite.Group(player, enemy)
enemies = pygame.sprite.Group(enemy)

# Game loop
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update(dt)

    # Collision
    if pygame.sprite.spritecollideany(player, enemies):
        running = False

    # Render
    screen.blit(background, (0, 0))

    score_text = font_small.render(str(SCORE), True, BLACK)
    screen.blit(score_text, (10, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    pygame.display.update()

pygame.quit()
sys.exit()
```
