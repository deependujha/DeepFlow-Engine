import argparse

import deepflow_engine as dfe
from deepflow_engine.constants import DEFAULT_GAME_HEIGHT, DEFAULT_GAME_WIDTH

import pygame
import random


# -------------------------------
# Enemy
# -------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 80)

        self.rect.center = (
            random.randint(40, DEFAULT_GAME_WIDTH - 40),
            0,
        )

        # float position (important)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def move(self, speed: float, dt: float) -> int:
        self.y += speed * dt
        self.rect.y = int(self.y)

        if self.rect.top > DEFAULT_GAME_HEIGHT:
            self.rect.top = -50
            self.rect.center = (
                random.randint(40, DEFAULT_GAME_WIDTH - 40),
                0,
            )

            self.x = float(self.rect.x)
            self.y = float(self.rect.y)

            return 1

        return 0


# -------------------------------
# Player
# -------------------------------
class Player(pygame.sprite.Sprite):
    GAME_WIDTH = DEFAULT_GAME_WIDTH
    TIME_TO_CROSS_SCREEN = (
        2  # should be able to cross the screen in 2 seconds at max speed
    )

    @property
    def MOVE_SPEED(self):
        return self.GAME_WIDTH / self.TIME_TO_CROSS_SCREEN

    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 80)
        self.rect.center = (160, 520)

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.last_move_direction = 1  # 1 for right, -1 for left

    def move(self, enemy_rect, dt: float, key_pressed=None):
        if key_pressed is not None:
            self.last_move_direction = 0
            if key_pressed[pygame.K_LEFT]:
                self.last_move_direction -= 1
            if key_pressed[pygame.K_RIGHT]:
                self.last_move_direction += 1
        else:
            # simple AI
            # move to left first, then right and repeat
            if self.rect.x < 10:
                self.last_move_direction = 1
            elif self.rect.x > DEFAULT_GAME_WIDTH - self.rect.width - 10:
                self.last_move_direction = -1

        self.x += self.last_move_direction * self.MOVE_SPEED * dt

        # clamp
        self.x = max(0, min(self.x, DEFAULT_GAME_WIDTH - self.rect.width))

        self.rect.x = int(self.x)
        self.TIME_TO_CROSS_SCREEN = max(
            0.5, self.TIME_TO_CROSS_SCREEN - dt * 0.01
        )  # gradually increase speed


# -------------------------------
# Game
# -------------------------------
class MyGame(dfe.DeepFlowGame):
    ACCELERATION = 50  # speed increase per second

    def __init__(self):
        super().__init__()
        self.speed = 200  # px/sec
        self.score = 0

    def start(self):
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self._initialize_game()

    def get_audio_map(self):
        return {
            "collision": "game-over.mp3",
        }

    def _initialize_game(self):
        self.p1 = Player()
        self.e1 = Enemy()

        self.enemies = pygame.sprite.Group(self.e1)

    def kill_all_sprites(self):
        self.p1.kill()
        for enemy in self.enemies:
            enemy.kill()

    # -------------------------------
    # Input abstraction
    # -------------------------------
    def get_input(self):
        if self._engine and self._engine.interactive:
            return pygame.key.get_pressed()
        return None

    # -------------------------------
    # Update
    # -------------------------------
    def update(self):
        dt = self.dt

        # enemy movement
        self.score += self.e1.move(self.speed, dt)

        # player movement
        self.p1.move(self.e1.rect, dt, self.get_input())

        # collision
        if pygame.sprite.collide_rect(self.p1, self.e1):
            self.play_audio("collision")

            # reset enemy
            self.e1.rect.top = -100
            self.e1.rect.center = (
                random.randint(40, DEFAULT_GAME_WIDTH - 40),
                0,
            )

            self.e1.x = float(self.e1.rect.x)
            self.e1.y = float(self.e1.rect.y)

        # gradual difficulty increase
        self.speed += self.ACCELERATION * dt

    # -------------------------------
    # Render
    # -------------------------------
    def render(self, canvas) -> None:
        canvas.fill((255, 255, 255))

        pygame.draw.rect(canvas, (0, 0, 255), self.p1.rect)
        pygame.draw.rect(canvas, (255, 0, 0), self.e1.rect)

        score_surface = self.font_small.render(f"Score: {self.score}", True, (0, 0, 0))
        canvas.blit(score_surface, (10, 10))


# -------------------------------
# Main
# -------------------------------
def parse_args():
    parser = argparse.ArgumentParser(description="Run DeepFlow Engine example game.")
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (generate video instead of interactive session)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.headless:
        print("Running in headless mode (video generation)")
    else:
        print("Running in interactive mode")

    game = MyGame()

    if args.headless:
        engine = dfe.DeepFlowEngine(
            game,
            interactive=False,
            frames_dir="frames",
            video_length_seconds=15,
        )
    else:
        # when in interactive mode, we can still save frames, if `frames_dir` is set.
        # This can be useful for debugging or generating videos of interactive sessions.
        engine = dfe.DeepFlowEngine(
            game,
            interactive=True,
            frames_dir="frames",
            fps=30,
        )

    out = dfe.run_pipeline(engine=engine, publish=False)
    print(f"Pipeline output: {out}")


if __name__ == "__main__":
    main()
