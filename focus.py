#!/usr/bin/env python3
"""focus-timer: a tiny Pomodoro timer for your terminal. No dependencies."""

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

LOG_FILE = Path.home() / ".focus_timer_log.json"
BAR_WIDTH = 30


def load_log():
    try:
        return json.loads(LOG_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_session(minutes):
    log = load_log()
    today = date.today().isoformat()
    log[today] = log.get(today, 0) + minutes
    LOG_FILE.write_text(json.dumps(log, indent=2))


def countdown(label, minutes):
    total = int(minutes * 60)
    try:
        for remaining in range(total, -1, -1):
            done = total - remaining
            filled = int(BAR_WIDTH * done / total) if total else BAR_WIDTH
            bar = "█" * filled + "░" * (BAR_WIDTH - filled)
            mins, secs = divmod(remaining, 60)
            sys.stdout.write(f"\r{label:<6} [{bar}] {mins:02d}:{secs:02d} ")
            sys.stdout.flush()
            if remaining:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped early. No worries — try again soon!")
        return False
    print("\a")  # terminal bell
    return True


def show_stats():
    log = load_log()
    if not log:
        print("No focus sessions yet. Run `python3 focus.py` to start one!")
        return
    print("Focus minutes by day:")
    for day in sorted(log)[-7:]:
        print(f"  {day}  {'▇' * (log[day] // 5):<20} {log[day]} min")
    print(f"Total: {sum(log.values())} minutes")


def main():
    parser = argparse.ArgumentParser(description="A tiny Pomodoro timer for your terminal.")
    parser.add_argument("-w", "--work", type=float, default=25, help="work minutes (default 25)")
    parser.add_argument("-b", "--break", dest="brk", type=float, default=5, help="break minutes (default 5)")
    parser.add_argument("-r", "--rounds", type=int, default=1, help="number of rounds (default 1)")
    parser.add_argument("--stats", action="store_true", help="show your focus history")
    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    for n in range(1, args.rounds + 1):
        print(f"Round {n}/{args.rounds} — time to focus!")
        if not countdown("Focus", args.work):
            return
        save_session(round(args.work))
        if n < args.rounds or args.rounds == 1:
            print("Nice work! Take a break.")
            if not countdown("Break", args.brk):
                return
    print("All done. 🎉  Run with --stats to see your progress.")


if __name__ == "__main__":
    main()
