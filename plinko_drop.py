#!/usr/bin/env python3
"""Colourful Plinko / pachinko chip drop."""
import random
import pygame

W, H = 720, 640
COLS = 9
ROWS = 8
GAP = 62
OX, OY = 86, 80


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Plinko Drop \u2014 ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 16)

    pins = []
    for r in range(ROWS):
        n = COLS if r % 2 == 0 else COLS - 1
        offset = 0 if r % 2 == 0 else GAP // 2
        for c in range(n):
            pins.append((OX + offset + c * GAP, OY + 40 + r * 48))

    slots = [1, 3, 5, 8, 12, 8, 5, 3, 1]
    bank = 80
    bet = 4
    ball = None
    msg = "Click or Space to drop a chip"

    def spawn():
        nonlocal bank, ball, msg
        if bank < bet:
            bank = 80
            msg = "Bank topped up"
            return
        bank -= bet
        ball = {"x": float(W // 2 + random.randint(-20, 20)), "y": 50.0, "vx": random.uniform(-1.2, 1.2), "vy": 0.0}

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_SPACE and ball is None:
                    spawn()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ball is None:
                spawn()

        if ball:
            ball["vy"] += 0.28
            ball["x"] += ball["vx"]
            ball["y"] += ball["vy"]
            if ball["x"] < 40:
                ball["x"] = 40
                ball["vx"] *= -0.6
            if ball["x"] > W - 40:
                ball["x"] = W - 40
                ball["vx"] *= -0.6
            for px, py in pins:
                dx, dy = ball["x"] - px, ball["y"] - py
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < 16 and dist > 0:
                    nx, ny = dx / dist, dy / dist
                    ball["x"] = px + nx * 16
                    ball["y"] = py + ny * 16
                    ball["vx"] += nx * 1.6 + random.uniform(-0.4, 0.4)
                    ball["vy"] = abs(ball["vy"]) * 0.25 + ny * 0.4
            if ball["y"] > OY + 40 + ROWS * 48 + 10:
                idx = int((ball["x"] - (OX - GAP // 2)) / GAP)
                idx = max(0, min(COLS - 1, idx))
                win = bet * slots[idx]
                bank += win
                msg = f"Landed slot x{slots[idx]}  +${win}"
                ball = None

        screen.fill((16, 24, 48))
        pygame.draw.rect(screen, (28, 40, 80), (24, 16, W - 48, H - 32), border_radius=16)
        screen.blit(font.render("PLINKO DROP", True, (255, 210, 80)), (40, 24))
        screen.blit(small.render("https://x.com/ElbowOS", True, (160, 190, 230)), (520, 30))
        screen.blit(font.render(f"Bank ${bank}", True, (255, 255, 255)), (40, 54))

        for px, py in pins:
            pygame.draw.circle(screen, (180, 210, 255), (px, py), 7)
            pygame.draw.circle(screen, (80, 120, 200), (px, py), 7, 2)

        base_y = OY + 40 + ROWS * 48 + 28
        for i, mult in enumerate(slots):
            x = OX - GAP // 2 + i * GAP
            color = (40, 160, 90) if mult >= 8 else (50, 90, 160) if mult >= 5 else (80, 70, 140)
            pygame.draw.rect(screen, color, (x + 4, base_y, GAP - 8, 46), border_radius=6)
            screen.blit(small.render(f"x{mult}", True, (255, 255, 255)), (x + 18, base_y + 14))

        if ball:
            pygame.draw.circle(screen, (255, 80, 120), (int(ball["x"]), int(ball["y"])), 10)
            pygame.draw.circle(screen, (255, 200, 220), (int(ball["x"]) - 3, int(ball["y"]) - 3), 3)

        screen.blit(small.render(msg + "   \u00b7   click / space", True, (220, 220, 240)), (40, H - 36))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
