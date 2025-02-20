#!/usr/bin/env python

import argparse
import random

class DiceRoll():
    def __init__(self, sides):
        self.sides = sides

    def roll():
        roll = random.choices(range(self.sides))
        print(roll)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", help="Roll an n-sided dice", 
                        dest='sides', type=int, default=6)
    args = parser.parse_args()

    print(DiceRoll.roll(sides=args.sides))