#!/usr/bin/env python3
"""Colourful space-raid shooter."""
import random
import pygame

W, H = 800, 600


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Star Raid \u2014 ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 16)

    stars = [(random.randrange(W), random.randrange(H), random.randint(1, 3)) for _ in range(70)]
    px = W / 2
    shots = []
    foes = []
    score = 0
    lives = 3
    cooldown = 0
    tick = 0
    over = False

    def spawn():
        foes.append({
            "x": float(random.randint(30, W - 50)),
            "y": -24.0,
            "dx": random.choice([-1.6, -1.0, 1.0, 1.6]),
            "hp": 1,
            "kind": random.choice(["a", "b"]),
        })

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
                    px, shots, foes, score, lives, over = W / 2, [], [], 0, 3, False

        keys = pygame.key.get_pressed()
        if not over:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                px -= 7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                px += 7
            px = max(20, min(W - 20, px))
            cooldown = max(0, cooldown - 1)
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and cooldown == 0:
                shots.append([px, H - 70])
                cooldown = 10
            if tick % 40 == 0:
                spawn()

            for s in shots:
                s[1] -= 11
            shots = [s for s in shots if s[1] > -10]

            for f in foes:
                f["y"] += 2.2
                f["x"] += f["dx"]
                if f["x"] < 16 or f["x"] > W - 32:
                    f["dx"] *= -1
            kept = []
            for f in foes:
                frect = pygame.Rect(int(f["x"]), int(f["y"]), 28, 22)
                hit = False
                left = []
                for s in shots:
                    if frect.collidepoint(s[0], s[1]):
                        hit = True
                        score += 15
                    else:
                        left.append(s)
                shots = left
                if frect.colliderect(pygame.Rect(int(px) - 16, H - 56, 32, 28)):
                    lives -= 1
                    hit = True
                    if lives <= 0:
                        over = True
                if not hit and f["y"] < H + 20:
                    kept.append(f)
            foes = kept

        screen.fill((8, 10, 28))
        for i, (sx, sy, sz) in enumerate(stars):
            sy = (sy + sz) % H
            stars[i] = (sx, sy, sz)
            pygame.draw.circle(screen, (180, 200, 255), (sx, int(sy)), sz)

        pts = [(int(px), H - 58), (int(px) - 16, H - 28), (int(px) + 16, H - 28)]
        pygame.draw.polygon(screen, (80, 220, 255), pts)
        pygame.draw.polygon(screen, (255, 255, 255), pts, 2)
        pygame.draw.rect(screen, (255, 80, 60), (int(px) - 3, H - 24, 6, 10))

        for s in shots:
            pygame.draw.rect(screen, (255, 240, 80), (int(s[0]) - 2, int(s[1]), 4, 12))

        for f in foes:
            col = (255, 90, 90) if f["kind"] == "a" else (180, 90, 255)
            pygame.draw.rect(screen, col, (int(f["x"]), int(f["y"]), 28, 22), border_radius=4)
            pygame.draw.circle(screen, (20, 10, 20), (int(f["x"]) + 8, int(f["y"]) + 10), 3)
            pygame.draw.circle(screen, (20, 10, 20), (int(f["x"]) + 20, int(f["y"]) + 10), 3)

        screen.blit(font.render(f"SCORE {score}    LIVES {lives}", True, (255, 230, 90)), (16, 12))
        screen.blit(small.render("https://x.com/ElbowOS    arrows / A D   space fire   R restart", True, (160, 180, 220)), (16, H - 24))
        if over:
            screen.blit(font.render("SHIP DOWN \u2014 press R", True, (255, 80, 80)), (260, 280))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
