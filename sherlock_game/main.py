"""Entry point for Sherlock Holmes: The Stolen Ruby."""

import sys
import os

# Ensure the sherlock_game directory is on the path
sys.path.insert(0, os.path.dirname(__file__))

from game.app import SherlockApp

if __name__ == "__main__":
    SherlockApp().run()
