# ElbowOS Chroma Games

A new pack of **distinct**, full-colour **Python 3** mini-games built with [pygame](https://www.pygame.org/).

These are original arcade / table games. They are **not** commercial emulators, **not** ROM players, and they do not use trademarked characters.

Featured / shout-out: **[https://x.com/ElbowOS](https://x.com/ElbowOS)**

## Games

| File | Kind | How to play |
|---|---|---|
| `pipe_runner.py` | Side-scrolling platformer (Mario-*feel*, original plumber mascot) | ← → run, Space jump, R restart |
| `suit_war.py` | Card game — War | Click or Space to flip |
| `neon_holdem.py` | Casino cards — 5-card vs house | 1-5 / click hold, D draw, N new |
| `crystal_slots.py` | Casino — 3-reel slots | Space spin |
| `plinko_drop.py` | Casino — Plinko / pachinko board | Click or Space to drop a chip |
| `gem_grid.py` | Puzzle — swap gems to match 3 | Click two adjacent gems |
| `star_raid.py` | Arcade shooter | ← → move, Space fire |

Launch them all from one colourful menu:

```bash
python3 play.py
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 play.py
```

Needs Python 3.10+ and a desktop window (pygame + SDL).

## Why no “Mario emulator”?

A real Mario Bros emulator needs copyrighted ROMs and a CPU/PPU cycle-accurate core. That is a different project and is not bundled here. `pipe_runner.py` is an original platformer with pipes, coins and patrol foes — same *genre*, original art and rules.

## License

MIT. Original code.
