#!/usr/bin/env python3
"""Colourful 8x8 gem swap match-3."""
import random
import pygame

W, H = 720, 760
N = 8
CELL = 70
OX, OY = 80, 90
COLORS = [
    (230, 70, 80),
    (80, 180, 90),
    (70, 130, 230),
    (240, 200, 50),
    (190, 80, 210),
    (50, 210, 210),
]


def new_grid():
    return [[random.randrange(len(COLORS)) for _ in range(N)] for _ in range(N)]


def matches(g):
    kill = set()
    for y in range(N):
        run = 1
        for x in range(1, N):
            if g[y][x] == g[y][x - 1] and g[y][x] != -1:
                run += 1
            else:
                if run >= 3:
                    for k in range(run):
                        kill.add((x - 1 - k, y))
                run = 1
        if run >= 3:
            for k in range(run):
                kill.add((N - 1 - k, y))
    for x in range(N):
        run = 1
        for y in range(1, N):
            if g[y][x] == g[y - 1][x] and g[y][x] != -1:
                run += 1
            else:
                if run >= 3:
                    for k in range(run):
                        kill.add((x, y - 1 - k))
                run = 1
        if run >= 3:
            for k in range(run):
                kill.add((x, N - 1 - k))
    return kill


def collapse(g):
    for x in range(N):
        col = [g[y][x] for y in range(N) if g[y][x] != -1]
        missing = N - len(col)
        col = [random.randrange(len(COLORS)) for _ in range(missing)] + col
        for y in range(N):
            g[y][x] = col[y]


def resolve(g):
    total = 0
    while True:
        kill = matches(g)
        if not kill:
            return total
        total += len(kill) * 10
        for x, y in kill:
            g[y][x] = -1
        collapse(g)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Gem Grid \u2014 ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24, bold=True)
    small = pygame.font.SysFont("arial", 16)

    grid = new_grid()
    resolve(grid)
    sel = None
    score = 0
    moves = 24
    msg = "Swap adjacent gems"

    def cell_at(pos):
        mx, my = pos
        x = (mx - OX) // CELL
        y = (my - OY) // CELL
        if 0 <= x < N and 0 <= y < N:
            return x, y
        return None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_n:
                    grid = new_grid()
                    resolve(grid)
                    sel = None
                    score = 0
                    moves = 24
                    msg = "New board"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and moves > 0:
                c = cell_at(event.pos)
                if c is None:
                    sel = None
                elif sel is None:
                    sel = c
                else:
                    x1, y1 = sel
                    x2, y2 = c
                    if abs(x1 - x2) + abs(y1 - y2) == 1:
                        grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]
                        gained = resolve(grid)
                        if gained:
                            score += gained
                            moves -= 1
                            msg = f"+{gained}"
                        else:
                            grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]
                            msg = "No match"
                    sel = None

        screen.fill((18, 14, 32))
        pygame.draw.rect(screen, (36, 24, 58), (40, 20, 640, 720), border_radius=16)
        screen.blit(font.render("GEM GRID", True, (255, 210, 90)), (56, 32))
        screen.blit(small.render("https://x.com/ElbowOS", True, (180, 160, 220)), (480, 40))
        screen.blit(font.render(f"Score {score}    Moves {moves}", True, (240, 240, 255)), (56, 62))

        for y in range(N):
            for x in range(N):
                r = pygame.Rect(OX + x * CELL + 4, OY + y * CELL + 4, CELL - 8, CELL - 8)
                pygame.draw.rect(screen, COLORS[grid[y][x]], r, border_radius=14)
                pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=14)
                if sel == (x, y):
                    pygame.draw.rect(screen, (255, 255, 120), r.inflate(6, 6), 3, border_radius=16)

        if moves <= 0:
            screen.blit(font.render("Out of moves \u2014 N for new board", True, (255, 180, 80)), (80, 680))
        else:
            screen.blit(small.render(msg + "   \u00b7   N new", True, (200, 190, 230)), (80, 690))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
