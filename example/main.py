import deepflow_engine as dfe
from deepflow_engine.constants import DEFAULT_GAME_HEIGHT, DEFAULT_GAME_WIDTH
import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 50, 80)  # Placeholder rect
        self.rect.center = (random.randint(40, DEFAULT_GAME_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > DEFAULT_GAME_HEIGHT:
            self.rect.top = -50
            self.rect.center = (random.randint(40, DEFAULT_GAME_WIDTH - 40), 0)
            return 1  # increase score when enemy goes off screen
        return 0


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
        if self.rect.right > DEFAULT_GAME_WIDTH:
            self.rect.right = DEFAULT_GAME_WIDTH


class MyGame(dfe.DeepFlowGame):
    def __init__(self):
        super().__init__()
        self.speed = 7
        self.score = 0
        self.width = DEFAULT_GAME_WIDTH
        self.height = DEFAULT_GAME_HEIGHT

    def start(self):
        self.font_small = pygame.font.SysFont("Verdana", 20)
        self._initialize_game()

    def get_audio_map(self):
        return {
            "collision_sound": "game-over.mp3",
        }

    def _initialize_game(self):
        # create sprites, load assets, etc.
        # Initialize Sprites
        self.p1 = Player()
        self.e1 = Enemy()
        self.enemies = pygame.sprite.Group()
        self.enemies.add(self.e1)

    def kill_all_sprites(self):
        self.p1.kill()
        for enemy in self.enemies:
            enemy.kill()

    def handle_events(self) -> None:
        pass

    def update_state(self) -> None:
        _score = self.e1.move(self.speed)
        self.score += _score
        # Increase speed slightly every second
        if self._engine.curr_frame % 60 == 0:
            self.speed += 0.5

    def player_action(self) -> None:
        self.p1.auto_move(self.e1.rect)

    def collision_check(self) -> None:
        if pygame.sprite.collide_rect(self.p1, self.e1):
            self.play_audio("collision_sound")  # Example audio event
            # NEW: Create a "Freeze Frame" effect
            # # Repeat the current frame 10 times in the folder to "stall" the video
            # for i in range(10):
            #     # This effectively pauses the video for 1/6th of a second
            #     pygame.image.save(DISPLAYSURF, f"frames/frame_{frame:04d}_pause_{i}.png")
            # Reset positions for the "Fail/Win" loop logic if desired
            self.e1.rect.top = -100
            self.e1.rect.center = (random.randint(40, DEFAULT_GAME_WIDTH - 40), 0)

    def render(self, canvas) -> None:
        # DRAWING
        canvas.fill((255, 255, 255))  # White BG
        # canvas.blit(background, (0, 0))

        # Draw Player (Blue) and Enemy (Red)
        pygame.draw.rect(canvas, (0, 0, 255), self.p1.rect)
        pygame.draw.rect(canvas, (255, 0, 0), self.e1.rect)
        # Draw Score
        scores = self.font_small.render(f"Score: {self.score}", True, (0, 0, 0))
        canvas.blit(scores, (10, 10))

    def play(self) -> None:
        try:
            self._play()
        except Exception as e:
            print(f"Error during game play: {e}")
        finally:
            self.exit()

    def update(self):
        self.update_state()
        self.player_action()
        self.collision_check()


def main():
    game = MyGame()
    engine = dfe.DeepFlowEngine(
        game, interactive=False, frames_dir="frames", video_length_seconds=15
    )
    out = dfe.run_pipeline(engine=engine, publish=False)
    print(f"Pipeline output: {out}")


if __name__ == "__main__":
    main()
