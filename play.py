#!/usr/bin/env python3
"""Colourful launcher for the ElbowOS chroma game pack."""
import os
import subprocess
import sys

import pygame

ROOT = os.path.dirname(os.path.abspath(__file__))

GAMES = [
    ("Pipe Runner", "pipe_runner.py", (70, 190, 80), "Platformer"),
    ("Suit War", "suit_war.py", (220, 60, 70), "Cards"),
    ("Neon Hold'em", "neon_holdem.py", (40, 140, 90), "Casino cards"),
    ("Crystal Slots", "crystal_slots.py", (230, 180, 40), "Casino"),
    ("Plinko Drop", "plinko_drop.py", (80, 160, 230), "Casino"),
    ("Gem Grid", "gem_grid.py", (180, 70, 200), "Puzzle"),
    ("Star Raid", "star_raid.py", (50, 80, 180), "Shooter"),
]


def run_game(filename: str) -> None:
    path = os.path.join(ROOT, filename)
    subprocess.call([sys.executable, path])


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((820, 560))
    pygame.display.set_caption("ElbowOS Chroma Games")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 40, bold=True)
    body = pygame.font.SysFont("arial", 22)
    small = pygame.font.SysFont("arial", 16)
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    return
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(GAMES)
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(GAMES)
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    pygame.quit()
                    run_game(GAMES[selected][1])
                    pygame.init()
                    screen = pygame.display.set_mode((820, 560))
                    pygame.display.set_caption("ElbowOS Chroma Games")
                    title = pygame.font.SysFont("arial", 40, bold=True)
                    body = pygame.font.SysFont("arial", 22)
                    small = pygame.font.SysFont("arial", 16)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for i, _g in enumerate(GAMES):
                    rect = pygame.Rect(60, 120 + i * 52, 700, 46)
                    if rect.collidepoint(mx, my):
                        pygame.quit()
                        run_game(GAMES[i][1])
                        pygame.init()
                        screen = pygame.display.set_mode((820, 560))
                        pygame.display.set_caption("ElbowOS Chroma Games")
                        title = pygame.font.SysFont("arial", 40, bold=True)
                        body = pygame.font.SysFont("arial", 22)
                        small = pygame.font.SysFont("arial", 16)

        for y in range(560):
            t = y / 560
            screen.fill(
                (
                    int(18 + 30 * t),
                    int(10 + 20 * t),
                    int(40 + 50 * t),
                ),
                rect=pygame.Rect(0, y, 820, 1),
            )

        screen.blit(title.render("ELBOWOS CHROMA GAMES", True, (255, 230, 90)), (70, 28))
        screen.blit(
            small.render("https://x.com/ElbowOS   ·   arrows + enter   ·   click a row", True, (200, 200, 220)),
            (70, 78),
        )

        for i, (name, _fn, color, kind) in enumerate(GAMES):
            rect = pygame.Rect(60, 120 + i * 52, 700, 46)
            bg = tuple(min(255, c + 40) for c in color) if i == selected else color
            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
            screen.blit(body.render(f"{i + 1}.  {name}", True, (20, 20, 20)), (80, 128 + i * 52))
            screen.blit(small.render(kind, True, (30, 30, 40)), (620, 134 + i * 52))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
