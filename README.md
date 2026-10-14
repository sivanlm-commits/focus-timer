# ⏱️ focus-timer

A tiny [Pomodoro](https://en.wikipedia.org/wiki/Pomodoro_Technique) timer for your terminal — one Python file, zero dependencies.

```
Round 1/4 — time to focus!
Focus  [██████████████░░░░░░░░░░░░░░░░] 13:22
```

## Usage

```bash
python3 focus.py                 # 25 min focus + 5 min break
python3 focus.py -w 50 -b 10     # custom lengths
python3 focus.py -r 4            # 4 rounds
python3 focus.py --stats         # see your focus history
```

Your finished sessions are saved to `~/.focus_timer_log.json`.

## Ideas / contributing

Pull requests welcome! Some ideas:
- Desktop notifications when a round ends
- A long break after every 4 rounds
- Weekly streak tracking

## License

MIT
