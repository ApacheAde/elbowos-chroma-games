#!/usr/bin/env python3
"""Colourful 5-card draw vs the house."""
import random
import pygame

W, H = 960, 580
SUITS = [("\u2665", (230, 40, 70)), ("\u2666", (230, 120, 30)), ("\u2663", (30, 150, 80)), ("\u2660", (25, 25, 40))]
RANKS = "23456789TJQKA"


def make_deck():
    d = [(r, s) for r in range(13) for s in range(4)]
    random.shuffle(d)
    return d


def hand_score(hand):
    ranks = sorted((c[0] for c in hand), reverse=True)
    suits = [c[1] for c in hand]
    counts = {r: ranks.count(r) for r in set(ranks)}
    flush = len(set(suits)) == 1
    uniq = sorted(set(ranks))
    straight = len(uniq) == 5 and uniq[-1] - uniq[0] == 4
    if uniq == [0, 1, 2, 3, 12]:
        straight = True
    vals = sorted(counts.values(), reverse=True)
    if straight and flush:
        return (8, ranks)
    if vals[0] == 4:
        return (7, ranks)
    if vals == [3, 2]:
        return (6, ranks)
    if flush:
        return (5, ranks)
    if straight:
        return (4, ranks)
    if vals[0] == 3:
        return (3, ranks)
    if vals == [2, 2, 1]:
        return (2, ranks)
    if vals[0] == 2:
        return (1, ranks)
    return (0, ranks)


LABELS = {
    0: "High card",
    1: "Pair",
    2: "Two pair",
    3: "Trips",
    4: "Straight",
    5: "Flush",
    6: "Full house",
    7: "Quads",
    8: "Straight flush",
}


def draw_card(surf, x, y, card, held, fonts):
    rect = pygame.Rect(x, y, 120, 168)
    pygame.draw.rect(surf, (250, 248, 240) if not held else (255, 240, 170), rect, border_radius=12)
    pygame.draw.rect(surf, (200, 140, 20) if held else (20, 20, 30), rect, 4, border_radius=12)
    r, s = card
    glyph, color = SUITS[s]
    rank = RANKS[r].replace("T", "10")
    surf.blit(fonts[0].render(rank, True, color), (x + 10, y + 8))
    surf.blit(fonts[1].render(glyph, True, color), (x + 32, y + 52))
    if held:
        surf.blit(fonts[2].render("HOLD", True, (140, 80, 0)), (x + 28, y + 140))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Neon Hold'em \u2014 ElbowOS")
    clock = pygame.time.Clock()
    fonts = (
        pygame.font.SysFont("arial", 26, bold=True),
        pygame.font.SysFont("arial", 56, bold=True),
        pygame.font.SysFont("arial", 16, bold=True),
        pygame.font.SysFont("arial", 22, bold=True),
    )

    bank = 200
    bet = 10
    phase = "deal"
    deck = []
    you = []
    house = []
    held = [False] * 5
    result = ""

    def deal():
        nonlocal deck, you, house, held, phase, result, bank
        if bank < bet:
            result = "Bank empty \u2014 N to reset bank"
            return
        bank -= bet
        deck = make_deck()
        you = [deck.pop() for _ in range(5)]
        house = [deck.pop() for _ in range(5)]
        held = [False] * 5
        phase = "hold"
        result = "Click cards or 1-5 to HOLD, then D to draw"

    def draw():
        nonlocal you, phase, result, bank
        for i in range(5):
            if not held[i]:
                you[i] = deck.pop()
        ys, hs = hand_score(you), hand_score(house)
        if ys > hs:
            bank += bet * 2
            result = f"You win  +{bet}   {LABELS[ys[0]]} beats {LABELS[hs[0]]}"
        elif ys < hs:
            result = f"House wins   {LABELS[hs[0]]} beats {LABELS[ys[0]]}"
        else:
            bank += bet
            result = "Push \u2014 bet returned"
        phase = "done"

    deal()

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
                    if phase != "hold":
                        if bank < bet:
                            bank = 200
                        deal()
                if event.key == pygame.K_d and phase == "hold":
                    draw()
                if phase == "hold" and event.key in (
                    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5
                ):
                    held[event.key - pygame.K_1] = not held[event.key - pygame.K_1]
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and phase == "hold":
                mx, my = event.pos
                for i in range(5):
                    r = pygame.Rect(50 + i * 180, 300, 120, 168)
                    if r.collidepoint(mx, my):
                        held[i] = not held[i]

        screen.fill((12, 28, 22))
        pygame.draw.rect(screen, (18, 90, 55), (20, 16, 920, 548), border_radius=18)
        screen.blit(fonts[3].render("NEON 5-CARD  vs HOUSE", True, (255, 220, 80)), (36, 28))
        screen.blit(fonts[2].render("https://x.com/ElbowOS", True, (180, 220, 180)), (760, 34))
        screen.blit(fonts[3].render(f"Bank ${bank}   bet ${bet}", True, (255, 255, 255)), (36, 64))
        screen.blit(fonts[2].render("House hand", True, (200, 220, 200)), (36, 100))

        show_house = phase == "done"
        for i, c in enumerate(house):
            x = 50 + i * 180
            if show_house:
                draw_card(screen, x, 124, c, False, fonts)
            else:
                pygame.draw.rect(screen, (30, 50, 120), (x, 124, 120, 168), border_radius=12)
                pygame.draw.rect(screen, (220, 190, 60), (x + 16, 140, 88, 136), 3, border_radius=8)

        screen.blit(fonts[2].render("Your hand", True, (200, 220, 200)), (36, 272))
        for i, c in enumerate(you):
            draw_card(screen, 50 + i * 180, 300, c, held[i] if phase == "hold" else False, fonts)

        screen.blit(fonts[3].render(result, True, (255, 240, 160)), (36, 488))
        screen.blit(fonts[2].render("1-5 / click hold   D draw   N next", True, (180, 210, 180)), (36, 528))
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
