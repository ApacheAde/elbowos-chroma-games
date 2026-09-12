#!/usr/bin/env python3
"""Colourful 3-reel crystal slots."""
import random
import pygame

W, H = 820, 560
SYMBOLS = [
    ("\u25c6", (80, 200, 255), 8),
    ("\u2605", (255, 210, 40), 12),
    ("\u25cf", (255, 80, 90), 4),
    ("\u25b2", (120, 230, 90), 6),
    ("\u2726", (220, 120, 255), 15),
    ("\u25a0", (255, 160, 40), 3),
]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Crystal Slots \u2014 ElbowOS")
    clock = pygame.time.Clock()
    title = pygame.font.SysFont("arial", 36, bold=True)
    big = pygame.font.SysFont("arial", 72, bold=True)
    body = pygame.font.SysFont("arial", 22, bold=True)

    bank = 100
    bet = 5
    reels = [0, 1, 2]
    spinning = 0
    msg = "Space to spin"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_SPACE and spinning == 0:
                    if bank < bet:
                        bank = 100
                        msg = "Bank topped up"
                    else:
                        bank -= bet
                        spinning = 24
                        msg = "Good luck\u2026"
                if event.key == pygame.K_n:
                    bank = 100
                    msg = "Reset"

        if spinning:
            spinning -= 1
            reels = [random.randrange(len(SYMBOLS)) for _ in range(3)]
            if spinning == 0:
                a, b, c = reels
                if a == b == c:
                    pay = bet * SYMBOLS[a][2]
                    bank += pay
                    msg = f"JACKPOT  +${pay}"
                elif a == b or b == c or a == c:
                    pay = bet * 2
                    bank += pay
                    msg = f"Pair  +${pay}"
                else:
                    msg = "No line"

        for y in range(H):
            t = y / H
            pygame.draw.line(screen, (int(30 + 40 * t), 8, int(50 + 20 * t)), (0, y), (W, y))
        pygame.draw.rect(screen, (40, 20, 70), (50, 40, 720, 480), border_radius=20)
        pygame.draw.rect(screen, (240, 200, 70), (50, 40, 720, 480), 4, border_radius=20)
        screen.blit(title.render("CRYSTAL SLOTS", True, (255, 220, 80)), (220, 58))
        screen.blit(body.render("https://x.com/ElbowOS", True, (200, 180, 230)), (300, 102))

        for i, idx in enumerate(reels):
            glyph, color, _p = SYMBOLS[idx]
            box = pygame.Rect(110 + i * 210, 160, 180, 200)
            pygame.draw.rect(screen, (18, 10, 28), box, border_radius=14)
            pygame.draw.rect(screen, color, box, 5, border_radius=14)
            screen.blit(big.render(glyph, True, color), (box.x + 50, box.y + 50))

        screen.blit(body.render(f"Bank  ${bank}     Bet  ${bet}", True, (255, 255, 255)), (110, 390))
        screen.blit(body.render(msg, True, (255, 230, 140)), (110, 430))
        screen.blit(body.render("SPACE spin    N reset bank    ESC quit", True, (180, 160, 210)), (110, 470))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
