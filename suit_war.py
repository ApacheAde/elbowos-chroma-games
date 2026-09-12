#!/usr/bin/env python3
"""Colourful War card game \u2014 player vs table."""
import random
import pygame

W, H = 900, 560
SUITS = [("\u2665", (200, 30, 50)), ("\u2666", (220, 80, 30)), ("\u2663", (30, 120, 60)), ("\u2660", (30, 30, 50))]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]


def deck():
    cards = [(r, s) for r in range(13) for s in range(4)]
    random.shuffle(cards)
    return cards


def draw_card(surf, x, y, card, face_up=True, font=None, big=None):
    rect = pygame.Rect(x, y, 110, 154)
    pygame.draw.rect(surf, (245, 245, 250), rect, border_radius=10)
    pygame.draw.rect(surf, (20, 20, 30), rect, 3, border_radius=10)
    if not face_up:
        pygame.draw.rect(surf, (40, 70, 160), rect.inflate(-10, -10), border_radius=8)
        pygame.draw.rect(surf, (220, 180, 50), rect.inflate(-28, -28), 3, border_radius=6)
        return
    r, s = card
    glyph, color = SUITS[s]
    label = RANKS[r]
    surf.blit(font.render(label, True, color), (x + 10, y + 8))
    surf.blit(big.render(glyph, True, color), (x + 28, y + 48))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Suit War \u2014 ElbowOS")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 22, bold=True)
    small = pygame.font.SysFont("arial", 18)
    huge = pygame.font.SysFont("arial", 64, bold=True)

    d = deck()
    pile_a, pile_b = d[:26], d[26:]
    shown_a = shown_b = None
    msg = "Space / click to flip"
    wars = 0

    def flip():
        nonlocal pile_a, pile_b, shown_a, shown_b, msg, wars
        if not pile_a or not pile_b:
            return
        shown_a, shown_b = pile_a.pop(0), pile_b.pop(0)
        pot = [shown_a, shown_b]
        a, b = shown_a[0], shown_b[0]
        while a == b:
            wars += 1
            if len(pile_a) < 2 or len(pile_b) < 2:
                msg = "War fizzles \u2014 not enough cards"
                break
            pot.extend([pile_a.pop(0), pile_b.pop(0)])
            shown_a, shown_b = pile_a.pop(0), pile_b.pop(0)
            pot.extend([shown_a, shown_b])
            a, b = shown_a[0], shown_b[0]
        else:
            random.shuffle(pot)
            if a > b:
                pile_a.extend(pot)
                msg = "You take the trick"
            else:
                pile_b.extend(pot)
                msg = "Table takes the trick"
        if not pile_a:
            msg = "Table wins the war"
        elif not pile_b:
            msg = "You win the war!"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    flip()
                if event.key == pygame.K_n:
                    d = deck()
                    pile_a, pile_b = d[:26], d[26:]
                    shown_a = shown_b = None
                    wars = 0
                    msg = "Fresh deck"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                flip()

        screen.fill((18, 90, 48))
        pygame.draw.rect(screen, (12, 70, 36), (30, 20, 840, 520), border_radius=16)
        screen.blit(font.render("SUIT WAR", True, (255, 230, 90)), (40, 32))
        screen.blit(small.render("https://x.com/ElbowOS", True, (200, 230, 180)), (680, 36))
        screen.blit(font.render(f"You  {len(pile_a)}", True, (255, 255, 255)), (160, 90))
        screen.blit(font.render(f"Table  {len(pile_b)}", True, (255, 255, 255)), (600, 90))
        screen.blit(small.render(f"{msg}   \u00b7   wars {wars}   \u00b7   N new game", True, (230, 230, 200)), (40, 520))

        draw_card(screen, 170, 160, (0, 0), face_up=False, font=font, big=huge)
        draw_card(screen, 610, 160, (0, 0), face_up=False, font=font, big=huge)
        if shown_a:
            draw_card(screen, 300, 200, shown_a, True, font, huge)
        if shown_b:
            draw_card(screen, 480, 200, shown_b, True, font, huge)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
