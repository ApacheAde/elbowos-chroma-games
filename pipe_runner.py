#!/usr/bin/env python3
"""Original colourful platformer. Mario-like genre, original plumber mascot."""
import pygame

W, H = 960, 540
GRAV = 0.55
JUMP = -12.2


def draw_plumber(surf, x, y, facing, t):
    body = pygame.Rect(int(x), int(y), 28, 36)
    pygame.draw.rect(surf, (40, 110, 210), body)
    pygame.draw.rect(surf, (220, 50, 50), (body.x, body.y, 28, 12))
    pygame.draw.circle(surf, (255, 210, 160), (body.centerx, body.y - 8), 10)
    brim = 8 if facing >= 0 else -8
    pygame.draw.rect(surf, (220, 40, 40), (body.centerx - 12, body.y - 20, 24, 6))
    pygame.draw.circle(surf, (20, 20, 20), (body.centerx + brim // 2, body.y - 10), 2)
    foot = 2 if (t // 6) % 2 == 0 else -2
    pygame.draw.rect(surf, (90, 50, 20), (body.x + 2, body.bottom - 2, 10, 6 + foot))
    pygame.draw.rect(surf, (90, 50, 20), (body.x + 16, body.bottom - 2, 10, 6 - foot))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Pipe Runner \u2014 ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 16)

    platforms = [
        pygame.Rect(0, 500, 2800, 50),
        pygame.Rect(220, 410, 140, 18),
        pygame.Rect(430, 340, 160, 18),
        pygame.Rect(700, 400, 120, 18),
        pygame.Rect(880, 310, 180, 18),
        pygame.Rect(1180, 420, 150, 18),
        pygame.Rect(1400, 330, 200, 18),
        pygame.Rect(1700, 260, 140, 18),
        pygame.Rect(1960, 380, 220, 18),
        pygame.Rect(2300, 300, 180, 18),
    ]
    pipes = [pygame.Rect(360, 430, 48, 70), pygame.Rect(1080, 430, 48, 70), pygame.Rect(1880, 430, 54, 70)]
    coins = [pygame.Rect(x, y, 16, 16) for x, y in (
        (250, 370), (470, 300), (740, 360), (940, 270), (1220, 380),
        (1460, 290), (1750, 220), (2020, 340), (2360, 260), (2500, 450),
    )]
    foes = [{"x": 620.0, "y": 478.0, "dx": 1.6, "lo": 560, "hi": 820},
            {"x": 1500.0, "y": 308.0, "dx": 1.4, "lo": 1400, "hi": 1580},
            {"x": 2100.0, "y": 478.0, "dx": 2.0, "lo": 2000, "hi": 2280}]
    flag = pygame.Rect(2620, 360, 14, 140)

    def reset():
        return 60.0, 400.0, 0.0, 0.0, 1, 0, False, list(coins), True

    px, py, vx, vy, facing, score, dead, remaining, running = reset()
    cam = 0.0
    tick = 0
    won = False

    while True:
        tick += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_r:
                    px, py, vx, vy, facing, score, dead, remaining, running = reset()
                    won = False
                    cam = 0.0

        keys = pygame.key.get_pressed()
        if running and not dead and not won:
            ax = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                ax -= 0.7
                facing = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                ax += 0.7
                facing = 1
            vx += ax
            vx *= 0.82
            on_ground = False
            vy += GRAV
            px += vx
            prect = pygame.Rect(int(px), int(py), 28, 36)
            for p in platforms + pipes:
                if prect.colliderect(p):
                    if vx > 0:
                        px = p.left - 28
                    elif vx < 0:
                        px = p.right
                    vx = 0
                    prect.x = int(px)
            py += vy
            prect = pygame.Rect(int(px), int(py), 28, 36)
            for p in platforms + pipes:
                if prect.colliderect(p):
                    if vy > 0:
                        py = p.top - 36
                        vy = 0
                        on_ground = True
                    elif vy < 0:
                        py = p.bottom
                        vy = 0
                    prect.y = int(py)
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
                vy = JUMP
            if py > H + 80:
                dead = True

            prect = pygame.Rect(int(px), int(py), 28, 36)
            kept = []
            for c in remaining:
                if prect.colliderect(c):
                    score += 10
                else:
                    kept.append(c)
            remaining = kept

            for f in foes:
                f["x"] += f["dx"]
                if f["x"] < f["lo"] or f["x"] > f["hi"]:
                    f["dx"] *= -1
                frect = pygame.Rect(int(f["x"]), int(f["y"]), 28, 22)
                if prect.colliderect(frect):
                    if vy > 1 and prect.bottom - frect.top < 18:
                        f["y"] = 9999
                        vy = -8
                        score += 50
                    else:
                        dead = True
            if prect.colliderect(flag):
                won = True
                score += 200

        cam += (px - 280 - cam) * 0.12
        cam = max(0, min(cam, 2800 - W))

        for y in range(H):
            t = y / H
            col = (int(90 + 80 * t), int(170 + 40 * t), int(255 - 40 * t))
            pygame.draw.line(screen, col, (0, y), (W, y))
        pygame.draw.ellipse(screen, (50, 170, 70), (-40 - cam * 0.2, 360, 420, 220))
        pygame.draw.ellipse(screen, (40, 150, 60), (300 - cam * 0.25, 380, 500, 240))
        pygame.draw.ellipse(screen, (60, 180, 80), (700 - cam * 0.2, 350, 460, 250))

        def wx(x):
            return int(x - cam)

        for p in platforms:
            pygame.draw.rect(screen, (90, 200, 70), (wx(p.x), p.y, p.w, p.h))
            pygame.draw.rect(screen, (140, 90, 40), (wx(p.x), p.y + 14, p.w, p.h - 14))
        for pipe in pipes:
            pygame.draw.rect(screen, (30, 180, 70), (wx(pipe.x), pipe.y, pipe.w, pipe.h))
            pygame.draw.rect(screen, (20, 140, 50), (wx(pipe.x) - 6, pipe.y - 10, pipe.w + 12, 18))
        for c in remaining:
            pygame.draw.circle(screen, (255, 210, 40), (wx(c.x + 8), c.y + 8), 9)
            pygame.draw.circle(screen, (255, 255, 160), (wx(c.x + 5), c.y + 5), 3)
        for f in foes:
            if f["y"] < 900:
                pygame.draw.ellipse(screen, (170, 90, 40), (wx(f["x"]), int(f["y"]), 28, 22))
                pygame.draw.circle(screen, (20, 20, 20), (wx(f["x"]) + 8, int(f["y"]) + 8), 3)
                pygame.draw.circle(screen, (20, 20, 20), (wx(f["x"]) + 18, int(f["y"]) + 8), 3)
        pygame.draw.rect(screen, (230, 230, 240), (wx(flag.x), flag.y, 8, flag.h))
        pygame.draw.polygon(screen, (240, 50, 50), [
            (wx(flag.x) + 8, flag.y),
            (wx(flag.x) + 70, flag.y + 18),
            (wx(flag.x) + 8, flag.y + 36),
        ])

        if not dead:
            draw_plumber(screen, px - cam, py, facing, tick)
        else:
            screen.blit(font.render("OUCH \u2014 press R", True, (255, 40, 40)), (360, 220))
        if won:
            screen.blit(font.render("GOAL!  +200   press R", True, (255, 255, 80)), (330, 200))

        hud = font.render(f"COINS {score}", True, (20, 20, 40))
        screen.blit(hud, (16, 12))
        screen.blit(small.render("original plumber \u00b7 not an emulator \u00b7 ElbowOS", True, (20, 40, 30)), (16, H - 24))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
