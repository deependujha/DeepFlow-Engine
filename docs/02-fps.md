# FPS (Frames Per Second) in PyGame

- FPS (Frames Per Second) is `the number of times your game loop updates and renders per second`.
- It controls how **smooth** and **consistent** your game feels.
- In Pygame, FPS is managed using a **Clock object**, which helps regulate the speed of the game loop.

```python
# Setting up FPS
FPS = 60
clock = pygame.time.Clock()
```

______________________________________________________________________

## Controlling FPS with `tick()`

- The `tick()` method is used to **limit the maximum FPS** of your game.
- It ensures your loop does not run faster than the specified FPS.
- It also returns the **time elapsed since the last frame (in milliseconds)**.

```python
# Inside the main game loop
while True:
    ...
    pygame.display.flip()
    clock.tick(FPS)
```

- If your game loop runs too fast → `tick()` pauses execution.
- If your game is slow → it won’t magically fix it (FPS will drop).

______________________________________________________________________

## Getting Delta Time (Frame Time)

- `tick()` returns time in **milliseconds**, which is useful for frame-independent movement.
- Convert it to seconds by dividing by 1000.

```python
dt = clock.tick(FPS) / 1000  # seconds
```

- `dt` represents: **"how much real time passed since last frame"**

______________________________________________________________________

## Frame-Dependent vs Frame-Independent Movement

### ❌ Frame-dependent (bad)

```python
player_x += 5
```

- Movement speed depends on FPS
- Faster machine → faster gameplay

______________________________________________________________________

### ✅ Frame-independent (correct)

```python
player_x += speed * dt
```

- `speed` = pixels per second
- Works consistently across all devices

______________________________________________________________________

## Monitoring Actual FPS

- You can check real FPS using:

```python
current_fps = clock.get_fps()
print(current_fps)
```

- Useful for debugging performance issues.

______________________________________________________________________

## Key Takeaways

- FPS controls **game smoothness**
- `clock.tick(FPS)` → caps FPS + stabilizes loop
- `dt` → makes movement **time-based, not frame-based**
- Always use a Clock in your game loop

______________________________________________________________________

## Mental Model

```text
Game Loop:
handle events → update (using dt) → render → display → tick(FPS)
```

- `tick()` is the **pace controller**
- `dt` is the **time translator**

______________________________________________________________________

If you keep just one thing from this:
👉 Always multiply movement by `dt` — otherwise your game will behave differently on every machine.
