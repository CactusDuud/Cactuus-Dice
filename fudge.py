"""
Property of Sage L Mahmud (https://github.com/CactusDuud)
Intended to be implemented alongside main.py
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/
"""

from random import choice


class DiceException(Exception):
    pass


class Dice:
    def __init__(self, command: int):
        if command > 0:
            self.rolls = command
            self.last_results = []
            self.last_sum = 0
        else:
            raise DiceException

    def __str__(self):
        return_str = f"{self.rolls if self.rolls > 1 else ''}dF"
        return return_str

    def roll(self):
        """Rolls the dice"""
        # Re-initialise values
        self.last_results = []
        self.last_sum = 0

        # Determine results
        self.last_results = [choice(('+', '.', '-')) for _ in range(self.rolls)]

        # Calculate sum of rolls
        self.count_sum()

    def count_sum(self):
        """Updates the sum of the last roll results"""
        for i in range(len(self.last_results)):
            if self.last_results[i] == '+':
                self.last_sum += 1
            elif self.last_results[i] == '-':
                self.last_sum -= 1

    def results(self) -> str:
        """Returns the results of the last roll as a string"""
        return f"({''.join(self.last_results)})"

    def sum(self) -> str:
        """Returns the sum of the last roll as a string"""
        return str(self.last_sum)
