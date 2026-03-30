# Sherlock Holmes: The Stolen Ruby

A 2D mobile mystery game built with Python and [Kivy](https://kivy.org/).

## Story

Lord Blackwood's priceless ruby has vanished from the British Museum. Scotland Yard is baffled. As Sherlock Holmes, you must investigate three locations, collect clues, and deduce the true culprit before they escape London.

## Screenshots

The game features hand-drawn vector scenes rendered entirely with Kivy's canvas API — no external image assets required.

| Main Menu | Scene Investigation | Case File | Verdict |
|-----------|-------------------|-----------|---------|
| Victorian foggy night | Tap objects to find clues | Review evidence | Correct or wrong? |

## Gameplay

1. **Investigate** — Navigate between three scenes: 221B Baker Street, the British Museum, and the East End Docks.
2. **Collect Clues** — Tap glowing objects to examine them. Each clue is added to your Case File.
3. **Deduce** — After collecting 4+ clues, accuse one of three suspects.
4. **Verdict** — Find out if your deduction was correct.

### Suspects

- **Colonel Moran** — Former army sharpshooter. Gambling debts.
- **Irene Adler** — Opera singer. Claims the ruby is rightfully hers.
- **Prof. Moriarty** — Criminal mastermind. Acting for a continental buyer.

## Running Locally (Desktop)

```bash
pip install kivy
cd sherlock_game
python main.py
```

## Android Build (via Buildozer)

```bash
pip install buildozer
cd sherlock_game
buildozer android debug deploy run
```

Requires the Android SDK/NDK. See [Buildozer docs](https://buildozer.readthedocs.io/).

## iOS Build (via Kivy-ios)

```bash
pip install kivy-ios
toolchain build python3 kivy
toolchain create SherlockHolmes .
```

## Project Structure

```
sherlock_game/
├── main.py                    # Entry point
├── buildozer.spec             # Android build config
├── requirements.txt
├── game/
│   ├── app.py                 # Kivy App + ScreenManager
│   ├── models/
│   │   └── game_state.py      # All game data & state
│   └── screens/
│       ├── menu_screen.py     # Animated Victorian main menu
│       ├── howtoplay_screen.py
│       ├── scene_screen.py    # Investigation scenes + object tap
│       ├── casefile_screen.py # Clue review
│       ├── deduction_screen.py# Accusation UI
│       └── verdict_screen.py  # Win/lose reveal
```

## Technical Notes

- All scene artwork (Baker Street interior, Museum, Docks) is drawn procedurally using Kivy's `canvas` API (`Rectangle`, `Ellipse`, `Line`).
- The `ObjectButton` widget uses a `Clock`-driven pulse animation to indicate interactive objects.
- Game state is a singleton (`game_state`) shared across all screens.
- Portrait orientation, 390×844 default (iPhone 14 size), fully responsive.
