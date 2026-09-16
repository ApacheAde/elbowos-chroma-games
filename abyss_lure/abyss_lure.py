#!/usr/bin/env python3
"""Abyss Lure neon deep-sea lure arcade for ElbowOS. Python 3 + pygame."""
import math, os, random, subprocess, sys
RECORD = "--record" in sys.argv or os.environ.get("ELBOWOS_RECORD") == "1"
PLAY = "--play" in sys.argv
if RECORD or not PLAY:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import pygame
W, H, FPS, SECS = 1080, 1920, 30, 15
OUT = os.environ.get("ELBOWOS_MP4", "/home/workdir/artifacts/ABYSS_LURE_ElbowOS.mp4")
TITLE, HANDLE = "ABYSS LURE", "x.com/ElbowOS"
VOID, INK, TEAL, GOLD, AMBER = (4, 8, 22), (8, 18, 42), (18, 210, 196), (255, 196, 64), (255, 150, 40)
VIOLET, MAG, CYAN, WHITE, ROSE, LIME, NAVY = (168, 92, 255), (255, 64, 196), (48, 220, 255), (244, 248, 255), (255, 90, 120), (140, 255, 90), (10, 28, 64)
class Game:
    def __init__(self):
        pygame.init(); pygame.font.init()
        flags = 0 if PLAY else pygame.HIDDEN
        try:
            self.screen = pygame.display.set_mode((W, H), flags)
        except pygame.error:
            os.environ["SDL_VIDEODRIVER"] = "dummy"; pygame.display.quit(); pygame.display.init()
            self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption(TITLE)
        self.font_lg = pygame.font.SysFont("DejaVu Sans", 62, bold=True)
        self.font = pygame.font.SysFont("DejaVu Sans", 38, bold=True)
        self.font_sm = pygame.font.SysFont("DejaVu Sans", 26)
        self.clock = pygame.time.Clock()
        self.score = self.combo = self.t = self.flash = self.catches = 0
        self.bx = W // 2; self.lx, self.ly = W // 2, 420; self.lvx, self.lvy = 0.0, 5.4
        self.reeling = False
        self.fish, self.jellies, self.sparks, self.bubbles, self.plankton = [], [], [], [], []
        self.pop, self.pop_t, self.spawn_timer = "", 0, 0
        for _ in range(70):
            self.plankton.append([random.randint(0, W), random.randint(200, H), random.uniform(0.2, 1.1), random.choice([TEAL, VIOLET, CYAN, MAG])])
        for _ in range(28):
            self.bubbles.append([random.randint(80, W - 80), random.randint(300, H), random.uniform(1.2, 3.4), random.randint(3, 8)])
    def burst(self, x, y, col, n=14):
        for _ in range(n):
            a = random.uniform(0, 6.2832); sp = random.uniform(1.6, 10)
            self.sparks.append([x, y, math.cos(a) * sp, math.sin(a) * sp, 20, col])
    def spawn_fish(self):
        side = random.choice((-1, 1)); y = random.randint(520, 1680)
        x = -40 if side > 0 else W + 40; spd = random.uniform(3.2, 6.4) * side
        self.fish.append([x, y, spd, random.choice(["gold", "cyan", "mag"]), random.uniform(0, 6.28)])
    def spawn_jelly(self):
        self.jellies.append([random.randint(120, W - 120), H + 40, random.uniform(-0.6, 0.6), random.uniform(-2.4, -1.4)])
    def autoplay(self):
        target, best = None, 1e9
        for f in self.fish:
            d = abs(f[1] - self.ly) + abs(f[0] - self.lx) * 0.45
            if d < best: best, target = d, f
        if self.ly > 1680 or (not self.fish and self.ly > 900): self.reeling = True
        elif target and self.ly < target[1] - 40: self.reeling = False
        if target:
            want = target[0] + target[2] * 8
            self.lvx += max(-0.9, min(0.9, (want - self.lx) * 0.04))
        self.lvx *= 0.92
    def tick(self):
        self.t += 1; self.flash = max(0, self.flash - 1); self.pop_t = max(0, self.pop_t - 1); self.spawn_timer += 1
        if self.spawn_timer % 22 == 0: self.spawn_fish()
        if self.spawn_timer % 70 == 0: self.spawn_jelly()
        self.bx += (self.lx - self.bx) * 0.08
        self.lvy += ((-9.2 if self.reeling else 6.1) - self.lvy) * (0.18 if self.reeling else 0.12)
        self.lx += self.lvx; self.ly += self.lvy
        self.lx = max(70, min(W - 70, self.lx))
        if self.ly < 340: self.ly, self.lvy, self.reeling = 340, abs(self.lvy) * 0.2, False
        if self.ly > 1760: self.ly, self.reeling = 1760, True
        for f in self.fish:
            f[0] += f[2]; f[1] += math.sin(self.t * 0.09 + f[4]) * 1.6; f[4] += 0.05
        self.fish = [f for f in self.fish if -80 < f[0] < W + 80]
        for j in self.jellies:
            j[0] += j[2] + math.sin(self.t * 0.07 + j[1] * 0.01) * 0.8; j[1] += j[3]
        self.jellies = [j for j in self.jellies if j[1] > 240]
        caught = []
        for i, f in enumerate(self.fish):
            if math.hypot(f[0] - self.lx, f[1] - self.ly) < 38:
                caught.append(i); pts = 55 if f[3] == "mag" else (40 if f[3] == "gold" else 25)
                self.combo += 1; self.score += pts + self.combo * 6; self.catches += 1
                self.flash, self.pop, self.pop_t, self.reeling = 7, "HOOKED", 16, True
                col = GOLD if f[3] == "gold" else (CYAN if f[3] == "cyan" else MAG)
                self.burst(f[0], f[1], col, 18)
        for i in reversed(caught): self.fish.pop(i)
        for j in self.jellies:
            if math.hypot(j[0] - self.lx, j[1] - self.ly) < 46:
                self.combo = 0; self.flash, self.pop, self.pop_t, self.reeling = 8, "STUNG", 14, True
                self.burst(self.lx, self.ly, ROSE, 16); j[1] = -200
        for p in self.sparks:
            p[0] += p[2]; p[1] += p[3]; p[3] += 0.12; p[4] -= 1
        self.sparks = [p for p in self.sparks if p[4] > 0]
        for b in self.bubbles:
            b[1] -= b[2]
            if b[1] < 220: b[1], b[0] = H + 10, random.randint(80, W - 80)
        for e in self.plankton:
            e[1] -= e[2]; e[0] += math.sin(self.t * 0.02 + e[1] * 0.01) * 0.4
            if e[1] < 180: e[1], e[0] = H + 8, random.randint(0, W)
    def draw(self, surf):
        surf.fill(VOID)
        for i in range(18):
            pygame.draw.rect(surf, (6 + i, 12 + i * 2, 28 + i * 3), (0, 180 + i * 100, W, 104))
        for e in self.plankton: pygame.draw.circle(surf, e[3], (int(e[0]), int(e[1])), 2)
        for b in self.bubbles: pygame.draw.circle(surf, (40, 80, 120), (int(b[0]), int(b[1])), b[3], 1)
        pygame.draw.rect(surf, INK, (0, 0, W, 230)); pygame.draw.rect(surf, TEAL, (0, 226, W, 6))
        pygame.draw.polygon(surf, NAVY, [(self.bx - 90, 210), (self.bx + 90, 210), (self.bx + 70, 168), (self.bx - 70, 168)])
        pygame.draw.polygon(surf, GOLD, [(self.bx - 22, 168), (self.bx + 22, 168), (self.bx, 128)])
        pygame.draw.line(surf, TEAL, (int(self.bx), 210), (int(self.lx), int(self.ly)), 3)
        pulse = 10 + int(4 * math.sin(self.t * 0.25))
        pygame.draw.circle(surf, GOLD, (int(self.lx), int(self.ly)), pulse + 8, 2)
        pygame.draw.circle(surf, AMBER, (int(self.lx), int(self.ly)), 16)
        pygame.draw.circle(surf, WHITE, (int(self.lx) - 4, int(self.ly) - 5), 5)
        pygame.draw.polygon(surf, LIME, [(int(self.lx) - 8, int(self.ly) + 14), (int(self.lx) + 8, int(self.ly) + 14), (int(self.lx), int(self.ly) + 30)])
        for f in self.fish:
            col = GOLD if f[3] == "gold" else (CYAN if f[3] == "cyan" else MAG)
            fx, fy, face = int(f[0]), int(f[1]), 1 if f[2] > 0 else -1
            pygame.draw.ellipse(surf, col, (fx - 22, fy - 12, 44, 24))
            pygame.draw.polygon(surf, col, [(fx - 22 * face, fy), (fx - 38 * face, fy - 12), (fx - 38 * face, fy + 12)])
            pygame.draw.circle(surf, WHITE, (fx + 10 * face, fy - 2), 4); pygame.draw.circle(surf, VOID, (fx + 12 * face, fy - 2), 2)
        for j in self.jellies:
            jx, jy = int(j[0]), int(j[1])
            pygame.draw.ellipse(surf, VIOLET, (jx - 28, jy - 18, 56, 36), 3); pygame.draw.ellipse(surf, MAG, (jx - 16, jy - 10, 32, 22))
            for k in range(5):
                tx = jx - 20 + k * 10
                pygame.draw.line(surf, VIOLET, (tx, jy + 14), (tx + int(6 * math.sin(self.t * 0.2 + k)), jy + 48), 2)
        for p in self.sparks: pygame.draw.circle(surf, p[5], (int(p[0]), int(p[1])), max(2, p[4] // 5))
        if self.flash:
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((255, 196, 64, 28) if self.pop != "STUNG" else (255, 64, 120, 36)); surf.blit(ov, (0, 0))
        if self.pop_t:
            lab = self.font_lg.render(self.pop, True, ROSE if self.pop == "STUNG" else GOLD)
            surf.blit(lab, lab.get_rect(center=(W // 2, 640)))
        title = self.font_lg.render(TITLE, True, GOLD); surf.blit(title, title.get_rect(center=(W // 2, 72)))
        sub = self.font_sm.render(HANDLE, True, MAG); surf.blit(sub, sub.get_rect(center=(W // 2, 132)))
        sc = self.font.render(f"SCORE  {self.score}", True, WHITE)
        cb = self.font_sm.render(f"STREAK  x{self.combo}   CATCH  {self.catches}", True, TEAL)
        hint = self.font_sm.render("A D steer   W / SPACE reel", True, AMBER)
        surf.blit(sc, sc.get_rect(center=(W // 2, H - 150)))
        surf.blit(cb, cb.get_rect(center=(W // 2, H - 96)))
        surf.blit(hint, hint.get_rect(center=(W // 2, H - 48)))
    def play_interactive(self):
        running = True
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE): running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: self.lvx -= 0.7
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.lvx += 0.7
            self.reeling = keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
            self.lvx *= 0.9; self.tick(); self.draw(self.screen); pygame.display.flip(); self.clock.tick(FPS)
        pygame.quit()
    def record(self):
        frames = FPS * SECS
        cmd = ["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "fast", "-movflags", "+faststart", OUT]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        canvas = pygame.Surface((W, H))
        try:
            for i in range(frames):
                self.autoplay(); self.tick(); self.draw(canvas)
                proc.stdin.write(pygame.image.tostring(canvas, "RGB"))
                if i % 30 == 0: print(f"frame {i}/{frames}", flush=True)
        finally:
            proc.stdin.close(); err = proc.stderr.read().decode("utf-8", "ignore"); rc = proc.wait()
        if rc != 0: raise SystemExit(f"ffmpeg failed ({rc}):\n{err[-1200:]}")
        print("wrote", OUT); pygame.quit()
def main():
    g = Game()
    if PLAY and not RECORD: g.play_interactive()
    else: g.record()
if __name__ == "__main__": main()
