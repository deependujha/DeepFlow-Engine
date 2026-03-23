# credits: https://github.com/deependujha

from abc import ABC, abstractmethod

import pygame
import sys
from typing import override

from deepflow.constants import (
    DEFAULT_FPS,
    DEFAULT_GAME_HEIGHT,
    DEFAULT_GAME_WIDTH,
    WHITE,
)


class DeepFlowBaseGame(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def exit(self) -> None:
        pass

    @abstractmethod
    def handle_events(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def loop(self) -> None:
        pass


class DeepFlowGame(DeepFlowBaseGame):
    def __init__(
        self,
        *,
        fps: int = DEFAULT_FPS,
        caption: str = "DeepFlow",
        display_surface_width: int = DEFAULT_GAME_WIDTH,
        display_surface_height: int = DEFAULT_GAME_HEIGHT,
        display_surface_fill_color: tuple[int, int, int] = WHITE,
    ) -> None:
        super().__init__()
        self._running = False
        self.fps = fps
        self.FramePerSec = pygame.time.Clock()
        self.caption = caption
        self.display_surface_width = display_surface_width
        self.display_surface_height = display_surface_height
        self.display_surface_fill_color = display_surface_fill_color
        self.dt = 0.0
        self._sprite_groups = {}
        self._added_sprites = set()

    def _verify_all_sprites_are_part_of_a_group(self) -> None:
        for attribute, value in vars(self).items():
            if (
                isinstance(value, pygame.sprite.Sprite)
                and value not in self._added_sprites
            ):
                raise ValueError(
                    f"Sprite '{attribute}' is not part of any sprite group. Please add it to a sprite group using 'add_to_sprite_group' method."
                )

    def add_to_sprite_group(
        self, group_name: str, sprite: pygame.sprite.Sprite
    ) -> None:
        if group_name not in self._sprite_groups:
            self._sprite_groups[group_name] = pygame.sprite.Group()
        self._sprite_groups[group_name].add(sprite)
        self._added_sprites.add(sprite)

    def get_sprite_group(self, group_name: str) -> pygame.sprite.Group:
        return self._sprite_groups.get(group_name, pygame.sprite.Group())

    @override
    def start(self) -> None:
        self._verify_all_sprites_are_part_of_a_group()
        pygame.init()
        self._running = True
        self.display_surface = pygame.display.set_mode(
            (self.display_surface_width, self.display_surface_height)
        )
        self.display_surface.fill(self.display_surface_fill_color)
        pygame.display.set_caption(self.caption)

    @override
    def loop(self) -> None:
        while self._running:
            self.handle_events()
            self.update()
            self.render()
            # self.dt = self.FramePerSec.tick(self.fps) / 1000.0
            self.FramePerSec.tick(self.fps)
            self.dt = 1.0 / self.fps

    @override
    def render(self) -> None:
        pygame.display.update()

    @override
    def exit(self) -> None:
        # kill all sprites in the groups
        for group in self._sprite_groups.values():
            for sprite in group:
                sprite.kill()
        pygame.quit()
        sys.exit()
